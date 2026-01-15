# File Storage and Upload Module (Refactored)

This module aims to make file uploading **extremely simple and secure**.

The core design philosophy is **"Logical Path"**:

* **Frontend/Database/API**: Only handle clean logical paths (e.g., `avatar/2026/01/14/logo.png`).
* **Backend底层**: Automatically map to physically isolated storage areas (e.g., `/data/Workspace/...`).

---

## 🚫 Prohibited Operations

1. **Prohibited** to use traditional HTML `<input type="file">` controls — this significantly increases workload, greatly expands the attack surface, and prevents access to advanced features like compression and privacy sanitization.
2. **Prohibited** to directly receive `IFormFile` in business Controllers.
3. **Prohibited** to manually concatenate physical paths to access files — always use `StorageService`.

---

## 🚀 Quick Integration: Three Steps

### Step 1: View (Place Control)

In the `.cshtml` page, use the `vc:file-upload` component.

```html
<form asp-action="UpdateProfile" method="post">
    <vc:file-upload 
        asp-for="IconPath" 
        upload-endpoint="/upload/avatar" 
        allowed-extensions="jpg png">
    </vc:file-upload>

    <button type="submit">提交</button>
</form>

@* ReSharper disable once Razor.SectionNotResolved *@
@section styles {
    <link rel="stylesheet" href="~/node_modules/dropify/dist/css/dropify.min.css" />
    <link rel="stylesheet" href="~/styles/uploader.css" />
}

@* ReSharper disable once Razor.SectionNotResolved *@
@section scripts {
    <script src="~/node_modules/dropify/dist/js/dropify.min.js"></script>
}
```

### Step 2: ViewModel (Bind Model and Validation)

The file upload is submitted separately and does not affect the main form submission. The ViewModel only needs a string property to receive the logical path.

Note: The logical path is neither a URL nor a physical path, but a "virtual path" representing the file's location within the storage system. Using a logical path allows the system to automatically handle file storage and access details, and helps prevent attacks exploiting path vulnerabilities.

```csharp
public class UpdateProfileViewModel
{
    [NotNull]
    [Display(Name = "Avatar file")]
    [Required(ErrorMessage = "The avatar file is required.")]
    [MaxLength(150)]
    [MinLength(2)]
    // 这里接收的是逻辑路径，例如 "avatar/2025/01/01/xxx.jpg"
    // ✅ 校验业务桶前缀，确保这里只能提交被上传到 `/avatar` 目录下的文件
    [RegularExpression(@"^avatar.*", ErrorMessage = "请上传正确的头像文件。")]
    public string? IconPath { get; set; }
}

```

### Step 3: Controller (Save to Database)

The business Controller does not need to handle file streams; treat them like ordinary strings.

```csharp
[HttpPost]
public async Task<IActionResult> UpdateProfile(UpdateProfileViewModel model)
{
    if (!ModelState.IsValid) return this.StackView(model);

    var user = await _userManager.GetUserAsync(User);
    
    // 直接存入逻辑路径
    // DB 存储示例: "avatar/2026/01/14/uuid.jpg"
    user.IconPath = model.IconPath; 
    
    await _userManager.UpdateAsync(user);
    return RedirectToAction(nameof(Index));
}

```

Of course, if the business Controller needs to check files, such as whether they exist or have the correct MIME type, it can also do so through `StorageService`.

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> ChangeAvatar(ChangeAvatarViewModel model)
{
    if (!ModelState.IsValid)
    {
        return this.StackView(model);
    }

    // Make sure the file is actually a photo.
    var absolutePath = storageService.GetFilePhysicalPath(model.AvatarUrl);
    if (!await image.IsValidImageAsync(absolutePath))
    {
        ModelState.AddModelError(string.Empty, localizer["The file is not a valid image."]);
        return this.StackView(model);
    }

    // Save the new avatar in the database.
    var user = await GetCurrentUserAsync();
    if (user != null)
    {
        user.AvatarRelativePath = model.AvatarUrl;
        await userManager.UpdateAsync(user);

        // Sign in the user to refresh the avatar.
        await signInManager.SignInAsync(user, isPersistent: false);
        return RedirectToAction(nameof(Index), new { Message = ManageMessageId.ChangeAvatarSuccess });
    }

    return this.StackView(model);
}
```

### Step 4: Distribute Files

Finally, when we need to display the files, we still use `StorageService` to convert them into internet-accessible URLs.

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage
<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" alt="User Avatar" />
```

Even if hackers successfully store malicious files or URLs from third-party servers into the database, they cannot access the actual files during rendering, because the system only allows access to files corresponding to these logical paths through `StorageService`.

**Supported dynamic parameters**:

* `?w=200`: Scale width (automatically maintains aspect ratio).
* `?square=true`: Center-crop to a square.
* **Default behavior**: All image download requests will **automatically remove EXIF information** (GPS, camera settings), protecting user privacy.

## 🏗️ Architecture Deep Dive

This module employs an advanced architecture based on **"physical isolation, logical unification"**.

### 1. Directory Layout

The server's physical disk (`/data`) is strictly divided into three regions:

```text
/data (存储根)
├── Workspace/        # [Source of Truth] 原始数据区
│   └── avatar/       # 仅供上传写入，不对外直接暴露
│
├── ClearExif/        # [Privacy Layer] 隐私清洗区 (缓存)
│   └── avatar/       # 下载原图时，实际读取的是这里的无EXIF副本
│
└── Compressed/       # [Cache Layer] 缩略图区 (缓存)
    └── avatar/       # 下载带参图片时，读取这里的压缩副本

```

### 2. Path Translation Mechanism

`StorageService` acts as a **smart gateway**, mapping user-defined logical paths to different physical regions, achieving "transparent security protection".

| User Request (API) | Logical Path (Internal) | Actual Physical Operation (Physical) | Notes |
| --- | --- | --- | --- |
| **Upload** | `avatar/img.png` | Write to `/data/Workspace/avatar/img.png` | Original file goes in but never comes out |
| **Download Original** | `avatar/img.png` | Read from `/data/ClearExif/avatar/img.png` | Automatically cleans privacy information |
| **Download Thumbnail** | `avatar/img.png` | Read from `/data/Compressed/avatar/img_w200.png` | Automatically compressed for faster delivery |

## 🧩 Core Service Reference

* **StorageService**: Core gateway handling path mapping, file storage, and access control checks.
* **ImageProcessingService**: Handles image compression, privacy removal, and format validation.
* **FeatureFoldersProvider**: (Internal) Configuration source managing physical directory structure.
* **FileUploadController**: Provides a unified upload endpoint, handling frontend upload requests.
