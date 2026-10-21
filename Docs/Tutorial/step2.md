# Aiursoft Template Tutorial - Step 2 - Add and Debug Third-Party Libraries

![rider-verify](./images/rider-verify.png)

## Step 2.1 Add Third-Party Library

Obviously, our original task is to create an application that converts markdown to HTML. For this purpose, we need a library capable of converting markdown to HTML.

In this tutorial, we choose [Markdig](https://github.com/xoofx/markdig). It is a powerful and easy-to-use markdown parser.

To install Markdig, we need to use the NuGet package manager. You can use the following command to install it:

```bash
cd ./src/MyOrg.MarkToHtml/
dotnet add MyOrg.MarkToHtml.csproj package Markdig
```

Next, we'll install an additional library that prevents the generated HTML from being vulnerable to XSS attacks, called [HtmlSanitizer](https://github.com/mganss/HtmlSanitizer). You can install it using the following command:

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet add MyOrg.MarkToHtml.csproj package HtmlSanitizer
```

You will notice that after the above command is executed, references to Markdig and HtmlSanitizer have been added to the `MyOrg.MarkToHtml.csproj` file, which might look like this:

```xml title="MyOrg.MarkToHtml.csproj"
<ItemGroup>
    <PackageReference Include="HtmlSanitizer" Version="9.0.886" />
    <PackageReference Include="Markdig" Version="0.42.0" />
</ItemGroup>
```

## Step 2.2 Test the functionality of third-party libraries (optional)

!!! tip "This step is entirely optional"

    This step is entirely optional and is intended to demonstrate how to debug third-party libraries. If you trust that Markdig will work properly, you can skip this step.

Before changing `Program.cs`, save its original contents:

```bash
# Working directory: src/MyOrg.MarkToHtml
cp Program.cs Program.cs.before-library-test
```

Next, we need to first test whether Markdig and HtmlSanitizer can function correctly. To do this, directly modify the `./src/MyOrg.MarkToHtml/Program.cs` file, temporarily comment out the original content in the `Main` method, and temporarily add the following code for testing Markdig:

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

Next, we can run the project again to test whether Markdig works properly:

```bash
# cd ./src/MyOrg.MarkToHtml/
dotnet run --project MyOrg.MarkToHtml.csproj
```

You might see output similar to the following:

```html
<h1 id="hello-world">Hello World</h1>
<p>This is a sample markdown text.</p>
<blockquote>
<p>This is a blockquote.</p>
</blockquote>
```

This proves that Markdig can successfully convert markdown to HTML. Next, we continue testing HtmlSanitizer.

We can modify the test code in the `Program.cs` file to include the use of HtmlSanitizer:

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

This time, the expected output will be:

```html
<div style="background-color: rgba(0, 0, 0, 1)">Test<img src="https://www.example.com/test.png" style="margin: 10px"></div>
```

It can be noticed that all potential XSS attack vectors have been removed. This demonstrates that HtmlSanitizer successfully cleans HTML.

## Step 2.3 Restore the Program.cs file

Restore the saved entry point, including its database, logging and initialization calls:

```bash
# Working directory: src/MyOrg.MarkToHtml
mv Program.cs.before-library-test Program.cs
```

Do not replace the entry point with a shortened version: the generated startup sequence can contain additional initialization required by the template.

## Step 2.4 Install the frontend code editor

Considering we need to provide users with the ability to edit Markdown and preview HTML on the frontend page, we need a powerful frontend code editor. We choose [CodeMirror 5](https://codemirror.net/) as our frontend code editor.

To install CodeMirror 5, we need to use the npm package manager. You can use the following command to install it:

```bash
cd wwwroot/ # From src/MyOrg.MarkToHtml after restoring Program.cs
npm install codemirror@5 --save
```

The current frontend build removes packages that are not listed in `package.json`'s `keep` map. Add CodeMirror while preserving the existing dependencies, scripts and keep entries:

```bash
# Still in src/MyOrg.MarkToHtml/wwwroot
node --input-type=module -e 'import fs from "node:fs"; const p=JSON.parse(fs.readFileSync("package.json","utf8")); p.keep={...p.keep,codemirror:"."}; fs.writeFileSync("package.json",JSON.stringify(p,null,2)+"\n");'
npm run build
test -f node_modules/codemirror/lib/codemirror.js
test -f node_modules/codemirror/lib/codemirror.css
test -f node_modules/codemirror/mode/markdown/markdown.js
cd ../../..  # Repository root
```

Keeping `codemirror: "."` includes the library, modes, addons and themes used in the next chapter. Review and commit both `package.json` and `package-lock.json`. Development success after `npm install` alone does not verify the Docker frontend build.

## Conclusion

Congratulations on completing Step 2! You have now successfully added and tested the third-party libraries Markdig, HtmlSanitizer, and CodeMirror. By properly utilizing Nuget, npm, and GitHub, you can easily integrate the work of others into your project and quickly expand your project's functionality.
