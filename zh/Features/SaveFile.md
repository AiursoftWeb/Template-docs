# 文件存储与上传模块（重构版）

此模块旨在使文件上传**极为简单且安全**。

核心设计哲学是**“逻辑路径”**：

* **前端/数据库/API**：仅处理清晰的逻辑路径（例如：`avatar/2026/01/14/logo.png`）。
* **后端底层**：自动映射到物理隔离的存储区域（例如：`/data/Workspace/...`）。

---

## 🚫 禁止操作

1. **禁止**使用传统的 HTML `<input type="file">` 控件——这会显著增加工作量，极大扩展攻击面，并阻止访问压缩和隐私净化等高级功能。
2. **禁止**在业务 Controller 中直接接收 `IFormFile`。
3. **禁止**手动拼接物理路径来访问文件——始终使用 `StorageService`。

---

## 🔐 公开文件与私有文件

此模块支持**公开**和**私有**文件存储：

### 公开文件（默认）

* **存储**: 保存在 `Workspace` 文件夹中
* **访问**: 拥有 URL 的任何人都可以下载
* **使用场景**: 用户头像、产品图片、公开文档
* **URL 格式**: `/download/avatar/2026/01/14/logo.png`

### 私有文件（Vault）

* **存储**: 保存在独立的 `Vault` 文件夹中
* **访问**: 需要一个限时、经过加密签名的令牌
* **使用场景**: 私有文档、敏感数据、机密文件、用户的个人数据
* **URL 格式**: `/download-private/contract/2026/01/14/agreement.pdf?token=<base64编码的令牌>`
* **安全机制**: 
  - 令牌在 60 分钟后过期
  - HMAC-SHA256 签名防止篡改
  - 路径级授权（令牌验证精确的文件路径）

---

## 🚀 快速集成：三步完成

### 步骤 1：查看（放置控件）

在 `.cshtml` 页面中，使用 `vc:file-upload` 组件。

**对于公开文件：**

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

**对于私人文件：**

```html
<form asp-action="UpdateContract" method="post">
    <vc:file-upload 
        asp-for="ContractPath" 
        upload-endpoint="/upload/contract?useVault=true" 
        allowed-extensions="pdf docx">
    </vc:file-upload>

    <button type="submit">上传私有文件</button>
</form>
```

> **注意**：向上传递端点添加 `?useVault=true` 以将文件存储在私有 Vault 中。

### 第 2 步：ViewModel（绑定模型和验证）

文件上传是单独提交的，不会影响主表单的提交。ViewModel 只需要一个字符串属性来接收逻辑路径。

注意：逻辑路径既不是 URL 也不是物理路径，而是一种“虚拟路径”，用于表示文件在存储系统中的位置。使用逻辑路径可以让系统自动处理文件存储和访问细节，并有助于防止利用路径漏洞的攻击。

**对于公开文件：**

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

**对于私人文件：**

```csharp
public class UpdateContractViewModel
{
    [NotNull]
    [Display(Name = "Contract Document")]
    [Required(ErrorMessage = "The contract file is required.")]
    [MaxLength(150)]
    [MinLength(2)]
    // 私有文件同样使用逻辑路径
    // ✅ 校验业务桶前缀，确保只能提交到 `/contract` 目录下
    [RegularExpression(@"^contract.*", ErrorMessage = "请上传正确的合同文件。")]
    public string? ContractPath { get; set; }
}
```

### 步骤 3：控制器（保存到数据库）

业务控制器无需处理文件流；将其视为普通字符串即可。

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

当然，如果业务 Controller 需要检查文件，例如文件是否存在或具有正确的 MIME 类型，也可以通过 `StorageService` 完成。

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

### 第4步：分发文件

最后，当需要显示文件时，我们仍然使用 `StorageService` 将其转换为可访问的互联网URL。

**对于公共文件：**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage
<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" alt="User Avatar" />
```

**对于私有文件：**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage
<!-- Token is automatically generated and embedded in the URL -->
<a href="@Storage.RelativePathToInternetUrl(Model.ContractPath, isVault: true)" 
   download="contract.pdf">
    Download Contract
</a>
```

> **重要**：
> - 对于私有文件，在 `RelativePathToInternetUrl()` 中设置 `isVault: true`
> - 系统会自动在 URL 中生成一个限时令牌
> - 令牌默认有效时间为 60 分钟
> - 每个令牌都经过加密签名且与路径绑定

即使黑客成功将第三方服务器的恶意文件或 URL 存储到数据库中，他们在渲染时也无法访问实际文件，因为系统仅允许通过 `StorageService` 访问与这些逻辑路径对应的文件。

**支持的动态参数**：

* `?w=200`：按比例缩放宽度。
* `?square=true`：居中裁剪为正方形。
* **默认行为**：所有图像下载请求将**自动移除 EXIF 信息**（GPS、相机设置），保护用户隐私。

