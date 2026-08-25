# 文件存储与上传开发规范

本模块采用 **“物理隔离，逻辑统一”** 的架构设计，旨在提供业界级别的安全文件存储解决方案。

核心设计理念为 **“逻辑路径”**：

* **前端/数据库/API**：仅处理清晰的 **逻辑路径**（例如：`avatar/2026/01/14/logo.png`）。
* **后端底层**：自动将逻辑路径映射到物理隔离的存储区域（例如：`/data/Workspace/...`）。

---

## 1. 安全边界与开发规则

`<vc:file-upload>` 是推荐的浏览器上传组件，不是安全边界。客户端限制可以被绕过，所有安全判断必须由服务端完成。

### 上传路径选择

| 场景 | 推荐实现 | 安全责任 |
| --- | --- | --- |
| 普通浏览器上传 | `<vc:file-upload>` + 通用 `FilesController` | 由签名 grant 和通用上传管线统一执行 |
| 分片上传、客户端加密、流式录音等特殊协议 | 独立 Controller | 必须实现不弱于通用上传管线的服务端验证和测试 |
| 导入、转码、后台任务等可信服务端流程 | `StorageService.SaveFromStream()` | 调用方负责业务格式和大小验证；`StorageService` 负责路径边界和写入 |

### 强制规则

1. 所有外部请求、文件名、逻辑路径、扩展名、长度和内容都不可信。
2. 普通浏览器上传默认使用通用上传管线。签名 grant 必须绑定操作、逻辑路径、Workspace/Vault、大小、扩展名和内容验证策略。
3. 特殊上传端点必须在读取请求体前限制请求大小，并在服务端验证身份、授权、文件数量、文件名、实际长度、扩展名、内容和目标存储区。
4. 服务端内部流可以直接保存，但不得把 `SaveFromStream()` 当作文件类型验证器。
5. 数据库和业务 API 只保存逻辑路径。访问物理文件必须通过 `StorageService`，禁止手动拼接存储根目录。
6. 通用文件下载必须使用 `attachment` 和 `X-Content-Type-Options: nosniff`。只有重新编码后的图片或经过明确文件头验证的允许媒体才能 `inline`。
7. ViewModel 的正则表达式只能限制业务目录，不能证明文件所有权。涉及用户隔离时，必须使用用户专属目录或持久化的上传归属记录。

### 禁止事项

* 仅依赖浏览器端的扩展名或大小限制。
* 在业务 Controller 中随意接收 `IFormFile` 并直接写盘。
* 使用 `Path.Combine(storageRoot, untrustedPath)` 访问存储文件。
* 根据用户提供的扩展名或 MIME 类型直接返回 `inline`。

---

## 2. 存储模式详解

此模块支持两种完全隔离的存储模式：

| 特性 | 公共文件（工作区） | 私有文件（保险库） |
| --- | --- | --- |
| **存储位置** | `/data/Workspace` | `/data/Vault`（物理隔离） |
| **访问权限** | 通过 URL 公开可访问 | **需要有效令牌** |
| **令牌过期时间** | 不适用 | 默认 60 分钟（ASP.NET Core Data Protection 保护） |
| **使用场景** | 头像、产品图片、公开文档 | 身份证、合同、发票、敏感数据 |
| **URL 格式** | `/download/avatar/.../img.png` | `/download-private/contract/.../doc.pdf?token=...` |
| **上传参数** | 默认值（`useVault=false`） | `useVault=true` |

---

## 3. 快速集成：四步流程

### 步骤 1：推荐的 UI 集成（ViewComponent）

普通浏览器上传应在 `.cshtml` 页面中使用 `vc:file-upload` 组件。特殊上传协议可以使用其他 UI，但必须遵守上一节的服务端规则。

**场景 A：公共文件（例如头像）**

```html
<form asp-action="UpdateProfile" method="post">
    <label>Upload Avatar</label>
    <vc:file-upload 
        asp-for="IconPath" 
        subfolder="avatar" 
        allowed-extensions="jpg png"
        max-size-in-mb="5">
    </vc:file-upload>

    <button type="submit" class="btn btn-primary">Submit</button>
</form>

@* Include necessary styles and scripts *@
@section styles {
    <link rel="stylesheet" href="~/node_modules/dropify/dist/css/dropify.min.css" />
    <link rel="stylesheet" href="~/styles/uploader.css" />
}
@section scripts {
    <script src="~/node_modules/dropify/dist/js/dropify.min.js"></script>
}

```

