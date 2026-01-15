# 文件存储与上传子系统集成指南

本模块采用 **“物理隔离、逻辑统一”** 的架构设计，旨在提供工业级的文件安全存储方案。

核心设计哲学是 **“逻辑路径（Logical Path）”**：

* **前端/数据库/API**：仅流转清晰的 **逻辑路径**（例如：`avatar/2026/01/14/logo.png`）。
* **后端底层**：自动映射到物理隔离的存储区域（例如：`/data/Workspace/...`）。

---

## 1. 核心规则 (Strict Rules)

1. **禁止** 使用传统的 HTML `<input type="file">` 控件——这会显著增加工作量，极大扩展攻击面，并阻止访问压缩和隐私净化等高级功能。
2. **禁止** 直接在业务 Controller 中处理 `IFormFile`。所有文件流操作必须由 `FilesController` 统一接管。
3. **禁止** 手动拼接物理路径（如 `Path.Combine(root, path)`）来访问文件——必须使用 `StorageService.GetFilePhysicalPath()` 以利用其内置的防路径遍历检测。

---

## 2. 存储模式详解

本模块支持两种完全隔离的存储模式：

| 特性 | 公开文件 (Public / Workspace) | 私有文件 (Private / Vault) |
| --- | --- | --- |
| **存储位置** | `/data/Workspace` | `/data/Vault` (物理隔离) |
| **访问权限** | 公网可直接访问 | **必须持有有效 Token** |
| **Token时效** | 无 | 默认 60 分钟 (HMAC-SHA256 签名) |
| **适用场景** | 用户头像、产品图片、公开文档 | 身份证、合同、发票、个人私密数据 |
| **URL 格式** | `/download/avatar/.../img.png` | `/download-private/contract/.../doc.pdf?token=...` |
| **上传参数** | 默认 (useVault=false) | `useVault=true` |

---

## 3. 快速集成：四步完成

### 步骤 1：UI 集成 (ViewComponent)

在 `.cshtml` 页面中，使用 `vc:file-upload` 组件。

**场景 A：公开文件（如头像）**

```html
<form asp-action="UpdateProfile" method="post">
    <label>上传头像</label>
    <vc:file-upload 
        asp-for="IconPath" 
        upload-endpoint="/upload/avatar" 
        allowed-extensions="jpg png"
        max-size-in-mb="5">
    </vc:file-upload>

    <button type="submit" class="btn btn-primary">提交</button>
</form>

@* 引入必要的样式和脚本 *@
@section styles {
    <link rel="stylesheet" href="~/node_modules/dropify/dist/css/dropify.min.css" />
    <link rel="stylesheet" href="~/styles/uploader.css" />
}
@section scripts {
    <script src="~/node_modules/dropify/dist/js/dropify.min.js"></script>
}

```

**场景 B：私有文件（如合同）**

> **⚠️ 关键修正**：必须在 `upload-endpoint` 添加 `?useVault=true` 告知上传接口存入 Vault，**同时**设置组件属性 `is-vault="true"`，否则在编辑回显时图片会裂开（403 Forbidden）。

```html
<form asp-action="UpdateContract" method="post">
    <label>上传保密合同</label>
    <vc:file-upload 
        asp-for="ContractPath" 
        upload-endpoint="/upload/contract?useVault=true" 
        is-vault="true"
        allowed-extensions="pdf docx">
    </vc:file-upload>

    <button type="submit" class="btn btn-primary">保存合同</button>
</form>

```

### 步骤 2：ViewModel 定义 (Logic Path Binding)

ViewModel 接收的是上传成功后返回的**逻辑路径字符串**。在此处进行第一道格式校验（Bucket Lock）。

> **概念说明**：逻辑路径既不是 URL 也不是物理路径，而是一种“虚拟路径”。它让系统自动处理存储细节，并有助于防止利用路径漏洞的攻击。

**对于公开文件：**

```csharp
public class UpdateProfileViewModel
{
    [Display(Name = "Avatar file")]
    [Required(ErrorMessage = "The avatar file is required.")]
    [MaxLength(150)]
    // ✅ 安全核心：正则锁定存储桶。
    // 强制要求路径必须以 "avatar/" 开头，防止攻击者提交其他目录下的文件。
    [RegularExpression(@"^avatar/.*", ErrorMessage = "请上传正确的头像文件。")]
    public string? IconPath { get; set; }
}

```

**对于私有文件：**

```csharp
public class UpdateContractViewModel
{
    [Display(Name = "Contract Document")]
    [Required(ErrorMessage = "必须上传合同文件。")]
    [MaxLength(200)]
    // ✅ 安全核心：锁定 contract 目录
    [RegularExpression(@"^contract/.*", ErrorMessage = "非法的文件路径。")]
    public string? ContractPath { get; set; }
}

```

### 步骤 3：Controller 业务处理 (Defensive Programming)

