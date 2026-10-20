# File Storage and Upload Development Guidelines

This module utilizes a **"Physically Isolated, Logically Unified"** architectural design, aimed at providing an industry-grade secure file storage solution.

The core design philosophy is the **"Logical Path"**:

* **Frontend/Database/API**: Only handle clean **Logical Paths** (e.g., `avatar/2026/01/14/logo.png`).
* **Backend Underlying**: Automatically maps logical paths to physically isolated storage areas (e.g., `/data/Workspace/...`).

---

## 1. Security Boundary and Development Rules

`<vc:file-upload>` is the recommended browser upload component, not a security boundary. Client-side restrictions can be bypassed; every security decision must be enforced by the server.

### Choose the Upload Path

| Scenario | Recommended implementation | Security responsibility |
| --- | --- | --- |
| Standard browser upload | `<vc:file-upload>` + the common `FilesController` | Enforced by the signed grant and common upload pipeline |
| Chunked upload, client-side encryption, streaming recording, or another special protocol | Dedicated controller | Must provide server-side validation and tests no weaker than the common pipeline |
| Trusted server workflow such as import, transcoding, or a background job | `StorageService.SaveFromStream()` | The caller validates business format and size; `StorageService` enforces the path boundary and write operation |

### Mandatory Rules

1. Treat every external request, file name, logical path, extension, length, and payload as untrusted.
2. Use the common upload pipeline for standard browser uploads. Its signed grant must bind the operation, logical path, Workspace/Vault area, size, extensions, and content-validation policy.
3. A special upload endpoint must limit the request before reading its body and validate identity, authorization, file count, file name, actual length, extension, content, and target storage area on the server.
4. Trusted server streams may be saved directly, but `SaveFromStream()` is not a file-type validator.
5. Store only logical paths in databases and business APIs. Resolve physical files through `StorageService`; never concatenate an untrusted path with the storage root.
6. Generic downloads must use `attachment` and `X-Content-Type-Options: nosniff`. Only re-encoded images or explicitly allowlisted media with a verified file signature may use `inline`.
7. A ViewModel regular expression can restrict a business folder but cannot prove file ownership. Use a user-scoped folder or a persisted upload-ownership record when users must be isolated.

### Prohibited Practices

* Relying only on browser-side extension or size checks.
* Accepting `IFormFile` in an arbitrary business controller and writing it directly to disk.
* Accessing storage with `Path.Combine(storageRoot, untrustedPath)`.
* Returning `inline` based on a user-provided extension or MIME type.

---

## 2. Storage Modes Detailed

This module supports two completely isolated storage modes:

| Feature | Public Files (Workspace) | Private Files (Vault) |
| --- | --- | --- |
| **Storage Location** | `/data/Workspace` | `/data/Vault` (Physically Isolated) |
| **Access Rights** | Publicly accessible via URL | **Valid Token Required** |
| **Token Expiry** | N/A | Default 60 minutes (protected by ASP.NET Core Data Protection) |
| **Use Cases** | Avatars, product images, public docs | ID cards, contracts, invoices, sensitive data |
| **URL Format** | `/download/avatar/.../img.png` | `/download-private/contract/.../doc.pdf?token=...` |
| **Upload Param** | Default (`useVault=false`) | `useVault=true` |

---

## 3. Quick Integration: Four-Step Process

### Step 1: Recommended UI Integration (ViewComponent)

Use the `vc:file-upload` component for standard browser uploads in `.cshtml` pages. A special upload protocol may use another UI, but it must follow the server-side rules above.

**Scenario A: Public Files (e.g., Avatars)**

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

**Scenario B: Private Files (e.g., Contracts)**

> **⚠️ Critical Correction**: You must set `is-vault="true"` AND provide a `subfolder`. The system will automatically generate a secure, time-limited upload token.

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

### Step 2: ViewModel Definition (Logical Path Binding)

The ViewModel receives the **Logical Path String** returned after a successful upload. This is where the first layer of validation (Bucket Locking) occurs.

