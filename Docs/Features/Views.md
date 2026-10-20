This is the core document about the **Aiursoft Template View Rendering Mechanism**.

In standard ASP.NET Core development, `return View()` is the norm. However, in Aiursoft Template, this is a **anti-pattern**.

-----

# 🚫 Stop Using `return View()`: Understanding the View Injection Mechanism

In the Aiursoft Template architecture, the `Layout` (layout file) is no longer a mere empty shell that blindly displays HTML. It is a highly intelligent component that requires a substantial amount of context data (user information, avatar, dark mode preference, menu tree after permission verification, multi-language configuration, etc.) to function properly.

If you habitually write `return View(model)`, your page will "break": no sidebar, no navigation, avatars won't display, and even theme colors may be incorrect.

## Core Principle

**Never directly call `return View()`**.

Instead, choose one of the following two alternatives based on the scenario:

1.  **`return this.StackView(model)`**: Use for standard business pages (with sidebar, navigation, footer).
2.  **`return this.SimpleView(model)`**: Use for standalone pages (login, registration, error pages).

-----

## 🛠️ Why? What Happens?

When you call the standard `return View(model)`, you only pass your own business data. **The `Sidebar`, `Navbar`, `Theme`, and other required components are all `null`**.

### Correct Flow: Inject (Injection)

Aiursoft Template introduces the `ViewModelArgsInjector` service. When you call `StackView` or `SimpleView`, the controller performs extensive behind-the-scenes work:

1.  **Retrieve `ViewModelArgsInjector` from the DI container.**
2.  **Automatically populate global data**: It determines who the current user is and what their avatar is.
3.  **Calculate permissions and menu**: It iterates through all menu items and uses `IAuthorizationService` to check whether the current user has permission to view each menu.
4.  **Handle multi-language and theme**: It checks the Cookie to determine whether dark mode or light mode is selected.

Only after this step "Inject" is completed, your model is ready to be rendered.

---

## 1. Scenario One: Standard Business Page (`StackView`)

This is the most commonly used method. Use it when you need a complete backend management interface, console, or dashboard.

**It automatically generates:**
* Left sidebar (menu filtered by user permissions).
* Top navigation bar (includes language switch).
* User dropdown menu (includes avatar and logout link).
* Footer information.

### ✅ Code Example

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

## 2. Scenario Two: Independent/Clean Page (`SimpleView`)

Use this when you need a "clean" canvas. For example: login pages, registration pages, full-screen error messages, or pages like PowerPoint presentation mode that require no navigation distractions.

**It automatically handles:**

  * Page title (PageTitle).
  * Basic CSS/JS references.
  * Theme color (Theme).
  * **Removes** all padding, giving you 100% control.
  * **Does not render** sidebar, navigation bar, or footer.

### ✅ Code Example

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

# ⚠️ Mandatory Rules: ViewModel Inheritance and Initialization

When using `this.StackView()` or `this.SimpleView()`, you might wonder: *“Where does the injector put the sidebar, user information, and other data?”*

The answer is: it goes into the **base class properties of the ViewModel**.

To make this mechanism work properly, every ViewModel you define for a page must follow these two **strict rules**:

## 1. Must Inherit from `UiStackLayoutViewModel`

The Layout file (`Layout.cshtml`) expects the model type to be `UiStackLayoutViewModel`. If your model does not inherit from it, the Razor engine will throw an error during Layout rendering due to missing properties like `Sidebar`, `Navbar`, `Theme`, or the injector will fail to work.

## 2. Must Initialize `PageTitle` in the Constructor

Avoid scattered assignments like `model.PageTitle = "..."` in the Controller's Action. This makes the code hard to maintain.
**Best practice**: The ViewModel should know its own name the moment it is created (in the constructor).

### ✅ Standard Code Example

Please see the following standard implementation:

```csharp
using Aiursoft.UiStack.Layout; // 引用基类命名空间

// 1. 继承 UiStackLayoutViewModel
public class RenderRepoViewModel : UiStackLayoutViewModel
{
    // 2. 在构造函数中强制要求传入或定义 PageTitle
    public RenderRepoViewModel(string repoName)
    {
        // PageTitle 将直接显示在浏览器标签页上 (e.g., "MyRepo | Warp")
        // 也会被注入器用于生成面包屑导航（如果有的话）
        PageTitle = repoName;
    }

    // 你的业务属性
    public required RepoStats Stats { get; init; }
}
```

### ❌ Incorrect example

```csharp
// 错误：没有继承基类，Layout 无法渲染导航栏，Injector 会抛出异常或无效
public class WrongViewModel 
{
    public string PageTitle { get; set; } // 即使你手写了这个属性也没用，基类里有特定逻辑
}

// 错误：在 Controller 里才想起来起名字
public class LazyViewModel : UiStackLayoutViewModel
{
    // 空的构造函数，导致 PageTitle 默认为 null
}

// Controller
public IActionResult Index() 
{
    var model = new LazyViewModel();
    model.PageTitle = "Index"; // 不要这样做！逻辑分散了。
    return this.StackView(model);
}
```

## 💡 Why do this?

1.  **Type Safety**: Inheriting from the base class ensures your model always has everything Layout needs (`Sidebar`, `Navbar`, `Footer`, `Theme`, etc.).
2.  **Single Responsibility**: The Controller is responsible only for fetching data (e.g., fetching `RepoStats` from the database), while the ViewModel is responsible for defining "Who am I?" (e.g., "I am the Repo Detail page").
3.  **Automated Translation**: Remember the code in `ViewModelArgsInjector`?
    ```csharp
    toInject.PageTitle = localizer[toInject.PageTitle ?? "View"];
    ```
    It will read the `PageTitle` you set in the constructor and automatically attempt multilingual translation. If you don't set it, it will only display the default "View", which looks very unprofessional.

Following this convention, your Controller code will become exceptionally clean:

```csharp
[Route("repo/{repoName}")]
public IActionResult Overview(string repoName)
{
    // 实例化时，标题自动确立
    var model = new RenderRepoViewModel(repoName)
    {
        Stats = _repoService.GetStats(repoName)
    };

    // 也就是一行代码的事，所有 UI 组件全部就绪
    return this.StackView(model);
}
```

-----

## ⚡ Summary & Quick Reference

| Feature | `return View()` | `this.SimpleView()` | `this.StackView()` |
| :--- | :---: | :---: | :---: |
| **Business Data** | ✅ Passed | ✅ Passed | ✅ Passed |
| **Page Title** | ❌ Lost | ✅ Auto-translated | ✅ Auto-translated |
| **Theme (Dark/Light)** | ❌ Default | ✅ Auto-detected | ✅ Auto-detected |
| **Sidebar / Menu** | ❌ None | ❌ None (by design) | ✅ **Auto-generated (with permissions)** |
| **Top Navigation** | ❌ None | ❌ None | ✅ **Includes user avatar / language** |
| **Use Cases** | **Do not use** | Login / Registration / Landing Pages | Backend / Dashboard / CRUD |

Remember: **The intelligence of Template lies in `Injector`. Do not bypass it—use it.**