**绝对不要**信任前端提交的字符串。在写入数据库前，必须调用 `StorageService` 进行物理文件校验。

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> UpdateContract(UpdateContractViewModel model)
{
    if (!ModelState.IsValid) return View(model);

    // 1. (关键) 验证文件物理存在性与安全性
    // 这里使用 isVault: true，因为我们预期这是一个私有文件
    try 
    {
        var physicalPath = storageService.GetFilePhysicalPath(model.ContractPath, isVault: true);
        
        // 如果是图片，还可以额外检查 IsValidImageAsync(physicalPath)
        if (!System.IO.File.Exists(physicalPath))
        {
             ModelState.AddModelError(nameof(model.ContractPath), "文件上传失败或已丢失，请重新上传。");
             return View(model);
        }
    }
    catch (ArgumentException) // 捕获路径遍历攻击尝试
    {
        return BadRequest();
    }

    // 2. 业务落库 (仅存储逻辑路径)
    // DB 存储示例: "contract/2026/01/14/uuid.pdf"
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

### 步骤 4：分发与下载

当需要显示文件时，使用 `StorageService` 将其转换为可访问的互联网 URL。

**对于公共文件：**

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
    下载合同
</a>

```

> **重要**：
> * 对于私有文件，务必设置 `isVault: true`。
> * 系统会自动生成一个包含加密签名的 `?token=...`。
> * 即使用户把这个 URL 发给别人，60分钟后也会失效。
> 
> 

**支持的动态参数（仅限图片）：**

* `?w=200`：按比例缩放宽度至 200px。
* `?square=true`：居中裁剪为正方形。
* **默认行为**：所有图像下载请求将**自动移除 EXIF 信息**（GPS、相机设置），保护用户隐私。

---

## 4. 架构深度解析 (Architecture)

本系统将磁盘划分为四个区域，通过 `StorageService` 进行透明路由。

### 1. 目录结构

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

| 用户请求 (API) | 逻辑路径 (内部) | 实际物理操作 (物理) | 说明 |
| --- | --- | --- | --- |
| **上传** | `avatar/img.png` | 写入 `/data/Workspace/avatar/img.png` | 原始文件存入但永不流出 |
| **下载原始文件** | `avatar/img.png` | 读取 `/data/ClearExif/Workspace/avatar/img.png` | 自动清除隐私信息 (Copy on Write) |
| **下载缩略图** | `avatar/img.png?w=200` | 读取 `/data/Compressed/Workspace/avatar/img_w200.png` | 自动压缩以实现更快的传输速度 |

**私有文件（保险库）：**

| 用户请求 (API) | 逻辑路径 (内部) | 实际物理操作 (物理) | 备注 |
| --- | --- | --- | --- |
| **上传** | `contract/doc.pdf` | 写入 `/data/Vault/contract/doc.pdf` | 与公共存储严格隔离 |
| **下载** | `contract/doc.pdf` | 读取 `/data/Vault/contract/doc.pdf` | **需有效令牌** |
| **下载图片** | `contract/scan.jpg` | 读取 `/data/ClearExif/Vault/contract/scan.jpg` | 令牌 + EXIF 清除 |
| **下载缩略图** | `contract/scan.jpg?w=200` | 读取 `/data/Compressed/Vault/contract/scan_w200.jpg` | 令牌 + 压缩 |

---

## 5. Token 安全机制 (Deep Dive)

### 工作原理

1. **令牌生成**：调用 `RelativePathToInternetUrl(path, isVault: true)` 时，系统使用 ASP.NET Core 的 `IDataProtectionProvider` 生成令牌：
* 文件路径被加密
* 过期时间戳（生成后60分钟）被嵌入
* 加密签名防止篡改


2. **令牌格式**：加密后的 base64 编码字符串。
3. **令牌验证**：在下载请求时，系统会自动验证：
* 令牌未过期
* 令牌未被篡改
* 请求的路径与令牌中授权的路径匹配（路径绑定，防止拿A文件的Token下B文件）



### 代码方式生成令牌

如果需要在后端代码中生成下载令牌（例如发送邮件附件链接）：

```csharp
public class DocumentService(StorageService storage)
{
    public string GetSecureDownloadUrl(string logicalPath)
    {
        // 生成一个限时的、加密的完整 URL
        return storage.RelativePathToInternetUrl(logicalPath, isVault: true);
    }
}

```

---

## 6. 常见问题 (FAQ)

**Q: 为什么上传接口 (`FilesController`) 要设计成接收 `subfolder` 路由参数？**
A: 为了实现**存储桶隔离**。前端指定 `/upload/avatar`，后端文件就物理落盘在 `.../avatar/` 目录下。配合 ViewModel 中的正则校验 `^avatar/.*`，可以从根源上防止用户将“聊天图片”上传后伪造成“头像”提交，杜绝了跨业务模块的文件引用风险。

**Q: 只有图片会被清除 EXIF 吗？**
A: 是的。系统会自动检测 MIME 类型和文件头。如果是 PDF 或 ZIP 等非图片文件，会直接流式传输，不进行 ImageSharp 处理。

**Q: 如果我想修改 Token 的过期时间怎么办？**
A: 在 `StorageService.GetDownloadToken` 方法中，修改 `TimeSpan.FromMinutes(60)` 即可。