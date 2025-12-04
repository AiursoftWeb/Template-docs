这是一个关于 **Aiursoft Template 视图渲染机制** 的核心文档。

在标准的 ASP.NET Core 开发中，`return View()` 是常态。但在 Aiursoft Template 中，这是一个**反模式**。

-----

# 🚫 停止使用 `return View()`：理解视图注入机制

在 Aiursoft Template 的架构中，`Layout`（布局文件）不再是一个只会傻傻显示 HTML 的空壳。它是一个高度智能的组件，需要大量上下文数据（用户信息、头像、暗黑模式偏好、权限验证后的菜单树、多语言配置等）才能正常工作。

如果你习惯性地写了 `return View(model)`，你的页面将会“崩坏”：没有侧边栏、没有导航、头像不显示、甚至主题颜色错乱。

## 核心原则

**永远不要直接调用 `return View()`。**

请根据场景，选择以下两种替代方案之一：

1.  **`return this.StackView(model)`**：用于标准业务页面（带侧边栏、导航、页脚）。
2.  **`return this.SimpleView(model)`**：用于独立页面（登录、注册、错误页）。

-----

## 🛠️ 为什么？发生了什么？

让我们看一眼底层的 `Layout.cshtml`。它依赖于一个庞大的 ViewModel —— `UiStackLayoutViewModel`。

````html
<html data-bs-theme="@Model.Theme"> ...
@if (Model.Sidebar != null) { <vc:sidebar ... /> } @if (Model.Navbar != null) { <vc:navbar ... /> }   ```

当你调用标准的 `return View(model)` 时，你只传递了你自己的业务数据。**Layout 所需的这些 `Sidebar`, `Navbar`, `Theme` 全是 `null`。**

### 正确的流程：Inject（注入）

Aiursoft Template 引入了 `ViewModelArgsInjector` 服务。当你调用 `StackView` 或 `SimpleView` 时，控制器会在幕后做大量工作：

1.  **从 DI 容器获取 `ViewModelArgsInjector`。**
2.  **自动填充全局数据**：它会去查当前用户是谁？头像是什么？
3.  **计算权限与菜单**：它会遍历所有菜单项，结合 `IAuthorizationService` 检查当前用户是否有权看到这个菜单。
4.  **处理多语言与主题**：检查 Cookie 确定是深色模式还是浅色模式。

只有经过这一步“填充（Inject）”，你的模型才算准备好被渲染。

---

## 1. 场景一：标准业务页面 (`StackView`)

这是最常用的方法。当你需要一个完整的后台管理界面、控制台或仪表盘时使用。

**它会自动生成：**
* 左侧侧边栏（根据用户权限过滤菜单）。
* 顶部导航栏（包含语言切换）。
* 用户下拉菜单（包含头像、注销链接）。
* 页脚信息。

### ✅ 代码示例

```csharp
[HttpGet]
public IActionResult Index()
{
    var model = new MyDashboardViewModel();
    // ❌ 错误：页面将是一片空白，没有菜单
    // return View(model); 

    // ✅ 正确：自动注入所有 UI 组件
    return this.StackView(model);
}
````

-----

## 2\. 场景二：独立/干净页面 (`SimpleView`)

当你需要一个“干净”的画布时使用。例如：登录页、注册页、全屏错误提示、或者像是 PowerPoint 播放模式那样不需要导航干扰的页面。

**它会自动处理：**

  * 页面标题（PageTitle）。
  * 基础 CSS/JS 引用。
  * 主题颜色（Theme）。
  * **移除**所有边距（Padding），给你 100% 的控制权。
  * **不渲染**侧边栏、导航栏和页脚。

### ✅ 代码示例

```csharp
[HttpGet]
public IActionResult Login()
{
    var model = new LoginViewModel();
    
    // ✅ 正确：只渲染内容，没有多余的菜单干扰
    return this.SimpleView(model);
}
```

-----

## ⚡ 总结与速查表

| 特性 | `return View()` | `this.SimpleView()` | `this.StackView()` |
| :--- | :---: | :---: | :---: |
| **业务数据** | ✅ 传递 | ✅ 传递 | ✅ 传递 |
| **页面标题** | ❌ 丢失 | ✅ 自动翻译 | ✅ 自动翻译 |
| **主题(深/浅)** | ❌ 默认 | ✅ 自动识别 | ✅ 自动识别 |
| **侧边栏/菜单** | ❌ 无 | ❌ 无 (设计如此) | ✅ **自动生成(带权限)** |
| **顶部导航** | ❌ 无 | ❌ 无 | ✅ **包含用户头像/语言** |
| **适用场景** | **禁止使用** | 登录/注册/落地页 | 后台/仪表盘/CRUD |

记住：**Template 的智能在于 `Injector`。不要绕过它，要利用它。**