**场景 B：私有文件（例如：合同）**

> **⚠️ 重要修正**：您必须设置 `is-vault="true"` 并提供一个 `subfolder`。系统将自动生成一个安全的、限时的上传令牌。

```html
<form asp-action="UpdateContract" method="post">
    <label>Upload Confidential Contract</label>
    <vc:file-upload 
        asp-for="ContractPath" 
        subfolder="contract" 
        is-vault="true"
        allowed-extensions="pdf docx">
    </vc:file-upload>

    <button type="submit" class="btn btn-primary">Save Contract</button>
</form>

```

### 步骤 2：ViewModel 定义（逻辑路径绑定）

ViewModel 接收上传成功后返回的 **逻辑路径字符串**。这是第一层验证（存储桶锁定）发生的位置。

> **概念**：逻辑路径既不是 URL 也不是物理路径；它是一个表示存储位置的虚拟路径。逻辑路径验证可以防止跨业务目录引用，但用户级所有权仍需单独验证。

**对于公开文件：**

```csharp
public class UpdateProfileViewModel
{
    [Display(Name = "Avatar file")]
    [Required(ErrorMessage = "The avatar file is required.")]
    [MaxLength(150)]
    // ✅ Security Core: Lock the bucket via Regex.
    // Forces the path to start with "avatar/", preventing submission of files from other directories.
    [RegularExpression(@"^avatar/.*", ErrorMessage = "Please upload a valid avatar file.")]
    public string? IconPath { get; set; }
}

```

**对于私人文件：**

```csharp
public class UpdateContractViewModel
{
    [Display(Name = "Contract Document")]
    [Required(ErrorMessage = "Contract file is required.")]
    [MaxLength(200)]
    // ✅ Security Core: Lock to the contract directory
    [RegularExpression(@"^contract/.*", ErrorMessage = "Invalid file path.")]
    public string? ContractPath { get; set; }
}

```

### 第三步：控制器业务逻辑（防御性编程）

**绝对不要**信任前端提交的字符串。在保存到数据库之前，必须验证逻辑路径、物理文件是否存在以及当前用户是否拥有引用该文件的权限。

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> UpdateContract(UpdateContractViewModel model)
{
    if (!ModelState.IsValid) return View(model);

    // 1. (Critical) Validate physical existence and security
    // We use isVault: true as this is expected to be a private file
    try 
    {
        var physicalPath = storageService.GetFilePhysicalPath(model.ContractPath, isVault: true);
        
        // If it's an image, you can additionally check: await imageCompressor.IsValidImageAsync(physicalPath)
        if (!System.IO.File.Exists(physicalPath))
        {
             ModelState.AddModelError(nameof(model.ContractPath), "File upload failed or missing. Please re-upload.");
             return View(model);
        }
    }
    catch (ArgumentException) // Catch path traversal attack attempts
    {
        return BadRequest();
    }

    // 2. Persist to Database (Store only the Logical Path)
    // DB Entry Example: "contract/2026/01/14/uuid.pdf"
    var contract = new Contract 
    { 
        FilePath = model.ContractPath,
        UploaderId = User.Identity.Name 
    };
    
    _dbContext.Contracts.Add(contract);
    await _dbContext.SaveChangesAsync();

    return RedirectToAction(nameof(Index));
}

```

### 第4步：分发与下载

在Razor视图中，使用 `StorageService` 将逻辑路径转换为可访问的URL。

**对于公开文件：**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage

<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" alt="User Avatar" />

```

**对于私有文件：**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage

<a href="@Storage.RelativePathToInternetUrl(Model.ContractPath, isVault: true)" 
   download="contract.pdf"
   class="btn btn-secondary">
    Download Contract
</a>