> **Concept**: A logical path is neither a URL nor a physical path. It identifies a storage location. Logical-path validation prevents cross-feature references, but user-level ownership must still be validated separately.

**For Public Files:**

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

**For Private Files:**

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

### Step 3: Controller Business Logic (Defensive Programming)

**NEVER** trust a string submitted by the frontend. Before saving it to the database, validate the logical path, physical file existence, and the current user's permission to reference that file.

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

### Step 4: Distribution and Download

In Razor views, use `StorageService` to convert logical paths into accessible URLs.

**For Public Files:**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage

<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" alt="User Avatar" />

```

**For Private Files:**

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage

<a href="@Storage.RelativePathToInternetUrl(Model.ContractPath, isVault: true)" 
   download="contract.pdf"
   class="btn btn-secondary">
    Download Contract
</a>

```

> **Important**:
> * For private files, always set `isVault: true`.
> * The system automatically generates a cryptographically signed `?token=...`.
> * Even if the URL is shared, it will expire after 60 minutes.
> 
> 

**Supported Dynamic Parameters (Images Only):**

* `?w=200`: Scale width to 200px (maintains aspect ratio).
* `?square=true`: Center-crop to a square.
* **Default Behavior**: All image requests **automatically strip EXIF metadata** (GPS, camera settings) to protect user privacy.

---

## 4. Architecture Deep Dive

The system divides the disk into four regions, routed transparently via `StorageService`.

### 1. Directory Structure

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

### 2. Path Translation Mechanism

`StorageService` acts as a **Smart Gateway**, mapping logical paths to different physical regions.

**Public Files (Workspace):**

| Request (API) | Logical Path (Internal) | Physical Operation | Notes |
| --- | --- | --- | --- |
| **Upload** | `avatar/img.png` | Write to `/data/Workspace/...` | Original saved but never exposed |
| **Download Raw** | `avatar/img.png` | Read from `/data/ClearExif/...` | Privacy stripped automatically |
| **Download Thumb** | `avatar/img.png?w=200` | Read from `/data/Compressed/...` | Compressed for delivery |

**Private Files (Vault):**

| Request (API) | Logical Path (Internal) | Physical Operation | Notes |
| --- | --- | --- | --- |
| **Upload** | `contract/doc.pdf` | Write to `/data/Vault/...` | Isolated from public storage |
| **Download** | `contract/doc.pdf` | Read from `/data/Vault/...` | **Token Required** |
| **Download Image** | `contract/scan.jpg` | Read from `/data/ClearExif/...` | Token + EXIF stripped |

---

## 5. Token Security Mechanism (Deep Dive)

### How it Works

1. **Generation**: When calling `RelativePathToInternetUrl(path, isVault: true)`, the system uses ASP.NET Core's `IDataProtectionProvider`:
* File path is encrypted.
* An expiry timestamp (60 mins) is embedded.
* A cryptographic signature is added to prevent tampering.


2. **Format**: An encrypted, base64-encoded string.
3. **Validation**: Upon download request, the system verifies:
* Token has not expired.
* Token has not been tampered with.
* The decrypted path matches the requested path (prevents using a token for File A to download File B).



### Programmatic Token Generation

If you need to generate secure URLs in backend code (e.g., for email attachments):

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

## 6. FAQ

**Q: Why does the upload interface (`FilesController`) use a `subfolder` route parameter?**
A: To implement **Bucket Isolation**. Frontend specifies `/upload/avatar`, and the backend saves it under the `.../avatar/` directory. Combined with Regex validation (`^avatar/.*`), this prevents users from uploading a "chat image" and submitting it as an "avatar," eliminating cross-module file reference risks.

**Q: Is EXIF stripping applied only to images?**
A: Yes. Non-image files are returned as `application/octet-stream` with `attachment` and `nosniff` by default. They are never rendered inline from a user-provided extension.

**Q: How do I change the token expiration time?**
A: In the `StorageService.GetToken` method, simply modify the `TimeSpan.FromMinutes(60)` value.