## 🏗️ 架构深度解析

此模块采用基于 **“物理隔离，逻辑统一”** 的先进架构。

### 1. 目录结构

服务器的物理磁盘 (`/data`) 严格划分为四个区域：

```text
/data (存储根)
├── Workspace/        # [Source of Truth] 公共原始数据区
│   └── avatar/       # 公共文件：仅供上传写入，不对外直接暴露
│
├── Vault/            # [Private Storage] 私有原始数据区 🔒
│   └── contract/     # 私有文件：需要token才能访问
│
├── ClearExif/        # [Privacy Layer] 隐私清洗区 (缓存)
│   ├── Workspace/    # 公共文件的EXIF清理副本
│   │   └── avatar/
│   └── Vault/        # 私有文件的EXIF清理副本
│       └── contract/
│
└── Compressed/       # [Cache Layer] 缩略图区 (缓存)
    ├── Workspace/    # 公共文件的压缩副本
    │   └── avatar/
    └── Vault/        # 私有文件的压缩副本
        └── contract/
```

### 2. 路径翻译机制

`StorageService` 作为一个 **智能网关**，将用户定义的逻辑路径映射到不同的物理区域，实现“透明化安全保护”。

**公共文件（工作区）：**

| 用户请求（API） | 逻辑路径（内部） | 实际物理操作（物理） | 说明 |
| --- | --- | --- | --- |
| **上传** | `avatar/img.png` | 写入 `/data/Workspace/avatar/img.png` | 原始文件存入但永不流出 |
| **下载原始文件** | `avatar/img.png` | 读取自 `/data/ClearExif/Workspace/avatar/img.png` | 自动清除隐私信息 |
| **下载缩略图** | `avatar/img.png?w=200` | 读取自 `/data/Compressed/Workspace/avatar/img_w200.png` | 自动压缩以实现更快的传输速度 |

**私有文件（保险库）：**

| 用户请求 (API) | 逻辑路径 (内部) | 实际物理操作 (物理) | 备注 |
| --- | --- | --- | --- |
| **上传** | `contract/doc.pdf` | 写入 `/data/Vault/contract/doc.pdf` | 与公共存储隔离 |
| **下载** | `contract/doc.pdf` | 读取 `/data/Vault/contract/doc.pdf` | 需有效令牌 |
| **下载图片** | `contract/scan.jpg` | 读取 `/data/ClearExif/Vault/contract/scan.jpg` | 令牌 + EXIF 清除 |
| **下载缩略图** | `contract/scan.jpg?w=200` | 读取 `/data/Compressed/Vault/contract/scan_w200.jpg` | 令牌 + 压缩 |

## 🧩 核心服务参考

* **StorageService**: 核心网关，负责路径映射、文件存储、令牌生成/验证以及访问控制检查。
* **ImageProcessingService**: 处理公共文件和私有文件的图像压缩、隐私信息移除及格式验证。
* **FeatureFoldersProvider**: (内部) 配置源，管理物理目录结构（Workspace、Vault、ClearExif、Compressed）。
* **FilesController**: 提供统一的上传和下载端点：
  - `/upload/{subfolder}?useVault=false` - 公共文件上传
  - `/upload/{subfolder}?useVault=true` - 私有文件上传
  - `/download/**` - 公共文件下载
  - `/download-private/**?token=xxx` - 带令牌验证的私有文件下载

---

## 🔑 私有文件的基于令牌的安全机制

### 工作原理

1. **令牌生成**：调用 `RelativePathToInternetUrl(path, isVault: true)` 时，系统使用 ASP.NET Core 的 `IDataProtectionProvider` 生成令牌：
   - 文件路径被加密
   - 过期时间戳（生成后60分钟）被嵌入
   - 加密签名防止篡改

2. **令牌格式**：加密后的 base64 编码字符串（由 DataProtection API 处理）

3. **令牌验证**：在下载请求时，系统会自动验证：
   - 令牌未过期
   - 令牌未被篡改
   - 请求的路径与令牌中授权的路径匹配

### 密钥管理

**无需配置！** 系统使用 ASP.NET Core 内置的 `DataProtection` API，该 API 自动执行：
- 生成和管理加密密钥
- 将密钥安全地持久化到磁盘
- 自动处理密钥轮换
- 在应用程序重启后提供安全的密钥存储

> **注意**：在生产环境中，密钥会自动存储在应用程序的数据目录中。对于分布式部署（多台服务器），您可能希望使用标准 DataProtection 配置来配置共享的密钥存储位置。

### 代码方式生成令牌

如果需要在后端代码中生成下载令牌：

```csharp
public class DocumentService
{
    private readonly StorageService _storage;
    
    public string GetSecureDownloadUrl(string logicalPath)
    {
        // Generates a time-limited, encrypted URL
        return _storage.RelativePathToInternetUrl(logicalPath, isVault: true);
    }
}
```