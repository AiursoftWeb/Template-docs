# Aiursoft Template Tutorial - Step 3 - 添加全新的页面

![home-convert](./assets/home-convert.png)

在上一步，我们成功地添加了将 markdown 转换为 HTML 的功能。接下来，我们需要创建一个前端页面，让用户能够输入 markdown 并预览生成的 HTML。

## Step 3.1 修改将必要的服务添加到依赖注入容器中

ASP.NET Core 使用依赖注入来管理应用的服务。为了让 Markdig 和 HtmlSanitizer 能够在应用中使用，我们需要将它们添加到依赖注入容器中。

首先，修改 `./src/MyOrg.MarkToHtml/Startup.cs` 文件，首先添加必要的 using 语句：

```csharp title="添加 using 语句，Startup.cs"
using Ganss.Xss;
using Markdig;
```

然后找到 `public void ConfigureServices(IConfiguration configuration, IWebHostEnvironment environment, IServiceCollection services)` 方法，添加下面的代码：

```csharp title="配置依赖注入，Startup.cs"
// Add the markdown pipeline and HTML sanitizer
var pipeline = new MarkdownPipelineBuilder().UseAdvancedExtensions().Build();
services.AddSingleton(pipeline);
services.AddSingleton<HtmlSanitizer>();
```

## Step 3.2 写一个全新的转换服务

为了更好地组织代码，我们将创建一个新的服务类，专门负责将 markdown 转换为 HTML。这样可以让代码更加模块化，易于维护。

所有的服务类都应该放在 `./src/MyOrg.MarkToHtml/Services/` 目录下。

在这里新建一个名为 `MarkToHtmlService.cs` 的文件，并添加以下代码：

```csharp title="MarkToHtmlService.cs"
using Aiursoft.Scanner.Abstractions;
using Ganss.Xss;
using Markdig;

namespace MyOrg.MarkToHtml.Services;

public class MarkToHtmlService(MarkdownPipeline pipeline, HtmlSanitizer sanitizer) : ITransientDependency
{
    public string ConvertMarkdownToHtml(string markdown)
    {
        // Use the pre-built, singleton instances. No more 'new' keywords!
        var html = Markdown.ToHtml(markdown, pipeline);
        var outputHtml = sanitizer.Sanitize(html);
        return outputHtml;
    }
}
```

注意，在这里我们给服务实现了接口: `ITransientDependency`。这表示这个服务是瞬态的，每次请求都会创建一个新的实例。Aiursoft Scanner 会自动将实现了这个接口的类注册到依赖注入容器中，无需修改 `Startup.cs` 文件。

同样的，我们在构造方法中索要了 `MarkdownPipeline` 和 `HtmlSanitizer` 的实例。因为我们在 `Startup.cs` 文件中已经将它们注册为单例，所以这里会自动注入同一个实例。

!!! tip "关于依赖注入的生命周期"

    * Singleton 的服务在整个应用生命周期内只会创建一个实例，适用于无状态且线程安全的服务。它只能依赖其它 Singleton 的服务。不可以依赖 Scoped 或 Transient 的服务。
    * Scoped 的服务在每个请求的生命周期内创建一个实例，适用于需要在请求间保持状态的服务。它可以依赖 Singleton 和 Scoped 的服务。不可以依赖 Transient 的服务。
    * Transient 的服务每次请求都会创建一个新的实例，适用于轻量级且无状态的服务。它可以依赖任何类型的服务，包括 Singleton、Scoped 和 Transient。

    打破上面的规则，应用仍然可以编译，甚至某些情况下可能可以运行；但容易产生非常诡异的生命周期问题，导致难以调试的 bug。

因此，在这里我们将 `MarkdownPipeline` 和 `HtmlSanitizer` 注册为 Singleton，因为它们是黑盒，又线程安全，还可以反复使用也就是无状态的。而 `MarkToHtmlService` 则注册为 Transient，因为构造它开销较小且无状态。

## Step 3.3 修改 ViewModel

为了让前端页面能够与后端服务进行交互，我们需要一个 ViewModel。ViewModel 是一种设计模式，用于将数据从控制器传递到视图。

在这里，为了简单，我们直接修改 `./src/MyOrg.MarkToHtml/Models/HomeViewModels/IndexViewModel.cs` 文件，添加一个新的属性 `MarkdownInput` 来存储用户输入的 markdown 内容，并将 `OutputHtml` 属性用于存储生成的 HTML 内容。

