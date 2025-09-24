# 开始之前

这里是 Aiursoft Template 的快速入门教程。我们都知道，开始一个新项目可能会很麻烦，所以我们准备了这个教程来帮助你快速上手。

这个教程预计需要 30 分钟。在你完成后，你将拥有一个功能齐全的项目，可以作为你未来项目的基础。我们为了展示，将简单开发一个美观、带多数据库、RBAC、本地化、OIDC接入、单元测试、Docker部署的 markdown 转 HTML 的简单笔记应用。

我们强烈建议你不要跳过任何步骤以确保体验完整。祝你这段 30 分钟的历险旅程顺利，并且快速成为一位 Aiursoft Template 大师，圆梦 Web 开发！

# Aiursoft Template Tutorial - Step 1 - 创建新项目

## Step 1.1 准备开发环境

第一步的目标是创建一个全新的项目。我们推荐你使用 [AnduinOS](https://www.anduinos.com) 1.3 或更高版本来进行实战开发，因为 AnduinOS 1.3+ 非常容易安装 dotnet、bash、npm、git、docker、mysql、nginx 等工具。

如果你不想使用 AnduinOS，你也可以在任何支持 .NET 8.0 的操作系统上进行开发，例如 Windows、macOS 或其他 Linux 发行版。

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
cd ../../../ # 回到项目根目录
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

## Step 1.4 配置项目 (可选)

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

## Step 2.2 测试第三方库 (可选)

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
npm install codemirror@5
cd ../../../ # 回到项目根目录
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

            // --- jQuery Validation Setup ---
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
                themeToggleButton.addEventListener('click', function (event) {
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

# Aiursoft Template Tutorial - Step 5 - 将数据保存到数据库

# Aiursoft Template Tutorial - Step 6 - 管理员看板和全新的权限

# Aiursoft Template Tutorial - Step 7 - 增加全新的配置项目，并支持环境变量

# Aiursoft Template Tutorial - Step 8 - 添加自定义验证

# Aiursoft Template Tutorial - Step 9 - 允许用户在前端上传文件

# Aiursoft Template Tutorial - Step 10 - 本地化应用以面向全球用户

# Aiursoft Template Tutorial - Step 11 - 发布应用到真实的服务器
