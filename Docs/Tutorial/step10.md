# Step 10 - Soft Delete and Recycle Bin

Continue with the MarkdownDocument entity from Step 4. Deleted documents should disappear from normal queries, remain restorable by their owner for 30 days, and then be removed by the existing background-job system.

## 10.1 Extend the existing entity and mapping

Add these properties inside MarkdownDocument:

```csharp
public bool IsDeleted { get; set; }
public DateTime? DateDeleted { get; set; }
```

In the existing TemplateDbContext, add this override. If an override already exists, append the entity configuration after its base call instead of replacing the method:

```csharp
protected override void OnModelCreating(ModelBuilder builder)
{
    base.OnModelCreating(builder);
    builder.Entity<MarkdownDocument>().HasQueryFilter(d => !d.IsDeleted);
}
```

Generate AddMarkdownDocumentSoftDelete migrations for both SQLite and MySQL using the commands from Step 4, changing the migration name. The MySQL connection must be configured before generating its migration. Return to SQLite for local development afterwards. Restart the app to apply its selected provider's migration.

## 10.2 Change the existing delete actions

In HomeController.DeleteConfirmed, replace `context.MarkdownDocuments.Remove(document);` with:

```csharp
document.IsDeleted = true;
document.DateDeleted = DateTime.UtcNow;
```

Keep its existing owner check, antiforgery validation, SaveChangesAsync and redirect. Make the same replacement in AdminController.DeleteDocumentConfirmed, retaining its CanDeleteAnyDocument policy. Normal history, edit and admin queries now hide deleted documents automatically. In the existing Home/Delete and Admin/DeleteDocument confirmation views, replace any text claiming the action is irreversible or permanent with a localized message such as `This note will move to the recycle bin for 30 days.` Keep the existing form actions and antiforgery handling.

## 10.3 Add an owner-scoped recycle bin

Create `Models/RecycleBinViewModels/IndexViewModel.cs` in the web project:

```csharp
using Aiursoft.UiStack.Layout;
using MyOrg.MarkToHtml.Entities;

namespace MyOrg.MarkToHtml.Models.RecycleBinViewModels;

public class IndexViewModel : UiStackLayoutViewModel
{
    public IndexViewModel() { PageTitle = "Recycle bin"; }
    public IEnumerable<MarkdownDocument> Documents { get; set; } = [];
}
```

Create `Controllers/RecycleBinController.cs`:

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyOrg.MarkToHtml.Entities;
using MyOrg.MarkToHtml.Models.RecycleBinViewModels;
using MyOrg.MarkToHtml.Services;

namespace MyOrg.MarkToHtml.Controllers;

[Authorize]
public class RecycleBinController(TemplateDbContext db, UserManager<User> users) : Controller
{
    public async Task<IActionResult> Index()
    {
        var userId = users.GetUserId(User);
        var documents = await db.MarkdownDocuments.IgnoreQueryFilters()
            .Where(d => d.UserId == userId && d.IsDeleted)
            .OrderByDescending(d => d.DateDeleted).ToListAsync();
        return this.StackView(new IndexViewModel { Documents = documents });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Restore(Guid id)
    {
        var userId = users.GetUserId(User);
        var document = await db.MarkdownDocuments.IgnoreQueryFilters()
            .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId && d.IsDeleted);
        if (document == null) return NotFound();
        document.IsDeleted = false;
        document.DateDeleted = null;
        await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }
}
```

IgnoreQueryFilters is deliberately followed by both an owner check and an IsDeleted check. Do not expose an unrestricted query of deleted documents to ordinary users.

Create `Views/RecycleBin/Index.cshtml`:

```html
@model MyOrg.MarkToHtml.Models.RecycleBinViewModels.IndexViewModel
<h1>@Localizer["Recycle bin"]</h1>
<p>@Localizer["Deleted notes are kept for 30 days before permanent cleanup."]</p>
<a asp-controller="Home" asp-action="History">@Localizer["My documents"]</a>
@foreach (var document in Model.Documents)
{
    <div class="card my-3"><div class="card-body">
        <h2 class="h5">@document.Title</h2>
        <form asp-action="Restore" method="post">
            <input type="hidden" name="id" value="@document.Id" />
            <button type="submit" class="btn btn-primary">@Localizer["Restore"]</button>
        </form>
    </div></div>
}
```

Add a link to `/RecycleBin` in the existing History view:

```html
<a asp-controller="RecycleBin" asp-action="Index">@Localizer["Recycle bin"]</a>
```

## 10.4 Register the cleanup job

Create `Services/BackgroundJobs/RecycleBinCleanupJob.cs`:

```csharp
using Aiursoft.Canon.BackgroundJobs;
using Microsoft.EntityFrameworkCore;
using MyOrg.MarkToHtml.Entities;

namespace MyOrg.MarkToHtml.Services.BackgroundJobs;

public class RecycleBinCleanupJob(TemplateDbContext db) : IBackgroundJob
{
    public string Name => "Recycle bin cleanup";
    public string Description => "Permanently deletes notes that were deleted more than 30 days ago.";

    public async Task ExecuteAsync()
    {
        var threshold = DateTime.UtcNow.AddDays(-30);
        var expired = await db.MarkdownDocuments.IgnoreQueryFilters()
            .Where(d => d.IsDeleted && d.DateDeleted < threshold).ToListAsync();
        db.MarkdownDocuments.RemoveRange(expired);
        await db.SaveChangesAsync();
    }
}
```

In Startup.ConfigureServices, alongside the existing job registrations, add:

```csharp
var recycleJob = services.RegisterBackgroundJob<RecycleBinCleanupJob>();
services.RegisterScheduledTask(
    registration: recycleJob,
    period: TimeSpan.FromDays(1),
    startDelay: TimeSpan.FromMinutes(10));
```

Keep the existing Aiursoft.Canon.BackgroundJobs and Aiursoft.Canon.ScheduledTasks imports, and import MyOrg.MarkToHtml.Services.BackgroundJobs. Do not add a second scheduler or modify the existing jobs.

## 10.5 Verify

Create and delete a note. It should disappear from History and Edit, appear in `/RecycleBin`, and return to History after Restore. A second user must not see or restore it. Delete a fresh note and run **Recycle bin cleanup** from `/Jobs`; the fresh note must remain restorable. In an isolated test database, give a deleted test note a DateDeleted older than 30 days and trigger cleanup again: that note must be physically removed while fresh deleted and active notes remain. Job execution is asynchronous; inspect the Jobs result rather than treating the trigger redirect as completion.

Uploaded images are not deleted by this note cleanup: multiple notes may reference the same image. File retention is a separate business decision.

Continue with [Step 11](./step11.md).