```csharp title="IndexViewModel.cs"
using System.ComponentModel.DataAnnotations;
using Aiursoft.UiStack.Layout;

namespace MyOrg.MarkToHtml.Models.HomeViewModels;

public class IndexViewModel : UiStackLayoutViewModel
{
    public IndexViewModel()
    {
        PageTitle = "Markdown to HTML Converter";
    }

    [Required(ErrorMessage = "Please input your markdown content!")]
    public string InputMarkdown { get; set; } = """
                                                # Hello world!

                                                > Quote

                                                [Link](https://www.aiursoft.com/)

                                                | Month    | Savings |
                                                | -------- | ------- |
                                                | January  | $250    |
                                                | February | $80     |
                                                | March    | $420    |

                                                """;

    public string OutputHtml { get; set; } = string.Empty;
}
```

注意，这里的 `[Required]` 特性表示 `InputMarkdown` 属性是必填的。如果用户没有输入任何内容，表单提交时会显示一个错误消息。如果用户强制通过 HTTP Post 提交，则服务器端的 `ModelState.IsValid` 会返回 false。

## Step 3.4 修改 Controller

Controller，也叫控制器，是 MVC 模式中的 C，负责处理用户的请求并返回响应。在我们的结构中，Controller 不会直接负责渲染视图，而是将数据传递给视图模型 (ViewModel)，然后由视图模型来渲染页面。

我们需要修改 `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` 文件，添加对 `MarkToHtmlService` 的依赖注入，并在 `Index` 方法中使用这个服务将用户输入的 markdown 转换为 HTML。

修改其构造函数，添加 `MarkToHtmlService` 的参数：

```csharp title="修改 HomeController 构造函数"
public class HomeController(
    MarkToHtmlService mtohService) : Controller
```

接下来，修改 `Index` 方法的 `GET` 方法的 `[RenderInNavBar]` 特性，确保它的名称已经修改为 "Convert Document"：

```csharp title="修改 HomeController 的 Index 方法的 RenderInNavBar 特性"
[RenderInNavBar(
NavGroupName = "Features",
NavGroupOrder = 1,
CascadedLinksGroupName = "Home",
CascadedLinksIcon = "home",
CascadedLinksOrder = 1,
LinkText = "Convert Document",
LinkOrder = 1)]
```

然后**增加**一个新的 `Index` 方法来处理 POST 请求，将输入的 markdown 转换为 HTML：

```csharp title="添加 Index POST 方法"
[HttpPost]
[ValidateAntiForgeryToken]
public IActionResult Index(IndexViewModel model)
{
    // If the model state is invalid, return the view with the current model to show validation errors
    if (!ModelState.IsValid)
    {
        return this.StackView(model);
    }

    // Convert the input markdown to HTML using the MarkToHtmlService
    model.OutputHtml = mtohService.ConvertMarkdownToHtml(model.InputMarkdown);
    return this.StackView(model);
}
```

!!! tip "Aiursoft Template 特有的返回视图方式"

    Aiursoft Template 要求所有返回视图时，均使用 `this.StackView(model)` 方法来返回视图，而不是直接使用 `return View(model)`。这是因为 `StackView` 方法会自动处理一些 Aiursoft UiStack 相关的逻辑，例如导航栏、布局等。

其中，`[HttpPost]` 特性表示这个方法只处理 POST 请求，`[ValidateAntiForgeryToken]` 特性用于防止跨站请求伪造 (CSRF) 攻击。ASP.NET Core 的表单在提交时会自动包含一个防伪令牌，服务器端会验证这个令牌以确保请求的合法性。

此时，我们的 `HomeController.cs` 文件应该类似于下面这样：

```csharp title="完整的 HomeController.cs"
using MyOrg.MarkToHtml.Models.HomeViewModels;
using MyOrg.MarkToHtml.Services;
using Aiursoft.UiStack.Navigation;
using Microsoft.AspNetCore.Mvc;

namespace MyOrg.MarkToHtml.Controllers;

public class HomeController(
    MarkToHtmlService mtohService) : Controller
{
    [RenderInNavBar(
        NavGroupName = "Features",
        NavGroupOrder = 1,
        CascadedLinksGroupName = "Home",
        CascadedLinksIcon = "home",
        CascadedLinksOrder = 1,
        LinkText = "Convert Document",
        LinkOrder = 1)]
    public IActionResult Index()
    {
        return this.StackView(new IndexViewModel());
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Index(IndexViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return this.StackView(model);
        }

        model.OutputHtml = mtohService.ConvertMarkdownToHtml(model.InputMarkdown);
        return this.StackView(model);
    }
}
```

