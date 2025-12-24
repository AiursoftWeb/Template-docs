# 文件存储与上传

本模块旨在让文件上传变得**极度简单**。无需复杂的流处理，无需关心物理路径，**只需要处理一个字符串路径**。

## 1. 极速上手 (Quick Start)

三步即可完成文件上传功能：**放控件 -> 绑模型 -> 存数据库**。

### 第一步：View (放控件)

在你的 `.cshtml` 页面中，使用 `vc:file-upload` 组件。

```html
<form asp-action="UpdateProfile" method="post">
    <!-- 1. 绑定你的 ViewModel 属性 -->
    <!-- 2. 指定上传到的"桶" (upload-endpoint) -->
    <vc:file-upload 
        asp-for="IconPath" 
        upload-endpoint="/upload/avatar" 
        allowed-extensions="jpg png">
    </vc:file-upload>

    <button type="submit">提交</button>
</form>
```

### 第二步：ViewModel (绑模型)

在 ViewModel 中，只需要定义一个 `string` 类型的属性来接收上传后的路径。

```csharp
public class UpdateProfileViewModel
{
    // 这里存的只是路径字符串，例如 "avatar/2025/01/01/xxx.jpg"
    [Required] // 必填校验
    public string IconPath { get; set; }
}
```

### 第三步：Controller (存数据库)

在 Controller 中，像处理普通文本一样处理这个路径。

```csharp
[HttpPost]
public async Task<IActionResult> UpdateProfile(UpdateProfileViewModel model)
{
    if (!ModelState.IsValid) return View(model);

    var user = await _userManager.GetUserAsync(User);
    
    // 直接把路径字符串存入数据库即可
    user.IconPath = model.IconPath; 
    
    await _userManager.UpdateAsync(user);
    return RedirectToAction(nameof(Index));
}
```

**完成！** 你已经实现了文件上传、自动存储、和业务关联。

---

## 2. 进阶：约束与校验

为了保证安全和数据的规范性，建议加上以下约束。

### 2.1 锁定上传目录 (Bucket Isolation)
防止用户把发票上传到头像的目录里。

在 ViewModel 中使用正则限制路径的前缀：

```csharp
public class UpdateProfileViewModel
{
    [Required]
    [Display(Name = "User Icon")]
    // 强制要求路径必须以 Workspace/avatar 开头
    [RegularExpression(@"^Workspace/avatar.*", ErrorMessage = "请上传正确的头像文件。")]
    public string IconPath { get; set; }
}
```

### 2.2 扩展名与大小限制

*   **前端限制**：在 View 组件上设置。
    ```html
    <vc:file-upload ... allowed-extensions="jpg png pdf" max-size-in-mb="10" />
    ```
*   **后端限制**：在 ViewModel 或 Controller 中进一步校验（组件已内置基础校验）。

---

## 3. 文件展示

图片存进去了，怎么显示出来？使用 `StorageService`。

```html
@inject Aiursoft.Template.Services.FileStorage.StorageService Storage

<!-- 自动转换为可访问的 HTTP URL -->
<img src="@Storage.RelativePathToInternetUrl(Model.IconPath)" />
```

### 隐私与裁剪

支持在 URL 后加参数进行实时处理：
*   `?w=200`: 缩放到 200px 宽。
*   `?square=true`: 自动裁剪正方形。
*   **隐私保护**：所有通过此方式访问的图片，都会**自动清除 EXIF 信息** (GPS、相机参数等)，保护用户隐私。

---

## 4. 核心原理 (Understanding)

为什么这么简单？因为采用了 **"两步走 (Two-Step)"** 策略：

1.  **上传 (Upload)**: 此过程与业务无关。用户选文件 -> 传到临时的文件服务器 -> 拿到一个路径字符串 (e.g. `Workspace/avatar/2025/...`)。
2.  **提交 (Submit)**: 用户点击保存按钮，只是把这个**字符串**也就是路径，作为一个普通字段提交给了你的业务 Controller。

## 高级设计细节

上面的内容已经可以支撑你构建一个完善的文件存储了。但是，一个文件存储为了安全、可靠、可组织、避免黑客耗尽磁盘空间，我们仍然需要讨论大量细节。

如果你需要高级开发技巧，请阅读完整的 [文件存储设计细节](./FileStorage.md)。