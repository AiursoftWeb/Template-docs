# 开始之前

这里是 Aiursoft Template 的快速入门教程。我们都知道，开始一个新项目可能会很麻烦，所以我们准备了这个教程来帮助你快速上手。

这个教程预计需要 30 分钟。在你完成后，你将拥有一个功能齐全的项目，可以作为你未来项目的基础。我们为了展示，将简单开发一个美观、带多数据库、RBAC、本地化、OIDC接入、单元测试、Docker部署的 markdown 转 HTML 的简单笔记应用。

我们强烈建议你不要跳过任何步骤以确保体验完整。祝你这段 30 分钟的历险旅程顺利，并且快速成为一位 Aiursoft Template 大师，圆梦 Web 开发！

# Aiursoft Template Tutorial - Step 1 - 创建新项目

## Step 1.1 准备开发环境

第一步的目标是创建一个全新的项目。我们推荐你使用 [AnduinOS](https://www.anduinos.com) 1.3 或更高版本来进行实战开发，因为 AnduinOS 1.3+ 非常容易安装 dotnet、bash、npm、git、docker、mysql、nginx 等工具。

如果你不想使用 AnduinOS，你也可以在任何支持 .NET 9.0 的操作系统上进行开发，例如 Windows、macOS 或其他 Linux 发行版。

在开始之前，请确保你已经安装了 `git`、`.NET 9.0 SDK` 和 `docker`。在 AnduinOS 上，你可以使用以下命令安装这些工具：

```bash
sudo apt install -y git dotnet9 docker.io
```

安装 git 后，你必须配置你的用户名和邮箱：

```bash
git config --global user.name "Your Name"
git config --global user.email "YourEmail@domain.com"
```

你还需要安装 Node.js 和 npm 以管理前端的依赖。你可以使用以下命令安装它们：

```bash
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg --yes
NODE_MAJOR=22
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update
sudo apt install nodejs -y
node -v
```

你还需要一个代码编辑器。我们推荐使用 [Visual Studio Code](https://code.visualstudio.com/) 或 [Jetbrains Rider](https://docs.anduinos.com/Applications/Code-Editors/Jetbrains-Rider/Jetbrains-Rider.html)。你也可以使用以下命令安装 Visual Studio Code：

```bash
cd ~
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt update
sudo apt install code -y
```

安装完成后，你可以通过运行 `code` 命令来启动 Visual Studio Code。

为了新建 Aiursoft Template 的项目，你需要安装 Voyager，它是 Aiursoft Template 的脚手架工具。你可以通过以下命令安装它：

```bash
dotnet tool install --global Aiursoft.Voyager
voyager --version
```

如果提示 `voyager` 命令未找到，请确保你的 `~/.dotnet/tools` 目录在你的 `PATH` 环境变量中。你可以使用这个命令来暂时缓解：

```bash
~/.dotnet/tools/voyager --version
```

如果上面过程一切顺利，你现在应该已经安装好了所有必要的工具，可以开始创建你的第一个 Aiursoft Template 项目了！

## Step 1.2 创建新项目

每次创建新项目时，都应当从这一步开始。

我们建议你使用一个独特的命名空间来避免与其他项目冲突。通常，我们建议使用类似 `MyOrg.MyProject` 的格式，其中 `MyOrg` 是你的组织或公司名称，`MyProject` 是你的项目名称。

这里，我们的模板是创建一个将 markdown 转换为 HTML 的应用，所以我们将命名为 `MyOrg.MarkToHtml`。

首先，创建一个新的文件夹来存放你的项目：

```bash
mkdir MyOrg.MarkToHtml
cd MyOrg.MarkToHtml
```

然后使用 voyager 初始化项目：

```bash
~/.dotnet/tools/voyager new -t web-app-all-in-one
```

你会注意到下面文件被生成：

```bash
.
├── CODE_OF_CONDUCT.md
├── Dockerfile
├── .editorconfig
├── .git
├── .gitignore
├── .gitlab-ci.yml
├── install.sh
├── LICENSE
├── MyOrg.MarkToHtml.sln
├── ninja.yaml
├── nuget.config
├── README.md
├── src
│   ├── MyOrg.MarkToHtml
│   ├── MyOrg.MarkToHtml.Entities
│   ├── MyOrg.MarkToHtml.InMemory
│   ├── MyOrg.MarkToHtml.MySql
│   └── MyOrg.MarkToHtml.Sqlite
└── tests
    ├── IntegrationTests
    └── MyOrg.MarkToHtml.Tests.csproj

15 directories, 17 files
```

其中未必所有文件都对你有用，下面是每个文件的简要说明：

* CODE_OF_CONDUCT.md: 代码行为准则，这只是一个示例。你可以放心的删除它而不影响项目。
* Dockerfile: 用于在 Docker 容器中运行应用的配置文件。它定义了如何在 Docker 里构建和运行应用的环境。
* .editorconfig: 代码风格配置文件，帮助你和你的团队保持一致的代码风格。你可以根据需要修改或删除它。
* .git: Git 版本控制的元数据文件夹。新创建项目时会自动生成，也会帮你生成一个初始的 commit。
* .gitignore: Git 忽略文件列表，指定哪些文件或文件夹不应被 Git 追踪。请不要删除它。
* .gitlab-ci.yml: GitLab CI/CD 的配置文件。如果你使用 GitLab 进行持续集成和部署，这个文件会定义你的流水线。如果你不使用 GitLab，可以删除它。
* install.sh: 一个简单的快速部署脚本，帮助你在无 Docker 的服务器上快速部署项目。你可以根据需要修改或删除它。
* LICENSE: 许可证文件，说明项目的使用和分发条款。你可以根据需要修改或删除它。
* MyOrg.MarkToHtml.sln: 这是 Visual Studio 的解决方案文件，包含了项目中的所有子项目。请不要删除它。
* ninja.yaml: 这是用于给 nuget ninja 看的配置文件，定义了项目的文件结构。如果你不使用 nuget ninja，可以删除它。
* README.md: 项目的自述文件，包含项目的基本信息和使用说明。你可以根据需要修改它。
* nuget.config: NuGet 包管理器的配置文件，定义了包源和其他设置。如果你不需要自定义包源，可以删除它。
* src/: 这个文件夹包含了项目的源代码。你会看到多个子项目文件夹，每个文件夹对应一个功能模块。你可以根据需要添加或删除子项目。
* tests/: 这个文件夹包含了项目的测试代码。你可以根据需要添加或删除测试项目。

接下来，你可以使用 Visual Studio Code 或 Jetbrains Rider 打开这个 `MyOrg.MarkToHtml.sln` 解决方案文件，开始编写代码了！

## Step 1.3 运行项目

在你开始编写代码之前，建议先编译并运行一下项目，确保一切正常工作。

你需要先还原前端的依赖。你可以使用以下命令来安装前端依赖：

```bash
cd ./src/MyOrg.MarkToHtml/wwwroot/
npm install
```

你可以使用以下命令来编译项目：

```bash
dotnet build ./MyOrg.MarkToHtml.sln
```

如果编译成功，你可以使用以下命令来运行项目：

```bash
cd ./src/MyOrg.MarkToHtml/
dotnet run
```

默认情况下，应用会在 `http://localhost:5000` 上运行。现在，你可以打开浏览器以访问这个地址，检查应用是否正常工作。正常情况下，你会看到一个欢迎页面。

你可以使用默认账户登录。默认账户信息如下：

* 用户名: `admin`
* 密码: `admin123`

## Step 1.4 配置项目使用的数据库 (可选)

> 这一步是完全可选的。如果你想使用默认配置，可以跳过这一步。

默认情况下，应用会使用 SQLite 作为数据库。这是配置在 `appsettings.json` 文件中的。如果你想使用其他数据库（如 MySQL 或 SQL Server），你需要修改 `appsettings.json` 文件中的连接字符串。在默认情况下，第一次启动会自动创建并播种数据库，您会注意到 `app.db` 文件被创建在 `src/MyOrg.MarkToHtml/` 目录下。

我们推荐你使用 [DbBrowser for SQLite](https://flathub.org/en/apps/org.sqlitebrowser.sqlitebrowser) 来查看和管理 SQLite 数据库，也就是 `app.db` 文件。删除这个文件即可将应用重置为初始状态。

默认情况下，应用会使用 `/tmp/data` 作为文件系统的后端存储路径。你可以在 `appsettings.json` 文件中修改这个路径。在默认情况下，这里可能会存放着默认的头像。

## 结语

恭喜你完成了第一步！你现在已经配置好了开发环境，初始化了 git 仓库，并成功运行了一个基本的 Aiursoft Template 项目，也理解了它使用的文件结构、Sqlite 数据库和文件存储。

接下来，我们将继续开发这个项目，添加更多功能。

# Aiursoft Template Tutorial - Step 2 - 添加和调试第三方库

## Step 2.1 添加第三方库

显然，我们本来的任务是创建一个将 markdown 转换为 HTML 的应用。为此，我们需要一个能够将 markdown 转换为 HTML 的库。

在这个教程里，我们选择 [Markdig](https://github.com/xoofx/markdig)。这是一款功能强大且易于使用的 markdown 解析器。

为了安装 Markdig，我们需要使用 NuGet 包管理器。你可以使用以下命令来安装它：

```bash
cd ./src/MyOrg.MarkToHtml/
dotnet add package Markdig
```

接下来，我们额外安装一个能够避免生成的 HTML 被 XSS 攻击的库，叫做 [HtmlSanitizer](https://github.com/mganss/HtmlSanitizer)。你可以使用以下命令来安装它：

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet add package HtmlSanitizer
```

你会注意到，在上面的命令执行完成后，`MyOrg.MarkToHtml.csproj` 文件中添加了对 Markdig 和 HtmlSanitizer 的引用，它看起来可能像这样：

```xml
<ItemGroup>
    <PackageReference Include="HtmlSanitizer" Version="9.0.886" />
    <PackageReference Include="Markdig" Version="0.42.0" />
</ItemGroup>
```

## Step 2.2 测试第三方库的工作能力 (可选)

> 这一步是完全可选的，是为了演示如何调试第三方库。如果你相信 Markdig 能够正常工作，可以跳过这一步。

接下来，我们需要先测试一下 Markdig 和 HtmlSanitizer 是否能正常工作。为此，我们直接修改 `./src/MyOrg.MarkToHtml/Program.cs` 文件，将 `Main` 方法原有内容暂时注释，然后暂时添加用于测试 Markdig 的以下代码：

```csharp
using Aiursoft.DbTools;
using MyOrg.MarkToHtml.Entities;
using static Aiursoft.WebTools.Extends;
using Markdig;

namespace MyOrg.MarkToHtml;

public abstract class Program
{
    public static async Task Main(string[] args)
    {
        var testMarkDown = """
                           # Hello World

                           This is a sample markdown text.

                           > This is a blockquote.
                           """;
        var pipeline = new MarkdownPipelineBuilder().UseAdvancedExtensions().Build();
        var html = Markdown.ToHtml(testMarkDown, pipeline);
        Console.WriteLine(html);

        // var app = await AppAsync<Startup>(args);
        // await app.UpdateDbAsync<TemplateDbContext>();
        // await app.SeedAsync();
        // await app.CopyAvatarFileAsync();
        // await app.RunAsync();
    }
}
```

接下来，我们可以再次运行项目来测试 Markdig 是否能正常工作：

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet run
```

可能会看到类似下面的输出：

```html
<h1 id="hello-world">Hello World</h1>
<p>This is a sample markdown text.</p>
<blockquote>
<p>This is a blockquote.</p>
</blockquote>
```

这证明 Markdig 能够成功地将 markdown 转换为 HTML。接下来，我们继续测试 HtmlSanitizer。

我们可以修改 `Program.cs` 文件中的测试代码，添加对 HtmlSanitizer 的使用：

```csharp
using Aiursoft.DbTools;
using Ganss.Xss;
using MyOrg.MarkToHtml.Entities;
using static Aiursoft.WebTools.Extends;

namespace MyOrg.MarkToHtml;

public abstract class Program
{
    public static async Task Main(string[] args)
    {
        var sanitizer = new HtmlSanitizer();
        var html = @"<script>alert('xss')</script><div onload=""alert('xss')"""
                   + @"style=""background-color: rgba(0, 0, 0, 1)"">Test<img src=""test.png"""
                   + @"style=""background-image: url(javascript:alert('xss')); margin: 10px""></div>";
        var sanitized = sanitizer.Sanitize(html, "https://www.example.com");
        Console.WriteLine(sanitized);

        // var app = await AppAsync<Startup>(args);
        // await app.UpdateDbAsync<TemplateDbContext>();
        // await app.SeedAsync();
        // await app.CopyAvatarFileAsync();
        // await app.RunAsync();
    }
}
```

这次，预计输出将会是：

```html
<div style="background-color: rgba(0, 0, 0, 1)">Test<img src="https://www.example.com/test.png" style="margin: 10px"></div>
```

可以注意到，所有潜在的 XSS 攻击向量都被移除了。说明 HtmlSanitizer 能够成功地清理 HTML。

## Step 2.3 恢复 `Program.cs` 文件

现在，我们测试完成了，回滚 `Program.cs` 文件中的更改，恢复原有内容：

```csharp
using Aiursoft.DbTools;
using MyOrg.MarkToHtml.Entities;
using static Aiursoft.WebTools.Extends;

namespace MyOrg.MarkToHtml;

public abstract class Program
{
    public static async Task Main(string[] args)
    {
        var app = await AppAsync<Startup>(args);
        await app.UpdateDbAsync<TemplateDbContext>();
        await app.SeedAsync();
        await app.CopyAvatarFileAsync();
        await app.RunAsync();
    }
}
```

## Step 2.4 安装前端的代码编辑器

考虑到我们需要在前端页面提供给用户编辑 Markdown 和预览 HTML 的功能，我们需要一个强大的前端代码编辑器。我们选择 [CodeMirror 5](https://codemirror.net/) 作为我们的前端代码编辑器。

为了安装 CodeMirror 5，我们需要使用 npm 包管理器。你可以使用以下命令来安装它：

```bash
cd ./src/MyOrg.MarkToHtml/wwwroot/
npm install codemirror@5 --save
```

你会注意到，在上面的命令执行完成后，`./src/MyOrg.MarkToHtml/wwwroot/package.json` 文件中添加了对 CodeMirror 的引用，它看起来可能像这样：

```json
{
  "name": "wwwroot",
  "version": "1.0.0",
  "description": "This is a server side application. This package is used to host the static files.",
  "author": "Anduin Xue",
  "license": "MIT",
  "dependencies": {
    "@aiursoft/uistack": "^1.0.8",
    "codemirror": "^5.65.20",
    "dropify": "^0.2.2"
  }
}
```

## 结语

恭喜你完成了第二步！你现在已经成功地添加并测试了第三方库 Markdig， HtmlSanitizer 和 CodeMirror。通过合理地使用 Nuget、npm、GitHub，你可以轻松将前人的工作成果整合到你的项目中，并快速扩充你的项目功能。

# Aiursoft Template Tutorial - Step 3 - 添加全新的页面

在上一步，我们成功地添加了将 markdown 转换为 HTML 的功能。接下来，我们需要创建一个前端页面，让用户能够输入 markdown 并预览生成的 HTML。

## Step 3.1 修改将必要的服务添加到依赖注入容器中

ASP.NET Core 使用依赖注入来管理应用的服务。为了让 Markdig 和 HtmlSanitizer 能够在应用中使用，我们需要将它们添加到依赖注入容器中。

首先，修改 `./src/MyOrg.MarkToHtml/Startup.cs` 文件，首先添加必要的 using 语句：

```csharp
using Ganss.Xss;
using Markdig;
```

然后找到 `public void ConfigureServices(IConfiguration configuration, IWebHostEnvironment environment, IServiceCollection services)` 方法，添加下面的代码：

```csharp
// Add the markdown pipeline and HTML sanitizer
var pipeline = new MarkdownPipelineBuilder().UseAdvancedExtensions().Build();
services.AddSingleton(pipeline);
services.AddSingleton<HtmlSanitizer>();
```

## Step 3.2 写一个全新的转换服务

为了更好地组织代码，我们将创建一个新的服务类，专门负责将 markdown 转换为 HTML。这样可以让代码更加模块化，易于维护。

所有的服务类都应该放在 `./src/MyOrg.MarkToHtml/Services/` 目录下。

在这里新建一个名为 `MarkToHtmlService.cs` 的文件，并添加以下代码：

```csharp
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

务必牢记：

> Singleton 的服务在整个应用生命周期内只会创建一个实例，适用于无状态且线程安全的服务。它只能依赖其它 Singleton 的服务。不可以依赖 Scoped 或 Transient 的服务。
> Scoped 的服务在每个请求的生命周期内创建一个实例，适用于需要在请求间保持状态的服务。它可以依赖 Singleton 和 Scoped 的服务。不可以依赖 Transient 的服务。
> Transient 的服务每次请求都会创建一个新的实例，适用于轻量级且无状态的服务。它可以依赖任何类型的服务，包括 Singleton、Scoped 和 Transient。

打破上面的规则，应用仍然可以编译，甚至某些情况下可能可以运行；但容易产生非常诡异的生命周期问题，导致难以调试的 bug。

因此，在这里我们将 `MarkdownPipeline` 和 `HtmlSanitizer` 注册为 Singleton，因为它们是黑盒，又线程安全，还可以反复使用也就是无状态的。而 `MarkToHtmlService` 则注册为 Transient，因为构造它开销较小且无状态。

## Step 3.3 修改 ViewModel

为了让前端页面能够与后端服务进行交互，我们需要一个 ViewModel。ViewModel 是一种设计模式，用于将数据从控制器传递到视图。

在这里，为了简单，我们直接修改 `./src/MyOrg.MarkToHtml/Models/HomeViewModels/IndexViewModel.cs` 文件，添加一个新的属性 `MarkdownInput` 来存储用户输入的 markdown 内容，并将 `OutputHtml` 属性用于存储生成的 HTML 内容。

```csharp
using System.ComponentModel.DataAnnotations;
using Aiursoft.UiStack.Layout;

namespace MyOrg.MarkToHtml.Models.HomeViewModels;

public class IndexViewModel : UiStackLayoutViewModel
{
    public IndexViewModel()
    {
        PageTitle = "Markdown to HTML Converter";
    }

    [Required]
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

```csharp
public class HomeController(
    MarkToHtmlService mtohService) : Controller
```

然后增加一个新的 `Index` 方法来处理 POST 请求，将输入的 markdown 转换为 HTML：

```csharp
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

> 注意：Aiursoft Template 要求所有返回视图时，均使用 `this.StackView(model)` 方法来返回视图，而不是直接使用 `return View(model)`。这是因为 `StackView` 方法会自动处理一些 Aiursoft UiStack 相关的逻辑，例如导航栏、布局等。

其中，`[HttpPost]` 特性表示这个方法只处理 POST 请求，`[ValidateAntiForgeryToken]` 特性用于防止跨站请求伪造 (CSRF) 攻击。ASP.NET Core 的表单在提交时会自动包含一个防伪令牌，服务器端会验证这个令牌以确保请求的合法性。

此时，我们的 `HomeController.cs` 文件应该类似于下面这样：

```csharp
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
        LinkText = "Index",
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

## Step 3.5 修改视图

视图 (View) 是 MVC 模式中的 V，负责渲染用户界面。在我们的结构中，视图使用 Razor 语法来生成 HTML 页面。

显然，视图的职责是绘制一个好看的页面，让用户能够输入 markdown 并预览生成的 HTML。

在我们编写视图的时候，只需要尊重 ViewModel 的属性即可。视图文件位于 `./src/MyOrg.MarkToHtml/Views/Home/Index.cshtml`。在默认情况下，它可能包含了一些示例内容。可以放心的直接删除，然后进行修改。

将其修改为以下内容：

```html
@using MyOrg.MarkToHtml.Controllers
@model MyOrg.MarkToHtml.Models.HomeViewModels.IndexViewModel
@inject IViewLocalizer Localizer

@* Page Header *@
<div class="row mb-2 mb-xl-3">
    <div class="col-auto d-none d-sm-block">
        <h3>@ViewData["Title"]</h3>
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

当然，你也可以继续使用熟悉的 C# 语法来动态渲染，例如 `@if`、`@for`、`@foreach` 等等。这种技巧可以让你轻松地将服务器端的数据渲染到客户端页面。但注意：它会在服务器端执行，将 C# 变量的值插入到生成的 HTML 中，再将其发送到客户端执行。相当于是使用 C# 在动态拼接 HTML，这种技巧叫作“服务器端渲染”，其优先级高于 JavaScript，可以在没有 JavaScript 的情况下运行；但缺点是无法在前端动态改变，并且会占用服务器的算力。

在后面的例子中，我们将大量使用这种技巧来渲染页面。

## Step 3.6 添加必要的样式和脚本

显然，上面的视图只能完成最基本的编辑和预览功能。其中复制按钮、打印按钮、代码高亮等功能都需要额外的样式和脚本来支持。

首先，还记得我们曾经安装 `codemirror` 吗？我们现在需要将它引入到页面中。

在上面的视图文件的末尾，添加以下代码：

```html
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

> 上面的 `@section styles` 是模板文件中预定义的一个部分，用于插入页面特定的样式。你可以在这里添加任何你需要的 CSS 样式。它会渲染在页面的 `<head>` 标签内。除了可以使用内联样式，你也可以使用 `<link>` 标签来引入外部样式表。

其中注意：使用 @大括号 ，也就是 `@{ }` 包起来的代码是 C# 代码块，其在服务器端执行。而使用 @@ 符号来转义 @ 符号，以便在 CSS 中使用。在这里，我们得到了一个服务器端变量 `theme`，它根据用户的主题偏好动态设置 CodeMirror 的主题。

在上面，为了确保编辑器控件和预览区域不会太高，我们将它们的最大高度设置为 70vh（视口高度的 70%）。这样可以确保它们在大多数屏幕上都能良好显示。

上面，为了方便打印，我们使用了大量 CSS 技巧，以确保打印出来的内容美观且易读。同时也使用了 `#printable-area` 这个 ID 来指定打印区域。

显然，我们还需要一些 Javascript 代码来初始化 CodeMirror 编辑器，并处理复制按钮和打印按钮的功能。

继续在上面的视图文件的末尾，添加以下代码：

```html

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

> 类似的，`@section scripts` 也是模板文件中预定义的一个部分，用于插入页面特定的脚本。你可以在这里添加任何你需要的 JavaScript 代码。它会出现在页面的底部。除了可以使用内联脚本，你也可以使用 `<script>` 标签来引入外部脚本文件。

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

# Aiursoft Template Tutorial - Step 4 - 添加全新的数据模型并改变数据库结构

我们可以扩展上面的例子，允许用户保存他们的 markdown 文档，并在之后重新编辑甚至分享它们。为此，我们需要添加一个新的数据模型，并改变数据库结构。

在改变数据库结构之前，我们需要先了解一下 Aiursoft Template 使用的数据库 ORM 工具：[Entity Framework Core (EF Core)](https://learn.microsoft.com/en-us/ef/core/)。

## Step 4.1 理解 Entity Framework Core （可选）

如果你非常熟悉 Entity Framework Core，可以跳过这一步。

Entity Framework Core (EF Core) 是一个强大的对象关系映射 (ORM) 工具，允许你使用 .NET 对象来操作数据库，而不必直接编写 SQL 语句。它支持多种数据库，包括 SQLite、MySQL、SQL Server、PostgreSQL 等等。

例如，它的语法类似：

```csharp
var books = await dbContext.Books
    .Where(b => b.Author == "Anduin Xue")
    .OrderBy(b => b.PublishedDate)
    .Skip(10)
    .Take(10)
    .ToListAsync();
```

这将会从数据库的 `Books` 表中查询作者为 "Anduin Xue" 的书籍，按发布日期排序，跳过前 10 条记录，取接下来的 10 条记录，并将结果转换为一个列表。其 SQL 可能类似：

```sql
SELECT * FROM Books
WHERE Author = 'Anduin Xue'
ORDER BY PublishedDate
LIMIT 10 OFFSET 10;
```

但是，考虑到我们可能会修改一些实体类的结构，例如增加新的属性，删除旧的属性，或者修改属性的类型。为了让数据库结构与实体类保持同步，我们需要使用 EF Core 的迁移 (Migration) 功能。

在这个例子里，我们将新建一个表，叫做 `MarkdownDocuments`，用于存储用户的 markdown 文档。但真实的数据库里并不存在这个表。因此，我们需要创建一个迁移来告诉 EF Core 如何创建这个表。迁移包含了数据库结构的变更信息。程序在启动的时候，会自动比较数据库本身的表结构的版本和最新的迁移版本，并自动运行差异的迁移。这样就能确保数据库结构与实体类保持同步。

如果忘记了创建迁移，或迁移没有成功运行，程序会仍然能运行，但执行的 SQL 可能无法正确在数据库里完成预期的操作，导致程序运行时出现异常。因此，每次修改了实体类后，都应该创建一个新的迁移。

## Step 4.2 创建新的数据模型

接下来，我们准备使用 Entity Framework Core 来创建一个新的数据模型类，叫做 `MarkdownDocument`，用于存储用户的 markdown 文档。其存储在表 `MarkdownDocuments` 中。

为了创建这个数据模型，我们直接修改 `./src/MyOrg.MarkToHtml/Entities/User.cs` 文件：

添加必要的 using 语句：

```csharp
using System.ComponentModel.DataAnnotations.Schema;
using System.Diagnostics.CodeAnalysis;
using System.Text.Json.Serialization;
```

添加一个新的类 `MarkdownDocuments`，表示用户拥有的所有 markdown 文档。

```csharp
public class User : IdentityUser
{
    // ... Existing properties ...
}

// New entity for storing markdown documents
public class MarkdownDocument
{
    [Key]
    public Guid Id { get; set; }

    [MaxLength(100)]
    public string? Title { get; set; }

    [MaxLength(65535)]
    public string? Content { get; set; }

    public DateTime CreationTime { get; init; } = DateTime.UtcNow;

    [StringLength(64)]
    public required string UserId { get; set; }

    [ForeignKey(nameof(UserId))]
    [NotNull]
    public User? User { get; set; }
}
```

在上面的例子中，我们的类 `MarkdownDocument` 包含了以下属性：

* `Id`：文档的唯一标识符，使用 GUID 类型。
* `Title`：文档的标题，最多 100 个字符。
* `Content`：文档的内容，最多 65535 个字符。
* `CreationTime`：文档的创建时间，使用 UTC 时间。
* `UserId`：文档所属用户的 ID，使用字符串类型，长度为 64 个字符。
* `User`：导航属性，表示文档所属的用户。其中 `UserId` 是外键，引用了 `User` 实体的主键。

> 关系型数据库的表之间通常通过外键来建立关联。在上面的例子中，`MarkdownDocument` 实体通过 `UserId` 属性与 `User` 实体建立了多对一的关系。也就是说，一个用户可以拥有多个文档，而每个文档只能属于一个用户。

在这里我们使用了一些 `Attributes`，例如 `[Key]`、`[MaxLength]`、`[StringLength]`、`[ForeignKey]` 等等。这些 `Attributes` 用于告诉 Entity Framework Core 如何映射这个类到数据库表。而 `[NotNull]` 和 `[JsonIgnore]` 则用于告诉编译器和 JSON 序列化器如何处理这些属性。

同时，我们编辑上面的 User 类，增加属性：

```csharp
[JsonIgnore]
[InverseProperty(nameof(MarkdownDocument.User))]
public IEnumerable<MarkdownDocument> CreatedDocuments { get; set; } = new List<MarkdownDocument>();
```

最终这个文件看起来可能像这样：

```csharp
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Diagnostics.CodeAnalysis;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Identity;

namespace MyOrg.MarkToHtml.Entities;

public class User : IdentityUser
{
    public const string DefaultAvatarPath = "Workspace/avatar/default-avatar.jpg";

    [MaxLength(30)]
    [MinLength(2)]
    public required string DisplayName { get; set; }

    [MaxLength(150)]
    [MinLength(2)]
    public string AvatarRelativePath { get; set; } = DefaultAvatarPath;

    public DateTime CreationTime { get; init; } = DateTime.UtcNow;

    [JsonIgnore]
    [InverseProperty(nameof(MarkdownDocument.User))]
    public IEnumerable<MarkdownDocument> CreatedDocuments { get; set; } = new List<MarkdownDocument>();
}

public class MarkdownDocument
{
    [Key]
    public Guid Id { get; set; }

    [MaxLength(100)]
    public string? Title { get; set; }

    [MaxLength(65535)]
    public string? Content { get; set; }

    public DateTime CreationTime { get; init; } = DateTime.UtcNow;

    [StringLength(64)]
    public required string UserId { get; set; }

    [ForeignKey(nameof(UserId))]
    [NotNull]
    public User? User { get; set; }
}
```

这样，我们就完成了数据模型的创建。

最后，为了显示的表明我们需要一个新表，编辑文件 `./src/MyOrg.MarkToHtml.Entities/MarkToHtmlDbContext.cs`，为 `TemplateDbContext` 添加以下属性：

```csharp
public DbSet<MarkdownDocument> MarkdownDocuments => Set<MarkdownDocument>();
```

当我们将 `TemplateDbContext` 作为数据库上下文类时，Entity Framework Core 会自动识别 `MarkdownDocuments` 属性，并将其映射到数据库中的 `MarkdownDocuments` 表。从而我们可以操作 `dbContext.MarkdownDocuments` 来进行 CRUD 操作。其会自动翻译成相应的 SQL 语句。

最终这个文件看起来可能像这样：

```csharp
using Aiursoft.DbTools;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace MyOrg.MarkToHtml.Entities;

public abstract class TemplateDbContext(DbContextOptions options) : IdentityDbContext<User>(options), ICanMigrate
{
    public virtual  Task MigrateAsync(CancellationToken cancellationToken) =>
        Database.MigrateAsync(cancellationToken);

    public virtual  Task<bool> CanConnectAsync() =>
        Database.CanConnectAsync();

    public DbSet<MarkdownDocument> MarkdownDocuments => Set<MarkdownDocument>();
}
```

这样，我们就完成了数据模型的创建。但是，数据库本身并不存在这个表。因此现在直接运行程序会报错。我们需要创建一个迁移来告诉 EF Core 如何创建这个表。

## Step 4.3 创建迁移并更新数据库

Aiursoft Template 支持多种数据库，包括 SQLite、MySQL、InMemory 等等。用户还可以额外扩展出其它数据库，例如 `PostgreSQL`、`SQL Server` 等等。在这里，我们只为默认的 SQLite 和 MySQL 创建迁移。其中 InMemory 数据库不需要迁移，因为它是临时的，程序每次启动都会重新创建。

为了创建迁移，我们需要使用 Entity Framework Core 的命令行工具 `dotnet ef`。如果你还没有安装它，可以使用以下命令来安装：

```bash
dotnet tool install --global dotnet-ef
```

### Step 4.3.1 为 SQLite 创建迁移

然后，我们需要为 SQLite 和 MySQL 分别创建迁移。为 Sqlite 创建迁移时，需要确保 `./src/MyOrg.MarkToHtml/appsettings.json` 中的 `ConnectionStrings.DbType` 设置为 `Sqlite`，并且 `DefaultConnection` 指向一个 SQLite 数据库文件，例如：

```json
{
  "ConnectionStrings": {
    "AllowCache": "True",
    "DbType": "Sqlite",
    "DefaultConnection": "DataSource=app.db;Cache=Shared"
  },
  // ... other settings ...
}
```

然后，运行以下命令来创建迁移：

```bash
cd ./src/MyOrg.MarkToHtml.Sqlite/
dotnet ef migrations add AddMarkdownDocumentsTable --context "SqliteContext" -s ../MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

会注意到类似这样的输出：

```bash
Done. To undo this action, use 'ef migrations remove'
```

同时，会在 `./src/MyOrg.MarkToHtml.Sqlite/Migrations/` 目录下生成一个新的迁移文件，名字类似 `20231010123456_AddMarkdownDocumentsTable.cs`。其内容可能类似：

```csharp
using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MyOrg.MarkToHtml.Sqlite.Migrations
{
    /// <inheritdoc />
    public partial class AddMarkdownDocumentsTable : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "MarkdownDocuments",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "TEXT", nullable: false),
                    Title = table.Column<string>(type: "TEXT", maxLength: 100, nullable: true),
                    Content = table.Column<string>(type: "TEXT", maxLength: 65535, nullable: true),
                    CreationTime = table.Column<DateTime>(type: "TEXT", nullable: false),
                    UserId = table.Column<string>(type: "TEXT", maxLength: 64, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_MarkdownDocuments", x => x.Id);
                    table.ForeignKey(
                        name: "FK_MarkdownDocuments_AspNetUsers_UserId",
                        column: x => x.UserId,
                        principalTable: "AspNetUsers",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_MarkdownDocuments_UserId",
                table: "MarkdownDocuments",
                column: "UserId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "MarkdownDocuments");
        }
    }
}
```

我们需要仔细 Review 上面的变化。当这个新的迁移运行时，它会创建一个新的表 `MarkdownDocuments`，并包含我们在数据模型中定义的所有列和约束，包含我们定义的外键约束。其中，`onDelete: ReferentialAction.Cascade` 表示当用户被删除时，关联的文档也会被自动删除。这是符合我们的预期的。

而 `Down` 方法则用于回滚迁移，即删除 `MarkdownDocuments` 表。符合我们的期待，那么么我们就可以继续了。

### Step 4.3.2 为 MySQL 创建迁移

然后，我们需要为 MySQL 创建迁移。为 MySQL 创建迁移时，需要确保 `./src/MyOrg.MarkToHtml.MySQL/appsettings.json` 中的 `ConnectionStrings.DbType` 设置为 `MySQL`，并且 `DefaultConnection` 指向一个 MySQL 数据库。其开头可以改成下面这样：

```json
{
  "ConnectionStrings": {
    "AllowCache": "True",
    "DbType": "MySql",
    "DefaultConnection": "Server=localhost;Database=template;Uid=template;Pwd=template_password;"
  },
  // ... other settings ...
}
```

接下来，为了创建迁移，我们必须启动一个真正的 MySQL。我们可以使用 Docker 来快速启动一个 MySQL 实例：

```bash
sudo docker run -d --name db -e MYSQL_RANDOM_ROOT_PASSWORD=true -e MYSQL_DATABASE=template -e MYSQL_USER=template -e MYSQL_PASSWORD=template_password -p 3306:3306 mysql
```

这满足了我们的应用程序的连接字符串要求。此时，我们可以使用以下命令来创建迁移：

```bash
cd ./src/MyOrg.MarkToHtml.MySql/ # 务必确保你在这个目录下
dotnet ef migrations add AddMarkdownDocumentsTable --context "MySqlContext" -s ../MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

类似的，也会在 `./src/MyOrg.MarkToHtml.MySQL/Migrations/` 目录下生成一个新的迁移文件，名字类似 `20231010123456_AddMarkdownDocumentsTable.cs`。将其内容仔细 Review 一下，确保它符合我们的预期，即可继续。

### Step 4.3.3 清理工作 删除数据库、回滚 appsettings.json

注意：如果你在创建迁移时遇到错误，提示无法连接到数据库，或者找不到某些类型，可能是因为你的 MySQL 服务器没有正确启动，或者你忘记了修改 `appsettings.json` 文件中的连接字符串。请确保你的 MySQL 服务器正在运行，并且连接字符串正确无误。

注意：在创建完 MySQL 迁移后，如果你不再需要这个 MySQL 实例，可以使用以下命令来停止并删除它：

```bash
sudo docker stop db
sudo docker rm db
```

同时，为了方便本地调试，建议回滚 `appsettings.json` 文件中的 `ConnectionStrings.DbType` 设置为 `Sqlite`，并且 `DefaultConnection` 指向一个 SQLite 数据库文件，例如：

```json
{
  "ConnectionStrings": {
    "AllowCache": "True",
    "DbType": "Sqlite",
    "DefaultConnection": "DataSource=app.db;Cache=Shared"
  },
  // ... other settings ...
}
```

每次修改了任何实体类，都应该重复执行上面 4.3.1 和 4.3.2 的步骤，创建新的迁移。如果你还支持了更多的数据库，也应该为它们创建迁移。

## Step 4.4 运行应用并验证数据库自动迁移（可选）

> 这一步是可选的。因为在生产环境中，迁移会在应用启动时自动运行。

现在，我们已经创建了迁移，接下来我们需要运行应用程序，并让它自动应用这些迁移，从而更新数据库结构。

在开始之前，我们可以先阅读一下 `./src/MyOrg.MarkToHtml/Startup.cs` 文件，了解一下应用程序是如何配置数据库的。找到下面代码，无需修改：

```csharp
var (connectionString, dbType, allowCache) = configuration.GetDbSettings();
services.AddSwitchableRelationalDatabase(
    dbType: EntryExtends.IsInUnitTests() ? "InMemory": dbType,
    connectionString: connectionString,
    supportedDbs:
    [
        new MySqlSupportedDb(allowCache: allowCache, splitQuery: false),
        new SqliteSupportedDb(allowCache: allowCache, splitQuery: true),
        new InMemorySupportedDb()
    ]);
```

上面的代码是配置此应用程序支持的数据库的核心代码。它会根据配置文件中的 `ConnectionStrings.DbType` 来选择使用哪种数据库，并根据 `ConnectionStrings.DefaultConnection` 来连接数据库。

其中，`allowCache` 则表示是否允许使用内存缓存数据库的查询结果，以提高性能。对于单个的实例，这个值通常应该设置为 `True` 以巨大的提升性能。但对于多实例的部署，这个值应该设置为 `False`，以避免缓存不一致的问题。

我们也会注意到，在单元测试环境中，数据库类型会被强制设置为 `InMemory`，以避免对真实数据库的依赖。

接下来，我们直接使用命令行来运行应用程序：

```bash
cd ./src/MyOrg.MarkToHtml/
dotnet run
```

在这次的运行中，会注意到下面的输出（注意：它只会在第一次运行时出现）：

```bash
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      SELECT "MigrationId", "ProductVersion"
      FROM "__EFMigrationsHistory"
      ORDER BY "MigrationId";
info: Microsoft.EntityFrameworkCore.Migrations[20402]
      Applying migration '20250924144553_AddMarkdownDocumentsTable'.
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (0ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      CREATE TABLE "MarkdownDocuments" (
          "Id" TEXT NOT NULL CONSTRAINT "PK_MarkdownDocuments" PRIMARY KEY,
          "Title" TEXT NULL,
          "Content" TEXT NULL,
          "CreationTime" TEXT NOT NULL,
          "UserId" TEXT NOT NULL,
          CONSTRAINT "FK_MarkdownDocuments_AspNetUsers_UserId" FOREIGN KEY ("UserId") REFERENCES "AspNetUsers" ("Id") ON DELETE CASCADE
      );
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (0ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      CREATE INDEX "IX_MarkdownDocuments_UserId" ON "MarkdownDocuments" ("UserId");
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (0ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
      VALUES ('20250924144553_AddMarkdownDocumentsTable', '9.0.9');
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (5ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      DELETE FROM "__EFMigrationsLock";
info: MyOrg.MarkToHtml.Entities.TemplateDbContext[0]
      Migrated database associated with context TemplateDbContext
```

可以看到，应用程序自动检测到数据库结构与最新的迁移版本不一致，因此它自动应用了我们刚才创建的迁移，创建了 `MarkdownDocuments` 表。只会再次运行，将会直接启动，而不会再次应用迁移。

## 结语

恭喜你完成了第四步！你现在已经成功地添加了一个全新的数据模型，并改变了数据库结构。通过合理地使用 Entity Framework Core 的迁移功能，你可以轻松地管理数据库结构的变更，而不必担心手动编写 SQL 语句，也不必担心数据库结构与实体类不一致的问题。甚至无需反复编译程序，就可以灵活的在多种数据库之间切换。

# Aiursoft Template Tutorial - Step 5 - 将数据保存到数据库

接下来，我们将继续扩展上面的例子，允许用户保存他们的 markdown 文档，并在之后重新编辑甚至分享它们。为此，我们需要修改控制器和视图，以便用户可以创建、查看、编辑和删除他们的文档。

## Step 5.1 保存并更新用户的文档

首先，我们需要修改 `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` 文件，添加必要的 using 语句：

```csharp
using System.ComponentModel.DataAnnotations;
using Aiursoft.CSTools.Tools;
using MyOrg.MarkToHtml.Models.HomeViewModels;
using MyOrg.MarkToHtml.Services;
using Aiursoft.UiStack.Navigation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyOrg.MarkToHtml.Entities;
```

然后我们调整其构造方法，支持日志、数据库和用户管理器：

```csharp
public class HomeController(
    ILogger<HomeController> logger,
    UserManager<User> userManager,
    TemplateDbContext context,
    MarkToHtmlService mtohService) : Controller
```

接下来我们重构 `Index` 方法，对于未认证的用户，我们直接渲染成 HTML，以保持核心功能不变。而对于已经认证的用户，我们则直接在数据库中添加或更新他们的文档，然后交给具体的 `Edit` 方法来渲染。

将 `Index` 方法修改为：

```csharp
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> Index(IndexViewModel model)
{
    if (!ModelState.IsValid)
    {
        return this.StackView(model);
    }

    var userId = userManager.GetUserId(User);
    if (User.Identity?.IsAuthenticated == true && !string.IsNullOrWhiteSpace(userId))
    {
        // If the user is authenticated, this action only saves the document in the database. And it's `edit` action to render it.
        // And go to the edit page.
        logger.LogTrace("Authenticated user submitted a document with ID: '{Id}'. Save it to the database.",
            model.DocumentId);
        var documentInDb = await context.MarkdownDocuments
            .FirstOrDefaultAsync(d => d.Id == model.DocumentId && d.UserId == userId);
        if (documentInDb != null)
        {
            logger.LogInformation("Updating the document with ID: '{Id}'.", model.DocumentId);
            documentInDb.Content = model.InputMarkdown.SafeSubstring(65535);
            documentInDb.Title = model.Title;
        }
        else
        {
            logger.LogInformation("Creating a new document with ID: '{Id}'.", model.DocumentId);
            model.DocumentId = Guid.NewGuid();
            var newDocument = new MarkdownDocument
            {
                Id = model.DocumentId,
                Content = model.InputMarkdown.SafeSubstring(65535),
                Title = model.InputMarkdown.SafeSubstring(40),
                UserId = userId
            };
            context.MarkdownDocuments.Add(newDocument);
        }

        await context.SaveChangesAsync();
        return RedirectToAction(nameof(Edit), new { id = model.DocumentId });
    }
    else
    {
        // If the user is not authenticated, just show the result.
        logger.LogInformation(
            "An anonymous user submitted a document with ID: '{Id}'. It was not saved to the database.",
            model.DocumentId);
        model.OutputHtml = mtohService.ConvertMarkdownToHtml(model.InputMarkdown);
        return this.StackView(model);
    }
}
```

当然，完成上面的修改后，你会注意到几个错误，包括 `model.DocumentId`、`model.Title` 找不到等。别担心，我们立刻去更新 `IndexViewModel`。

编辑文件 `./src/MyOrg.MarkToHtml/Models/HomeViewModels/IndexViewModel.cs`，添加必要的属性：

```csharp
[Required]
public Guid DocumentId { get; set; } = Guid.NewGuid();

public bool IsEditing { get; init; }

[MaxLength(100)]
public string? Title { get; set; }
```

其中，`DocumentId` 用于标识用户的文档。对于每个新 GET 请求，我们每次都会生成一个新的 ID。为了确保反复提交编辑过程中这个Id不会变，我们需要在视图中将其作为隐藏字段提交。

修改 `./src/MyOrg.MarkToHtml/Views/Home/Index.cshtml`，在 `<form>` 标签内添加以下代码：

```html
<form asp-action="Index" method="post" id="markdown-form">
    <input type="hidden" asp-for="DocumentId" />
    ... Other existing code ...
```

这样在每次提交的时候，都会将 `DocumentId` 一起提交到服务器端。

### Step 5.1.1 理解保存和更新逻辑

阅读服务端的代码，其中核心逻辑是：

```csharp
var documentInDb = await context.MarkdownDocuments
    .FirstOrDefaultAsync(d => d.Id == model.DocumentId && d.UserId == userId);
if (documentInDb != null)
{
    logger.LogInformation("Updating the document with ID: '{Id}'.", model.DocumentId);
    documentInDb.Content = model.InputMarkdown.SafeSubstring(65535);
    documentInDb.Title = model.Title;
}
else
{
    logger.LogInformation("Creating a new document with ID: '{Id}'.", model.DocumentId);
    model.DocumentId = Guid.NewGuid();
    var newDocument = new MarkdownDocument
    {
        Id = model.DocumentId,
        Content = model.InputMarkdown.SafeSubstring(65535),
        Title = model.InputMarkdown.SafeSubstring(40),
        UserId = userId
    };
    context.MarkdownDocuments.Add(newDocument);
}
```

对于未认证用户，我们直接渲染成 HTML，以保持核心功能不变。对于已认证的用户，我们要支持保存和更新他们的文档。所以第一次提交时，我们可以帮用户保存到数据库，并建立 DocumentId 和 UserId 的关联。之后用户再次提交时，我们就可以根据 DocumentId 和 UserId 来找到对应的文档，并更新它的内容和标题。

我们的代码是：

```text
用户的 DocumentId 如果不存在或不属于这个用户，那么不会信任用户提交的 DocumentId，而是重新生成一个新的 ID 然后插入数据库。这样可以防止用户恶意提交别人的 DocumentId 来修改别人的文档。

而如果用户提交的 DocumentId 存在并且属于当前用户，那么就只更新这个文档的内容和标题。具体的 Markdown 渲染过程则交给了 `Edit` 方法来处理。现在，我们创建 `Edit` 方法。
```

## Step 5.2 创建编辑文档的页面

在 `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` 文件中，添加以下代码：

```csharp
[Authorize]
public async Task<IActionResult> Edit([Required][FromRoute]Guid id)
{
    var userId = userManager.GetUserId(User);
    var document = await context.MarkdownDocuments.FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

    if (document == null)
    {
        return NotFound("The document was not found or you do not have permission to edit it.");
    }

    var model = new IndexViewModel
    {
        DocumentId = document.Id,
        Title = document.Title,
        InputMarkdown = document.Content ?? string.Empty,
        OutputHtml = mtohService.ConvertMarkdownToHtml(document.Content ?? string.Empty),
        IsEditing = true
    };

    return this.StackView(model: model, viewName: nameof(Index)); // Reuse the Index view for editing.
}
```

在上面的代码中，我们使用了 `[Authorize]` 属性来确保只有认证用户才能访问这个方法。

我们根据传入的 `id` 参数，从数据库中查询对应的文档。如果找不到文档，或者文档不属于当前用户，就返回 404 错误。

> ASP.NET Core 会自动将路由参数绑定到方法参数上。如果参数使用了 `[FromRoute]` 属性，表示这个参数来自路由。而 `id` 这个参数，则来自于 URL 中的 `{id}` 部分。在默认行为下，它的路由遵循控制器的路由规则，例如 `/Home/Edit/{id}`。也就是说，如果用户访问 `/Home/Edit/1234`，那么 `id` 参数就会被绑定为 `1234`。

我们之前的 `Index` 已经可以将已经认证的用户的文档保存到数据库中，并且在保存后重定向到 `Edit` 方法来渲染文档。因此，我们可以复用 `Index` 视图来显示编辑页面。

考虑到创建和编辑我们共享了同一个视图，我们在 `IndexViewModel` 中添加了一个 `IsEditing` 属性，用于区分当前是创建还是编辑状态。

例如，我们可以在编辑模式下，除了允许编辑文档外，还可以允许用户编辑文档的标题。我们可以在视图中添加一个输入框，用于编辑标题。

修改 `./src/MyOrg.MarkToHtml/Views/Home/Index.cshtml` 文件，在左侧的 Markdown 输入区域上方，添加以下代码：

```html
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
            @if (Model.IsEditing)
            {
                <div class="mb-3">
                    <label asp-for="Title" class="form-label">@Localizer["Document Title (optional)"]</label>
                    <input asp-for="Title" class="form-control form-control-lg" placeholder="@Localizer["Document Title (optional)"]"/>
                    <span asp-validation-for="Title" class="text-danger"></span>
                </div>
            }

            <textarea asp-for="InputMarkdown" class="form-control" id="markdown-editor"
                        placeholder="@Localizer["Type your Markdown here..."]"></textarea>
            <span asp-validation-for="InputMarkdown" class="text-danger"></span>
        </div>
    </div>
</div>
```

这样，在编辑模式下，用户可以看到一个标题输入框，可以为他们的文档添加一个标题。

当然，最核心的功能，也就是查看自己的文档列表，仍然没有实现。我们将在下一步中实现这个功能。

## Step 5.3 创建用户文档列表页面

在 `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` 文件中，添加以下代码：

```csharp
[Authorize]
[RenderInNavBar(
    NavGroupName = "Features",
    NavGroupOrder = 1,
    CascadedLinksGroupName = "Home",
    CascadedLinksIcon = "history",
    CascadedLinksOrder = 2,
    LinkText = "My documents",
    LinkOrder = 2)]
public async Task<IActionResult> History()
{
    var userId = userManager.GetUserId(User);
    var documents = await context.MarkdownDocuments
        .Where(d => d.UserId == userId)
        .OrderByDescending(d => d.CreationTime)
        .ToListAsync();

    var model = new HistoryViewModel
    {
        MyDocuments = documents
    };
    return this.StackView(model);
}
```

它的功能正是从数据库中查询当前用户的所有文档，并按创建时间降序排列。然后将这些文档传递给视图进行渲染。

其中，`[RenderInNavBar]` 属性用于将这个方法渲染到导航栏中。这样用户就可以通过导航栏访问他们的文档列表。

创建文件 `./src/MyOrg.MarkToHtml/Models/HomeViewModels/HistoryViewModel.cs`，添加以下代码：

```csharp
using Aiursoft.UiStack.Layout;
using MyOrg.MarkToHtml.Entities;

namespace MyOrg.MarkToHtml.Models.HomeViewModels;

public class HistoryViewModel : UiStackLayoutViewModel
{
    public HistoryViewModel()
    {
        PageTitle = "My Documents History";
    }

    public IEnumerable<MarkdownDocument> MyDocuments { get; set; } = new List<MarkdownDocument>();
}
```

创建文件 `./src/MyOrg.MarkToHtml/Views/Home/History.cshtml`，添加以下代码：

```html
@using Aiursoft.WebTools
@model MyOrg.MarkToHtml.Models.HomeViewModels.HistoryViewModel
@inject IViewLocalizer Localizer

<style>
    .clickable-row {
        cursor: pointer;
    }
</style>

<div class="row mb-2 mb-xl-3">
    <div class="col-auto d-none d-sm-block">
        <h3>@Localizer["My Documents"]</h3>
    </div>

    <div class="col-auto ms-auto mt-n1">
        <a asp-controller="Home" asp-action="Index" class="btn btn-primary">
            <i class="align-middle" data-lucide="file-plus"></i> @Localizer["Create a new document"]
        </a>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h5 class="card-title">@Localizer["All My Documents"]</h5>
        <h6 class="card-subtitle text-muted">@Localizer["A list of all documents you have created."]</h6>
    </div>
    <div class="table-responsive">
        <table class="table table-hover mb-0">
            <thead>
            <tr>
                <th>@Localizer["Title"]</th>
                <th>@Localizer["Creation Time"]</th>
                <th>@Localizer["Length"]</th>
                <th class="text-end">@Localizer["Actions"]</th>
            </tr>
            </thead>
            <tbody>
            @foreach (var doc in Model.MyDocuments)
            {
                <tr class="clickable-row" data-href="@Url.Action("Edit", new { id = doc.Id })">
                    <td>
                        @if (string.IsNullOrWhiteSpace(doc.Title))
                        {
                            <label class="text-muted">(no title)</label>
                        }
                        else
                        {
                            @doc.Title
                        }
                    </td>
                    <td>
                        <label class="text-muted" data-utc-time="@doc.CreationTime.ToHtmlDateTime()"></label>
                    </td>
                    <td>@(doc.Content?.Length ?? 0)</td>
                    <td class="text-end">
                        <a asp-action="Edit" asp-route-id="@doc.Id" class="btn btn-sm btn-outline-primary">
                            <i class="align-middle" data-lucide="edit-2"></i> @Localizer["Edit"]
                        </a>
                        <a asp-action="Delete" asp-route-id="@doc.Id" class="btn btn-sm btn-outline-danger">
                            <i class="align-middle" data-lucide="trash-2"></i> @Localizer["Delete"]
                        </a>
                    </td>
                </tr>
            }
            </tbody>
        </table>
    </div>
</div>

@* ReSharper disable once Razor.SectionNotResolved *@
@section scripts {
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const rows = document.querySelectorAll(".clickable-row");
            rows.forEach(row => {
                row.addEventListener("click", function (event) {
                    const target = event.target;
                    // Prevent navigation if a link or button was clicked inside the row
                    if (!target.matches('a, a *, button, button *')) {
                        window.location.href = row.dataset.href;
                    }
                });
            });
        });
    </script>
}
```

这个视图使用了一个表格来显示用户的所有文档。每一行显示文档的标题、创建时间、内容长度以及操作按钮（编辑和删除）。点击行可以导航到编辑页面。

注意，其中我们使用了一个技巧：`data-utc-time` 属性来存储 UTC 时间。Aiursoft Template 自带的 JavaScript 会自动将其转换为用户本地时间并显示。还记得我们在设计实体的时候是如何定义这个 `CreationTime` 属性的吗？当时的代码是：

```csharp
public DateTime CreationTime { get; init; } = DateTime.UtcNow;
```

所以这个实体本身创建的时候，就已经将当时的 UTC 时间存储在数据库里了。而转换为当地时区是靠 JavaScript 在用户的设备上实现的。这样可以确保无论用户来自哪个时区，显示的时间都是当地的时间。

最后，为了方便用户在编辑页面能够返回到他们的文档列表，我们在 `./src/MyOrg.MarkToHtml/Views/Home/Index.cshtml` 文件中，找到提交按钮，在它左侧添加一个返回按钮：

```html
    @* Submit Button Row *@
    <div class="row mt-3">
        <div class="col text-center">
            @if ((User.Identity?.IsAuthenticated ?? false) && Model.IsEditing)
            {
                <a asp-action="History" class="btn btn-outline-secondary btn-lg mr-2">
                    <i class="align-middle" data-lucide="file-text">&nbsp;</i>
                    @Localizer["My Documents"]
                </a>
            }

            <button type="submit" class="btn btn-primary btn-lg">
                @if (User.Identity?.IsAuthenticated ?? false)
                {
                    <i class="align-middle" data-lucide="check-circle">&nbsp;</i>
                    @Localizer["Convert and save"]
                }
                else
                {
                    <i class="align-middle" data-lucide="chevrons-right">&nbsp;</i>
                    @Localizer["Convert to HTML"]
                }
            </button>
        </div>
    </div>
```

这样，用户在编辑他们的文档时，可以方便地返回到他们的文档列表页面。

现在，不会再有错误了。你可以运行应用程序，在匿名模式下，只能创建并查看 HTML。而在登录后，你可以创建、编辑和查看你自己的文档列表。

> 默认用户是 `admin`，默认密码是 `admin123`。

当然，我们还没有实现删除文档的功能。我们将在下一步中实现这个功能。

## Step 5.4 实现删除文档的功能

在完成了创建、编辑、列表等功能后，删除自然已经是最后一个需要实现的功能了。到这里，我们已经熟练掌握了如何使用 Entity Framework Core 来操作数据库中的数据。删除文档的功能也不例外。你可以试试自己实现它，或者参考下面的代码。

在 `./src/MyOrg.MarkToHtml/Controllers/HomeController.cs` 文件中，添加以下代码：

```csharp
// GET: /Home/Delete/{guid}
[Authorize]
public async Task<IActionResult> Delete(Guid? id)
{
    if (id == null)
    {
        return NotFound();
    }

    var userId = userManager.GetUserId(User);
    var document = await context.MarkdownDocuments
        .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

    if (document == null)
    {
        // Document not found or user does not have permission.
        return NotFound();
    }

    return this.StackView(new DeleteViewModel
    {
        Document = document
    });
}

// POST: /Home/Delete/{guid}
[HttpPost, ActionName("Delete")]
[ValidateAntiForgeryToken]
[Authorize]
public async Task<IActionResult> DeleteConfirmed(Guid id)
{
    var userId = userManager.GetUserId(User);
    var document = await context.MarkdownDocuments
        .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

    if (document == null)
    {
        return NotFound();
    }

    context.MarkdownDocuments.Remove(document);
    await context.SaveChangesAsync();

    logger.LogInformation("Document with ID: '{Id}' was deleted by user: '{UserId}'.", id, userId);

    return RedirectToAction(nameof(History));
}
```

同时创建 `./src/MyOrg.MarkToHtml/Models/HomeViewModels/DeleteViewModel.cs` 文件，添加以下代码：

```csharp
using Aiursoft.UiStack.Layout;
using MyOrg.MarkToHtml.Entities;

namespace MyOrg.MarkToHtml.Models.HomeViewModels;

public class DeleteViewModel : UiStackLayoutViewModel
{
    public DeleteViewModel()
    {
        PageTitle = "Delete Document";
    }

    // This property will hold the document to be deleted, so the view can display its details.
    public MarkdownDocument Document { get; set; } = null!;
}
```

创建 `./src/MyOrg.MarkToHtml/Views/Home/Delete.cshtml` 文件，添加以下代码：

```html
@using Aiursoft.WebTools
@model MyOrg.MarkToHtml.Models.HomeViewModels.DeleteViewModel
@inject IViewLocalizer Localizer

<h1 class="h3 mb-3">@Localizer["Delete Document"]</h1>

<div class="row justify-content-center">
    <div class="col-lg-10 col-xl-8">
        <div class="card">
            <div class="card-header text-center">
                <i class="align-middle text-danger" data-lucide="shield-alert" style="width: 48px; height: 48px;"></i>
            </div>
            <div class="card-body">
                <div class="text-center">
                    <h2 class="h4 card-title fw-bold">@Localizer["Are you sure?"]</h2>
                    <p class="mb-3 text-muted">@Localizer["This action is irreversible. You are about to permanently delete the following document:"]</p>
                </div>

                <div class="list-group list-group-flush my-4">
                    <div class="list-group-item">
                        <div class="row">
                            <strong class="col-sm-3">@Localizer["Title"]</strong>
                            <div class="col-sm-9">
                                @if (string.IsNullOrWhiteSpace(Model.Document.Title))
                                {
                                    <label class="text-muted">(no title)</label>
                                }
                                else
                                {
                                    @Model.Document.Title
                                }
                            </div>
                        </div>
                    </div>
                    <div class="list-group-item">
                        <div class="row">
                            <strong class="col-sm-3">@Localizer["Creation Time"]</strong>
                            <div class="col-sm-9">
                                <label data-utc-time="@Model.Document.CreationTime.ToHtmlDateTime()" class="text-monospace"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="text-center">
                    <form asp-action="Delete" class="d-inline-block">
                        <input type="hidden" asp-for="@Model.Document.Id" />
                        <button type="submit" class="btn btn-danger">
                            <i class="align-middle me-2" data-lucide="trash-2"></i> @Localizer["Yes, delete this document"]
                        </button>
                    </form>
                    <a asp-action="History" class="btn btn-light">@Localizer["Cancel"]</a>
                </div>
            </div>
        </div>
    </div>
</div>
```

这个视图显示了一个确认删除的页面，列出了要删除的文档的标题和创建时间，并提供了确认和取消按钮。

## 结语

恭喜你完成了第五步！你现在已经成功地实现了一个完整的 CRUD（创建、读取、更新、删除）功能，允许用户创建、编辑、查看和删除他们的 Markdown 文档。

通过合理地使用 Entity Framework Core，你可以轻松地操作数据库中的数据，而不必担心手动编写 SQL 语句，也不必担心数据库结构与实体类不一致的问题。

在上面的过程中，我们巧妙的将创建和编辑共享了同一个视图，这样可以减少代码重复，提高代码的可维护性。同时我们还对于匿名用户和已经认证的用户做了不同处理，确保匿名用户可以匿名使用，而认证用户则可以享受更多的功能。

现在运行应用程序，尝试创建、编辑、查看和删除你的文档，体验一下完整的功能吧！

# Aiursoft Template Tutorial - Step 6 - 管理员看板和全新的权限

作为站长，你可能希望有一个专门的管理员看板，用于管理用户和内容。你也可能希望有一些特殊的权限设置，例如调整一篇文档的所有者，或者让某些用户拥有更高的权限。我们将在这一步中实现这些功能。

# Aiursoft Template Tutorial - Step 7 - 增加全新的配置项目，并支持环境变量

# Aiursoft Template Tutorial - Step 8 - 添加自定义验证

# Aiursoft Template Tutorial - Step 9 - 允许用户在前端上传文件

# Aiursoft Template Tutorial - Step 10 - 软删除和回收站，基于后台任务

# Aiursoft Template Tutorial - Step 11 - 本地化应用以面向全球用户

# Aiursoft Template Tutorial - Step 12 - 发布应用到真实的服务器

# Aiursoft Template Tutorial - Step 13 - 课后练习

这部分留给你自己完成。你可以尝试添加更多的功能。到这里以后，相信完成下面的功能对你来说已经不再是难事了。

这些功能不仅能极大地丰富你的应用，还能让你在实践中深入掌握更多关于数据库设计、后端架构、前端交互和性能优化的专业知识。祝你玩得开心！

## Step 12.1 Markdown 支持多种隐私选项

现在，Markdown 保存好了以后只能自己看。我们可以尝试添加更多的隐私选项，例如：

* 公开：任何人都可以查看这个文档。
* 私密：只有自己可以查看这个文档。
* 不出现在列表中：只有知道链接的人才能查看这个文档。
* 密码保护：访问这个文档需要输入密码。
* 分享给特定的用户组：只有特定的用户组可以查看这个文档。

## Step 12.2 支持其它格式

除了 Markdown，我们还可以支持更多的格式，例如：

* Mermaid：一种用于绘制图表和流程图的文本格式。
* LaTeX：一种用于排版数学公式和科学文档的标记语言。
* HTML：直接输入 HTML 代码，并渲染成网页。
* 富文本格式（WYSIWYG）：允许用户使用类似 Word 的编辑器来创建和编辑文档。

## Step 12.3 搜索

我们可以尝试实现搜索功能，允许用户根据标题或内容搜索他们的文档。可以使用全文索引或者简单的字符串匹配来实现这个功能。甚至可以支持模糊搜索和高级搜索选项。

## Step 12.4 文档版本历史与回滚

用户在编辑文档时，可能会误删重要内容或想找回之前的某个版本。实现一个版本控制系统，让每一次保存都成为一个可追溯的历史记录。

这需要妥善的设计数据结构，例如：

* 可以每次提交都完整的保存一份文档的快照，这样方便实现，并且可以支持任意版本的回滚。但缺点是会占用较多的存储空间。
* 也可以只保存每次修改的差异（diff），这样节省存储空间，但实现起来相对复杂一些。

## Step 12.5 高级组织：文件夹与标签系统

当文档数量增多时，一个扁平的列表将变得难以管理。引入文件夹和标签来帮助用户组织他们的文档。

这需要妥善设计数据库结构，例如：

* 文件夹表：存储文件夹信息，如名称、创建时间、用户ID等。
* 标签表：存储标签信息，如名称、颜色等。
* 文档-标签关联表：实现多对多关系，允许一个文档有多个标签。
* 文档-文件夹关联：允许一个文档属于一个文件夹。
* 用户-文件夹关联：允许用户创建和管理自己的根文件夹。

## Step 12.6 性能优化：分页加载

如果一个用户有成百上千篇文档，“我的文档”页面一次性加载所有文档会导致页面加载缓慢，并给服务器和数据库带来压力。通过分页加载，只加载当前页的文档，提升用户体验。

这需要为列表页面增加两个参数 `page` 和 `pageSize`，并在数据库查询时使用 `Skip` 和 `Take` 方法来实现分页。它们会被翻译成 SQL 语句中的 `OFFSET` 和 `LIMIT`，从而只查询需要的数据。

## Step 12.7 支持 PostgreSQL

我们已经支持了 SQLite 和 MySQL，现在可以尝试添加对 PostgreSQL 的支持。PostgreSQL 是一个功能强大且广泛使用的开源关系型数据库管理系统。通过添加对 PostgreSQL 的支持，可以让应用程序适应更多的部署环境和用户需求。

Aiursoft Template 的设计中，不需要修改任何核心代码，就可以轻松地添加对新的数据库的支持。你只需要模仿 MySql、Sqlite 的实现，创建一个新的 PostgreSql 支持类，并确保在配置文件中正确设置连接字符串和数据库类型即可。