!!! tip "[RenderInNavBar] 的高级技巧"

    `[RenderInNavBar]` 属性有很多参数，可以帮助你更好地组织导航栏。

    它有三重等级，第一级是始终展开的，多个标签的组，称作 `NavGroup`。
    
    第二级是可以折叠的，多个标签的组，称作 `CascadedLinksGroup`。它是唯一具有图标的一个层级。会展现为一个可折叠的菜单。用户点击图标或名称即可展开或折叠它。
    
    第三级是具体的链接，称作 `Link`。

    而 `Order` 则用于控制它们在同一级别中的排序。数字越小，排序越靠前。例如，我们将 `Roles` 放在了 `Administration` 组下的 `Directory` 组中，并且将它的顺序设置为 `2`，这样它就会排在 `Users` 的后面。

    ```csharp
    // Users management
    [RenderInNavBar(
    NavGroupName = "Administration",
    NavGroupOrder = 9999,
    CascadedLinksGroupName = "Directory",
    CascadedLinksIcon = "users",
    CascadedLinksOrder = 9998,
    LinkText = "Users",
    LinkOrder = 1)]

    // Roles management
    [RenderInNavBar(
    NavGroupName = "Administration",
    NavGroupOrder = 9999,
    CascadedLinksGroupName = "Directory",
    CascadedLinksIcon = "users",
    CascadedLinksOrder = 9998,
    LinkText = "Roles",
    LinkOrder = 2)]
    ```

## Step 3.5 修改视图

视图 (View) 是 MVC 模式中的 V，负责渲染用户界面。在我们的结构中，视图使用 Razor 语法来生成 HTML 页面。

