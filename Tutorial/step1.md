# 开始之前

这里是 Aiursoft Template 的快速入门教程。我们都知道，开始一个新项目可能会很麻烦，所以我们准备了这个教程来帮助你快速上手。

这个教程预计需要 30 分钟。在你完成后，你将拥有一个功能齐全的项目，可以作为你未来项目的基础。我们为了展示，将简单开发一个美观、带多数据库、RBAC、本地化、OIDC接入、单元测试、Docker部署的 markdown 转 HTML 的简单笔记应用。

我们强烈建议你不要跳过任何步骤以确保体验完整。祝你这段 30 分钟的历险旅程顺利，并且快速成为一位 Aiursoft Template 大师，圆梦 Web 开发！

# Aiursoft Template Tutorial - Step 1 - 创建新项目

## Step 1.1 准备开发环境

第一步的目标是创建一个全新的项目。我们推荐你使用 [AnduinOS](https://www.anduinos.com) 来进行实战开发，因为 AnduinOS 非常容易安装 dotnet、bash、npm、git、docker、mysql、nginx 等工具。

如果你不想使用 AnduinOS，你也可以在任何支持 .NET 8.0 的操作系统上进行开发。

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

你会注意到，在上面的命令执行完成后，`MyOrg.MarkToHtml.csproj` 文件中添加了对 Markdig 的引用，它看起来可能像这样：

```xml
<ItemGroup>
  <PackageReference Include="Markdig" Version="0.42.0" />
</ItemGroup>
```

接下来，我们额外安装一个能够避免生成的 HTML 被 XSS 攻击的库，叫做 [HtmlSanitizer](https://github.com/mganss/HtmlSanitizer)。你可以使用以下命令来安装它：

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet add package HtmlSanitizer
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

可以注意到，所有潜在的 XSS 攻击向量都被移除了。

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

## 结语

恭喜你完成了第二步！你现在已经成功地添加并测试了第三方库 Markdig 和 HtmlSanitizer。通过合理地使用 Nuget、GitHub，你可以轻松将前人的工作成果整合到你的项目中，并快速扩充你的项目功能。

# Aiursoft Template Tutorial - Step 3 - 添加全新的页面

# Aiursoft Template Tutorial - Step 4 - 在 Docker 里运行和发布应用

# Aiursoft Template Tutorial - Step 5 - 添加全新的数据模型并改变数据库结构

# Aiursoft Template Tutorial - Step 6 - 将数据保存到数据库

# Aiursoft Template Tutorial - Step 7 - 增加全新的配置项目

# Aiursoft Template Tutorial - Step 8 - 本地化应用

# Aiursoft Template Tutorial - Step 9 - 发布应用到真实的服务器