```

> **重要**：
> * 对于私有文件，始终设置 `isVault: true`。
> * 系统会自动生成一个经过密码学签名的 `?token=...`。
> * 即使 URL 被分享，也将在 60 分钟后过期。
> 
> 

**支持的动态参数（仅限图片）：**

* `?w=200`：将宽度缩放至 200px（保持宽高比）。
* `?square=true`：居中裁剪为正方形。
* **默认行为**：所有图片请求 **自动移除 EXIF 元数据**（GPS 信息、相机设置），以保护用户隐私。

---

## 4. 架构深度解析

系统将磁盘划分为四个区域，通过 `StorageService` 透明路由。

### 1. 目录结构

```text
/data (Storage Root)
├── Workspace/        # [Source of Truth] Public raw data area
│   └── avatar/       # Public files: Upload-only, not directly exposed
│
├── Vault/            # [Private Storage] Private raw data area 🔒
│   └── contract/     # Private files: Token required for access
│
├── ClearExif/        # [Privacy Layer] Privacy sanitization (Cache)
│   ├── Workspace/    # EXIF-cleared copies for public files
│   └── Vault/        # EXIF-cleared copies for private files
│
└── Compressed/       # [Cache Layer] Thumbnail area (Cache)
    ├── Workspace/    # Compressed copies for public files
    └── Vault/        # Compressed copies for private files

```

### 2. 路径翻译机制

`StorageService` 作为**智能网关**，将逻辑路径映射到不同的物理区域。

**公共文件（Workspace）：**

| 请求（API） | 逻辑路径（内部） | 物理操作 | 说明 |
| --- | --- | --- | --- |
| **上传** | `avatar/img.png` | 写入 `/data/Workspace/...` | 原始文件保存但永不暴露 |
| **下载原始文件** | `avatar/img.png` | 读取自 `/data/ClearExif/...` | 隐私信息自动清除 |
| **下载缩略图** | `avatar/img.png?w=200` | 读取自 `/data/Compressed/...` | 压缩后传输 |

**私有文件（Vault）：**

| 请求（API） | 逻辑路径（内部） | 物理操作 | 说明 |
| --- | --- | --- | --- |
| **上传** | `contract/doc.pdf` | 写入 `/data/Vault/...` | 与公共存储隔离 |
| **下载** | `contract/doc.pdf` | 读取自 `/data/Vault/...` | **需要令牌** |
| **下载图片** | `contract/scan.jpg` | 读取自 `/data/ClearExif/...` | 需要令牌且 EXIF 信息已清除 |

---

## 5. Token 安全机制（深入解析）

### 工作原理

1. **生成**：调用 `RelativePathToInternetUrl(path, isVault: true)` 时，系统使用 ASP.NET Core 的 `IDataProtectionProvider`：
* 文件路径被加密。
* 嵌入过期时间戳（60 分钟）。
* 添加加密签名以防止篡改。

2. **格式**：加密后的 base64 编码字符串。
3. **验证**：在下载请求时，系统会验证：
* Token 未过期。
* Token 未被篡改。
* 解密后的路径与请求的路径匹配（防止使用 File A 的 Token 下载 File B）。

### 程序化 Token 生成

如果需要在后端代码中生成安全 URL（例如，用于邮件附件）：

```csharp
public class DocumentService(StorageService storage)
{
    public string GetSecureDownloadUrl(string logicalPath)
    {
        // Generates a time-limited, encrypted full URL
        return storage.RelativePathToInternetUrl(logicalPath, isVault: true);
    }
}

```

---

## 6. 常见问题

**Q: 为什么上传接口（`FilesController`）使用 `subfolder` 路由参数？**
A: 为了实现 **存储桶隔离**。前端指定 `/upload/avatar`，后端将其保存在 `.../avatar/` 目录下。结合正则验证（`^avatar/.*`），可防止用户上传“聊天图片”并提交为“头像”，从而消除跨模块文件引用的风险。

**Q: EXIF 数据剥离是否仅应用于图片？**
A: 是的。非图片文件默认以 `application/octet-stream`、`attachment` 和 `nosniff` 返回，不会根据用户提供的扩展名以内联方式渲染。

**Q: 如何修改令牌过期时间？**
A: 在 `StorageService.GetToken` 方法中，只需修改 `TimeSpan.FromMinutes(60)` 的值即可。
