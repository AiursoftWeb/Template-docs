# Step 9 - Upload an Image for a Note

Use the existing signed-upload pipeline.

This example gives each signed-in user a separate folder, previews a public image, and provides Markdown to paste into a note.

The note stores the generated image URL as part of its Markdown content; the uploader's form stores the logical path, not a filesystem path.

These Workspace images are public even when the note is private; use the [Vault guidance](../Features/SaveFile.md) for confidential attachments.


Stop the server with **Ctrl+C** before editing.

```bash
cd ~/Source/MyOrg.MarkToHtml
```

This returns to the repository root. All file paths below start there.

**Our goal:** upload one picture and put its Markdown into a saved note.

We need three files. Let's give each a small job:

- The model receives the uploaded image's logical path.
- The controller checks that the path belongs to this user.
- The view shows the existing upload widget and the resulting Markdown.

## 9.1 Add the upload model and controller

Create `src/MyOrg.MarkToHtml/Models/UploadsViewModels/IndexViewModel.cs`:

```csharp
using System.ComponentModel.DataAnnotations;
using Aiursoft.UiStack.Layout;

namespace MyOrg.MarkToHtml.Models.UploadsViewModels;

public class IndexViewModel : UiStackLayoutViewModel
{
    public IndexViewModel() { PageTitle = "Upload a note image"; }

    [Required]
    [MaxLength(150)]
    public string? FilePath { get; set; }
    public string? ImageUrl { get; set; }
}
```

Create `src/MyOrg.MarkToHtml/Controllers/UploadsController.cs`:

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Localization;
using MyOrg.MarkToHtml.Entities;
using MyOrg.MarkToHtml.Models.UploadsViewModels;
using MyOrg.MarkToHtml.Services;
using MyOrg.MarkToHtml.Services.FileStorage;

namespace MyOrg.MarkToHtml.Controllers;

[Authorize]
public class UploadsController(UserManager<User> users, StorageService storage,
    IStringLocalizer<UploadsController> localizer) : Controller
{
    [HttpGet]
    public IActionResult Index() => this.StackView(new IndexViewModel());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Index(IndexViewModel model)
    {
        if (!ModelState.IsValid) return this.StackView(model);
        var prefix = $"note-images/{users.GetUserId(User)}/";
        var path = model.FilePath!;
        if (!path.StartsWith(prefix, StringComparison.Ordinal) ||
            path.Contains('\\') || path.Split('/').Length != 3 ||
            !new[] { ".png", ".jpg", ".jpeg" }.Contains(Path.GetExtension(path).ToLowerInvariant()))
        {
            return Forbid();
        }
        if (!System.IO.File.Exists(storage.GetFilePhysicalPath(path)))
        {
            ModelState.AddModelError(nameof(model.FilePath), localizer["Upload an image first."]);
            return this.StackView(model);
        }
        model.ImageUrl = storage.RelativePathToInternetUrl(path);
        return this.StackView(model);
    }
}
```

The common FilesController validates the signed grant, extension, size and content.

The business controller independently checks that the returned path belongs to the signed-in user's folder.

A valid upload token from another feature is not proof of ownership here.

## 9.2 Add the view

Create `src/MyOrg.MarkToHtml/Views/Uploads/Index.cshtml`:

```html
@using Microsoft.AspNetCore.Identity
@using MyOrg.MarkToHtml.Entities
@model MyOrg.MarkToHtml.Models.UploadsViewModels.IndexViewModel
@inject UserManager<User> Users

<h1>@Localizer["Upload a note image"]</h1>
<p>@Localizer["These images are public. Do not upload confidential files."]</p>
<form method="post" asp-action="Index">
    <vc:file-upload asp-for="FilePath"
                    subfolder="@($"note-images/{Users.GetUserId(User)}")"
                    allowed-extensions="jpg jpeg png" max-size-in-mb="5" />
    <span asp-validation-for="FilePath" class="text-danger"></span>
    <button type="submit" class="btn btn-primary">@Localizer["Use image"]</button>
</form>
@if (!string.IsNullOrEmpty(Model.ImageUrl))
{
    <img src="@Model.ImageUrl" alt="@Localizer["Uploaded note image"]" class="img-fluid" />
    <p>@Localizer["Copy this Markdown into your note and save the note:"]</p>
    <textarea class="form-control" readonly>@($"![Note image]({Model.ImageUrl})")</textarea>
}
@section styles {
    <link rel="stylesheet" href="~/node_modules/dropify/dist/css/dropify.min.css" />
    <link rel="stylesheet" href="~/styles/uploader.css" />
}
@section scripts {
    <script src="~/node_modules/dropify/dist/js/dropify.min.js"></script>
}
```

The component uses the existing uploader script and Dropify. Keep the generated Dropify entry in package.json's keep map. No extra upload endpoint or direct IFormFile write is needed.

## Checkpoint 9 - Put a picture in a note

Save all three new files.

```bash
dotnet build ./MyOrg.MarkToHtml.sln
```

This checks the model, controller, and Razor view together.
**Expected:** a successful build.

```bash
dotnet run --project ./src/MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

This starts the updated app. Sign in, then type `http://localhost:5000/Uploads` in the browser address bar.
The new page is not automatically added to the menu.

Take these actions one at a time:
 1. Select a small PNG or JPEG. Wait for the upload to finish.
2. Click **Use image**. Expect a preview and a box containing a Markdown image line.
3. Copy that whole Markdown line into a note, then save the note.
4. Reopen the note and switch to Preview. Expect the picture to load.
5. Try a `.txt` file in the widget. Expect it to be rejected.
6. Sign out and open the Uploads URL again. Expect the login page.

A picture in Workspace is publicly downloadable if someone has its URL.
A private note does not make its picture private.
Use the Vault guidance linked above when that is not acceptable.

Press **Ctrl+C** after checking. Keep the note for the next chapter.

Continue with [Step 10](./step10.md).
