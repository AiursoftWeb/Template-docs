# 文件存储与上传模块 (Refactored)

本模块旨在让文件上传变得**极度简单且安全**。

核心设计哲学是 **“逻辑路径 (Logical Path)”**：

* **前端/数据库/API**：只处理干净的逻辑路径（如 `avatar/2026/01/14/logo.png`）。
* **后端底层**：自动映射到物理隔离的存储区（如 `/data/Workspace/...`）。

---

## 🚫 严禁操作

1. **严禁**使用传统的 HTML `<input type="file">` 控件，这会巨大增加工作量，并且巨大的增加攻击面，还享受不到压缩、隐私清洗等高级功能。
2. **严禁**在业务 Controller 中直接接收 `IFormFile`。
3. **严禁**手动拼接物理路径访问文件，必须通过 `StorageService`。

---

## 🚀 快速集成：三步走

### 第一步：View (放控件)

在 `.cshtml` 页面中，使用 `vc:file-upload` 组件。

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

### 第二步：ViewModel (绑模型与校验)

接收文件是单独的提交，不会影响主表单的提交。ViewModel 只需要一个字符串属性来接收逻辑路径。

注意：逻辑路径不是 URL，也不是物理路径，而是一个“虚拟路径”，代表文件在存储系统中的位置。使用逻辑路径可以让系统自动处理文件的存储和访问细节，并且避免黑客利用路径漏洞进行攻击。

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

### 第三步：Controller (存数据库)

业务 Controller 不需要处理文件流，像处理普通字符串一样即可。

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

当然，业务 Controller 如果需要检查文件，例如是否存在、MIME 类型是否正确，也可以通过 `StorageService` 来完成。

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

### 第四步：分发文件

最后，我们需要展示文件时，仍然通过 `StorageService` 来将其转换为互联网可访问的 URL。

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage
<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" alt="User Avatar" />
```

黑客即使将恶意文件或第三方服务器的 URL 成功存入数据库，渲染时也无法访问到真实文件，因为系统只允许通过 `StorageService` 访问这些逻辑路径所对应的文件。

**支持的动态参数**：

* `?w=200`: 缩放宽度（自动按比例）。
* `?square=true`: 居中裁剪正方形。
* **默认行为**: 所有图片下载请求，**均会自动清除 EXIF 信息**（GPS、相机参数），保护用户隐私。

## 🏗️ 架构原理 (Architecture Deep Dive)

本模块采用了 **"物理隔离，逻辑统一"** 的高级架构。

### 1. 目录结构 (Directory Layout)

服务器物理磁盘（`/data`）被严格划分为三个区域：

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

### 2. 路径转换机制 (Path Translation)

`StorageService` 充当了**智能网关**，将用户的逻辑路径映射到不同的物理区域，实现“无感知的安全保护”。

| 用户请求 (API) | 逻辑路径 (Internal) | 实际物理操作 (Physical) | 说明 |
| --- | --- | --- | --- |
| **上传** | `avatar/img.png` | Write to `/data/Workspace/avatar/img.png` | 原始文件只进不出 |
| **下载原图** | `avatar/img.png` | Read from `/data/ClearExif/avatar/img.png` | 自动清洗隐私信息 |
| **下载缩略图** | `avatar/img.png` | Read from `/data/Compressed/avatar/img_w200.png` | 自动压缩加速 |

## 🧩 核心服务参考

* **StorageService**: 核心网关，处理路径映射、文件存储、防越权检查。
* **ImageProcessingService**: 处理图片压缩、去隐私、格式校验。
* **FeatureFoldersProvider**: (Internal) 管理物理目录结构的配置源。
* **FileUploadController**: 提供统一的上传端点，处理前端上传请求。
