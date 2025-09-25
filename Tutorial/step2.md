# Aiursoft Template Tutorial - Step 2 - 添加和调试第三方库

## Step 2.1 添加第三方库

显然，我们本来的任务是创建一个将 markdown 转换为 HTML 的应用。为此，我们需要一个能够将 markdown 转换为 HTML 的库。

在这个教程里，我们选择 [Markdig](https://github.com/xoofx/markdig)。这是一款功能强大且易于使用的 markdown 解析器。

为了安装 Markdig，我们需要使用 NuGet 包管理器。你可以使用以下命令来安装它：

```bash title="安装 Markdig"
cd ./src/MyOrg.MarkToHtml/
dotnet add package Markdig
```

接下来，我们额外安装一个能够避免生成的 HTML 被 XSS 攻击的库，叫做 [HtmlSanitizer](https://github.com/mganss/HtmlSanitizer)。你可以使用以下命令来安装它：

```bash title="安装 HtmlSanitizer"
# cd ./src/MyOrg.MarkToHtml/
dotnet add package HtmlSanitizer
```

你会注意到，在上面的命令执行完成后，`MyOrg.MarkToHtml.csproj` 文件中添加了对 Markdig 和 HtmlSanitizer 的引用，它看起来可能像这样：

```xml title="MyOrg.MarkToHtml.csproj"
<ItemGroup>
    <PackageReference Include="HtmlSanitizer" Version="9.0.886" />
    <PackageReference Include="Markdig" Version="0.42.0" />
</ItemGroup>
```

## Step 2.2 测试第三方库的工作能力 (可选)

!!! tip "这一步是完全可选的"

    这一步是完全可选的，是为了演示如何调试第三方库。如果你相信 Markdig 能够正常工作，可以跳过这一步。

接下来，我们需要先测试一下 Markdig 和 HtmlSanitizer 是否能正常工作。为此，我们直接修改 `./src/MyOrg.MarkToHtml/Program.cs` 文件，将 `Main` 方法原有内容暂时注释，然后暂时添加用于测试 Markdig 的以下代码：

```csharp title="测试 Markdig，Program.cs"
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

```html title="Markdig 输出"
<h1 id="hello-world">Hello World</h1>
<p>This is a sample markdown text.</p>
<blockquote>
<p>This is a blockquote.</p>
</blockquote>
```

这证明 Markdig 能够成功地将 markdown 转换为 HTML。接下来，我们继续测试 HtmlSanitizer。

我们可以修改 `Program.cs` 文件中的测试代码，添加对 HtmlSanitizer 的使用：

```csharp title="测试 HtmlSanitizer，Program.cs"
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

```html title="HtmlSanitizer 输出"
<div style="background-color: rgba(0, 0, 0, 1)">Test<img src="https://www.example.com/test.png" style="margin: 10px"></div>
```

可以注意到，所有潜在的 XSS 攻击向量都被移除了。说明 HtmlSanitizer 能够成功地清理 HTML。

## Step 2.3 恢复 `Program.cs` 文件

现在，我们测试完成了，回滚 `Program.cs` 文件中的更改，恢复原有内容：

```csharp title="恢复 Program.cs"
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

```bash title="安装 CodeMirror 5"
cd ./src/MyOrg.MarkToHtml/wwwroot/
npm install codemirror@5 --save
```

你会注意到，在上面的命令执行完成后，`./src/MyOrg.MarkToHtml/wwwroot/package.json` 文件中添加了对 CodeMirror 的引用，它看起来可能像这样：

```json title="package.json"
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
