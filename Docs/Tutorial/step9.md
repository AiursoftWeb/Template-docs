# Step 9 - Upload an Image for a Note

Use the existing signed-upload pipeline. This example gives each signed-in user a separate folder, previews a public image, and provides Markdown to paste into a note. The note stores the generated image URL as part of its Markdown content; the uploader's form stores the logical path, not a filesystem path. These Workspace images are public even when the note is private; use the [Vault guidance](../Features/SaveFile.md) for confidential attachments.

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

The common FilesController validates the signed grant, extension, size and content. The business controller independently checks that the returned path belongs to the signed-in user's folder. A valid upload token from another feature is not proof of ownership here.

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

## 9.3 Verify

From the repository root, build and run the project as in Step 1. Sign in, open `/Uploads`, upload a PNG or JPEG smaller than 5 MiB, then select **Use image**. Copy the generated Markdown into a note and save it. Reopen the note and verify the image loads. Try a disallowed extension and another user's logical path; both must be rejected. Signing out must prevent opening `/Uploads`.

Continue with [Step 10](./step10.md).