!!! note "视图使用 Razor 语法"

    Razor 是一种基于 C# 的模板引擎，允许你在 HTML 中嵌入 C# 代码。它的文件扩展名通常是 `.cshtml`。Razor 语法非常灵活，可以让你轻松地将服务器端的数据渲染到客户端页面。

    强烈建议在继续之前，补习基础的 [Razor 语法](https://learn.microsoft.com/en-us/aspnet/core/mvc/views/razor)。

显然，视图的职责是绘制一个好看的页面，让用户能够输入 markdown 并预览生成的 HTML。

在我们编写视图的时候，只需要尊重 ViewModel 的属性即可。视图文件位于 `./src/MyOrg.MarkToHtml/Views/Home/Index.cshtml`。在默认情况下，它可能包含了一些示例内容。可以放心的直接删除，然后进行修改。

将其修改为以下内容：

```html title="Index.cshtml"
@using MyOrg.MarkToHtml.Controllers
@model MyOrg.MarkToHtml.Models.HomeViewModels.IndexViewModel

<div class="row mb-2 mb-xl-3">
    <div class="col-auto d-none d-sm-block">
        <h3>@Localizer["Markdown to HTML Converter"]</h3>
    </div>
    <div class="col-auto ms-auto text-end mt-n1">
        <p class="mb-0 text-muted">@Localizer["A simple tool to convert your Markdown into clean, sanitized HTML."]</p>
    </div>
</div>

<form asp-action="Index" method="post" id="markdown-form">
    <div class="row">
        @* Left Column: Markdown Input *@
        <div class="col-lg-6 d-flex">
            <div class="card flex-fill">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="align-middle" data-lucide="markdown">&nbsp;</i>
                        @Localizer["Markdown Input"]
                    </h5>
                </div>
                <div class="card-body p-2">
                    <textarea asp-for="InputMarkdown" class="form-control" id="markdown-editor"
                              placeholder="@Localizer["Type your Markdown here..."]"></textarea>
                    <span asp-validation-for="InputMarkdown" class="text-danger"></span>
                </div>
            </div>
        </div>

        @* Right Column: Standalone Tab Component *@
        <div class="col-lg-6 d-flex flex-column">
            @* The tab component now stands alone and fills the available space *@
            <div class="tab flex-grow-1">
                <ul class="nav nav-tabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        @* The 'active' class is now on the link (<a>), not the list item (<li>) *@
                        <a class="nav-link active" href="#code" data-bs-toggle="tab" role="tab" aria-selected="true">
                            <i class="align-middle" data-lucide="code-2">&nbsp;</i>
                            @Localizer["Code"]
                        </a>
                    </li>
                    <li class="nav-item" role="presentation">
                        <a class="nav-link" href="#preview" data-bs-toggle="tab" role="tab" aria-selected="false">
                            <i class="align-middle" data-lucide="eye">&nbsp;</i>
                            @Localizer["Preview"]
                        </a>
                    </li>
                </ul>
                <div class="tab-content pt-3">
                    @* Code Pane *@
                    <div class="tab-pane active show" id="code" role="tabpanel">
                        <button type="button" id="copy-button" class="btn btn-outline-primary mb-2" title="@Localizer["Copy HTML to clipboard"]">
                            <i class="align-middle" data-lucide="copy"></i> @Localizer["Copy"]
                        </button>
                        <textarea class="form-control" rows="25" id="html-output" readonly>@Model.OutputHtml</textarea>
                    </div>
                    @* Preview Pane *@
                    <div class="tab-pane" id="preview" role="tabpanel">
                        @if (!string.IsNullOrEmpty(Model.OutputHtml))
                        {
                            <button type="button" id="print-button" class="btn btn-outline-info mb-2" title="@Localizer["Print Preview"]">
                                <i class="align-middle" data-lucide="printer"></i> @Localizer["Print"]
                            </button>

                            <div id="printable-area">
                                @Html.Raw(Model.OutputHtml)
                            </div>
                        }
                        else
                        {
                            <div class="text-center p-5">
                                <p class="text-muted">@Localizer["HTML preview will appear here after conversion."]</p>
                            </div>
                        }
                    </div>
                </div>
            </div>
        </div>
    </div>

    @* Submit Button Row *@
    <div class="row mt-3">
        <div class="col text-center">
            <button type="submit" class="btn btn-primary btn-lg">
                <i class="align-middle" data-lucide="chevrons-right">&nbsp;</i>
                @Localizer["Convert to HTML"]
            </button>
        </div>
    </div>
</form>
```

在上面的例子中，我们使用了大量 Razor 的技巧来动态生成 HTML 页面。

例如：`@* Something *@` 用于添加注释；`@model` 用于指定视图使用的 ViewModel 类型，从而可以通过 `@Model.Something` 来访问 ViewModel，`@inject` 用于注入服务，`@Localizer["Some Text"]` 用于本地化字符串，`@Html.Raw(Model.OutputHtml)` 用于渲染未经编码的 HTML 内容。

!!! example "Razor 语法中的 C# 代码块 - 服务器端渲染"

    当然，你也可以继续使用熟悉的 C# 语法来动态渲染，例如 `@if`、`@for`、`@foreach` 等等。这种技巧可以让你轻松地将服务器端的数据渲染到客户端页面。但注意：它会在服务器端执行，将 C# 变量的值插入到生成的 HTML 中，再将其发送到客户端执行。相当于是使用 C# 在动态拼接 HTML，这种技巧叫作“服务器端渲染”，其优先级高于 JavaScript，可以在没有 JavaScript 的情况下运行；但缺点是无法在前端动态改变，并且会占用服务器的算力。

在后面的例子中，我们将大量使用这种技巧来渲染页面。

## Step 3.6 添加必要的样式和脚本

显然，上面的视图只能完成最基本的编辑和预览功能。其中复制按钮、打印按钮、代码高亮等功能都需要额外的样式和脚本来支持。

首先，还记得我们曾经安装 `codemirror` 吗？我们现在需要将它引入到页面中。

在上面的视图文件的末尾，添加以下代码：

```html title="为 Index.cshtml 添加样式"
@{
    var isDarkMode = Context.Request.Cookies[ThemeController.ThemeCookieKey] == true.ToString();
    var theme = isDarkMode ? "material" : "eclipse";
}

@* ReSharper disable once Razor.SectionNotResolved *@
@section styles {
    <link rel="stylesheet" href="~/node_modules/codemirror/lib/codemirror.css"/>
    <link rel="stylesheet" href="~/node_modules/codemirror/theme/@(theme).css" />
    <style>
        .CodeMirror, #preview {
            max-height: 70vh;
        }
        #preview {
            overflow-y: auto;
        }
        .CodeMirror {
            border: 1px solid #dee2e6;
            height: auto;
            display: flex;
            flex-direction: column;
        }
        .CodeMirror-scroll {
            flex-grow: 1;
            overflow: auto !important;
            position: relative;
        }

        @@media print {
            @@page {
                margin-top: 2cm;
                margin-bottom: 2cm;
            }

            body * {
                visibility: hidden;
            }

            #printable-area, #printable-area * {
                visibility: visible;
            }

            #printable-area {
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                padding: 1.2cm;
            }

            #printable-area pre,
            #printable-area code {
                white-space: pre-wrap !important;
                overflow-wrap: break-word;
                word-wrap: break-word;
                color: #222 !important;
            }

            #printable-area {
                font-family: Georgia, "Times New Roman", serif;
                font-size: 12pt;
                line-height: 1.5;
                color: #000 !important;
            }

            #printable-area strong, #printable-area b {
                font-weight: 700 !important; /* Use a heavy font-weight */
                color: inherit !important;
            }

            #printable-area h1, #printable-area h2, #printable-area h3 {
                margin-top: 24pt;
                margin-bottom: 12pt;
            }

            #printable-area a[href]::after {
                content: " (" attr(href) ")";
                font-size: 9pt;
                color: #555;
            }

            #printable-area table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
                font-size: 11pt;
            }
            #printable-area th, #printable-area td {
                border: 1px solid #ccc;
                padding: 0.5rem;
                text-align: left;
            }
        }
    </style>
}
```

这样，我们就引入了 CodeMirror 的样式，并添加了一些自定义的样式来美化页面。

!!! note "Aiursoft Template 特有的样式插入方式"

    上面的 `@section styles` 是模板文件中预定义的一个部分，用于插入页面特定的样式。你可以在这里添加任何你需要的 CSS 样式。它会渲染在页面的 `<head>` 标签内。除了可以使用内联样式，你也可以使用 `<link>` 标签来引入外部样式表。

!!! warning "务必使用 ReSharper disable once Razor.SectionNotResolved 来避免 Razor 报错"

    由于 Aiursoft Template 使用了自定义的视图引擎，Resharper 或 Rider 可能无法正确识别 `@section styles`，从而报错。为了避免这个问题，我们可以使用 `@* ReSharper disable once Razor.SectionNotResolved *@` 来告诉 Resharper 忽略这个错误。

其中注意：使用 @大括号 ，也就是 `@{ }` 包起来的代码是 C# 代码块，其在服务器端执行。而使用 @@ 符号来转义 @ 符号，以便在 CSS 中使用。在这里，我们得到了一个服务器端变量 `theme`，它根据用户的主题偏好动态设置 CodeMirror 的主题。

在上面，为了确保编辑器控件和预览区域不会太高，我们将它们的最大高度设置为 70vh（视口高度的 70%）。这样可以确保它们在大多数屏幕上都能良好显示。

上面，为了方便打印，我们使用了大量 CSS 技巧，以确保打印出来的内容美观且易读。同时也使用了 `#printable-area` 这个 ID 来指定打印区域。

显然，我们还需要一些 Javascript 代码来初始化 CodeMirror 编辑器，并处理复制按钮和打印按钮的功能。

继续在上面的视图文件的末尾，添加以下代码：

```html title="为 Index.cshtml 添加脚本"

@* ReSharper disable once Razor.SectionNotResolved *@
@section scripts {
    <script src="~/node_modules/codemirror/lib/codemirror.js"></script>
    <script src="~/node_modules/codemirror/mode/markdown/markdown.js"></script>
    <script src="~/node_modules/codemirror/mode/xml/xml.js"></script>
    <script src="~/node_modules/codemirror/addon/edit/closebrackets.js"></script>
    <script src="~/node_modules/codemirror/addon/edit/matchbrackets.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            let markdownEditorInstance;
            let htmlOutputInstance;

            // --- jQuery Validation Setup. Don't ignore hidden fields (CodeMirror will hide the original textarea) ---
            if ($.validator) {
                $.validator.setDefaults({
                    ignore: []
                });
            }

            // --- CodeMirror Initialization ---
            if (typeof CodeMirror !== 'undefined') {
                if (!document.getElementById('markdown-editor').CodeMirror) {
                    markdownEditorInstance = CodeMirror.fromTextArea(document.getElementById('markdown-editor'), {
                        lineNumbers: true,
                        mode: 'markdown',
                        theme: '@(theme)',
                        viewportMargin: Infinity
                    });

                    markdownEditorInstance.on('change', function() {
                        // For validator to work, we need to update the underlying textarea
                        markdownEditorInstance.save();
                    });
                }
                if (!document.getElementById('html-output').CodeMirror) {
                    htmlOutputInstance = CodeMirror.fromTextArea(document.getElementById('html-output'), {
                        lineNumbers: true,
                        mode: 'xml',
                        readOnly: true,
                        theme: '@(theme)',
                        viewportMargin: Infinity
                    });
                }
            }

            // --- Copy to Clipboard Handling ---
            const copyButton = document.getElementById('copy-button');
            if (copyButton && htmlOutputInstance) {
                copyButton.addEventListener('click', function () {
                    const codeToCopy = htmlOutputInstance.getValue();
                    if (!codeToCopy) {
                        return;
                    }
                    navigator.clipboard.writeText(codeToCopy).then(function () {
                        copyButton.innerHTML = `@Localizer["Copied!"]`;
                    }, function (err) {
                        console.error('Could not copy text: ', err);
                        alert('@Localizer["Failed to copy text."]');
                    });
                });
            }

            // --- Theme Toggle Handling ---
            const themeToggleButton = document.querySelector('.js-theme-toggle');
            const markdownForm = document.getElementById('markdown-form');
            if (themeToggleButton && markdownForm) {
                themeToggleButton.addEventListener('click', function () {
                    // Submit the form after switching theme to refresh CodeMirror themes
                    setTimeout(() => {
                        markdownForm.submit();
                    }, 1000);
                });
            }

            // --- Styling Tables in the Preview Pane ---
            function stylePreviewTables() {
                const previewArea = document.getElementById('preview');
                if (!previewArea) return;
                const tables = previewArea.querySelectorAll('table');
                tables.forEach(table => {
                    table.classList.add('table', 'table-striped', 'table-bordered');
                    if (!table.parentElement.classList.contains('table-responsive')) {
                        const wrapper = document.createElement('div');
                        wrapper.className = 'table-responsive';
                        table.parentNode.insertBefore(wrapper, table);
                        wrapper.appendChild(table);
                    }
                });
            }
            stylePreviewTables();

            // --- Print Button Handling ---
            const printButton = document.getElementById('print-button');
            if (printButton) {
                printButton.addEventListener('click', function () {
                    window.print();
                });
            }
        });
    </script>
}
```

!!! note "Aiursoft Template 特有的脚本插入方式"

    类似的，`@section scripts` 也是模板文件中预定义的一个部分，用于插入页面特定的脚本。你可以在这里添加任何你需要的 JavaScript 代码。它会出现在页面的底部。除了可以使用内联脚本，你也可以使用 `<script>` 标签来引入外部脚本文件。

> 在上面的代码中，我们使用了技巧 `@(theme)` 来动态设置 CodeMirror 的主题，以匹配用户的主题偏好。这是 Razor 的功能，它会在服务器端执行，将 C# 变量的值插入到生成的 HTML 中，再将其发送到客户端执行。参考上面提到的“服务器端渲染”技巧。

这样，我们的 jQuery Validation、CodeMirror 初始化、复制按钮、切换主题时自动刷新、更漂亮的表格样式、打印按钮等功能都实现了。

现在，你可以保存所有更改，重新编译并运行项目：

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet build
dotnet run
```

正常情况下，你可以在浏览器中访问 `http://localhost:5000`，看到一个漂亮的页面，允许你输入 markdown 并预览生成的 HTML。你也可以尝试点击“Convert to HTML”按钮，看看生成的 HTML 是否正确。还可以复制生成的 HTML，或者打印预览。

## 结语

恭喜你完成了第三步！你现在已经成功地添加了一个全新的页面，允许用户输入 markdown 并预览生成的 HTML。通过合理地使用 ASP.NET Core 的依赖注入、MVC 模式、Razor 视图等技术，你可以轻松地扩展你的应用功能。

Aiursoft Template 提供了强大的基础设施，让你能够专注于业务逻辑的实现，而不必担心底层的细节。开发一个简单的应用从未如此简单和高效！
