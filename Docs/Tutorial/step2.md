# Step 2 - Try the Libraries Before Building the Page

![Debugging a library in the editor](./images/rider-verify.png)

**Our goal:** convert a tiny Markdown example, clean unsafe HTML, and install CodeMirror.
We will connect these pieces to a page in Step 3.

First, stop the app with **Ctrl+C** if it is still running.

```bash
cd ~/Source/MyOrg.MarkToHtml
```

This returns to the repository root. We start each chapter here.

## 2.1 Add the two C# libraries

```bash
cd src/MyOrg.MarkToHtml
```

This moves into the web project, where `MyOrg.MarkToHtml.csproj` lives.

```bash
dotnet add MyOrg.MarkToHtml.csproj package Markdig
```

[Markdig](https://github.com/xoofx/markdig) converts Markdown into HTML.
This command adds its package reference to our web project.

**Expected:** a successful restore and a `PackageReference` for Markdig in the csproj.

```bash
dotnet add MyOrg.MarkToHtml.csproj package HtmlSanitizer
```

[HtmlSanitizer](https://github.com/mganss/HtmlSanitizer) removes unsafe HTML such as scripts.
The conversion library and sanitizer have different jobs; we need both.

**Expected:** another successful restore and a reference to HtmlSanitizer.
The exact current package versions may differ from screenshots.

## 2.2 Save the original entry point

We are about to use `Program.cs` as a tiny scratch program.
This is temporary. Let's save the real startup code first.

```bash
cp Program.cs Program.cs.before-library-test
```

`cp` copies the file. Our backup has no `.cs` extension, so it will not be compiled.
**Expected:** both files are visible in the web-project folder.

Do not skip the backup. We need it to restore logging, database startup, and the web server.

## 2.3 Try Markdig

Open `src/MyOrg.MarkToHtml/Program.cs` in the editor.
Temporarily replace the **whole file** with this small program:

```csharp
using Markdig;

namespace MyOrg.MarkToHtml;

public abstract class Program
{
    public static void Main(string[] args)
    {
        var markdown = "# Hello World\n\nThis is my first conversion.";
        var pipeline = new MarkdownPipelineBuilder().UseAdvancedExtensions().Build();
        var html = Markdown.ToHtml(markdown, pipeline);
        Console.WriteLine(html);
    }
}
```

Save the file. In the terminal, we are still in `src/MyOrg.MarkToHtml`.

```bash
dotnet run --project MyOrg.MarkToHtml.csproj
```

This runs our temporary program.
**Expected:** an `<h1>` and a `<p>` printed in the terminal, then the prompt returns.

No website opens in this exercise. We temporarily replaced the web-server startup.

## Checkpoint 2A - Markdown becomes HTML

Look for `Hello World` inside an HTML heading.
That is the result from Markdig. Good; the first piece works.

## 2.4 Try the sanitizer

Replace the **whole temporary Program.cs** again:

```csharp
using Ganss.Xss;

namespace MyOrg.MarkToHtml;

public abstract class Program
{
    public static void Main(string[] args)
    {
        var sanitizer = new HtmlSanitizer();
        var unsafeHtml = "<h1>Hello</h1><script>alert('xss')</script>";
        Console.WriteLine(sanitizer.Sanitize(unsafeHtml));
    }
}
```

Save the file.

```bash
dotnet run --project MyOrg.MarkToHtml.csproj
```

This runs the sanitizer example.
**Expected:** `<h1>Hello</h1>`, with no `<script>` or `alert` left in the output.

## Checkpoint 2B - Unsafe script content is removed

The heading stays. The script goes away.
We will use the same order in the real service: convert first, sanitize second.

## 2.5 Put the real startup code back

```bash
mv Program.cs.before-library-test Program.cs
```

`mv` moves the backup back to its original name, replacing the scratch program.
The application can now start its web server again.

If you retried this chapter and the backup is missing, stop here.
Do not run this command twice or invent a shortened startup file.
Recover the original generated Program.cs from Git before continuing.

## 2.6 Install the browser editor

```bash
cd wwwroot
```

This enters the frontend folder from the web-project folder.

```bash
npm install codemirror@5 --save
```

This downloads CodeMirror 5 and records the dependency.
`@5` matters: the page in the next chapter uses the CodeMirror 5 API.

Now open `src/MyOrg.MarkToHtml/wwwroot/package.json` in the editor.
Find the existing `keep` object.
Add `"codemirror": "."` after `dropify`, including the comma between entries.

The **keep object only** should now look like this:

```json
"keep": {
  "dropify": "dist",
  "codemirror": "."
}
```

Keep the surrounding `dependencies` and `scripts` sections.
This small block is not a replacement for the whole package.json file.

Why add this? The frontend build removes files it does not need.
The dot tells it to keep CodeMirror's library, themes, modes, and addons.
Without this entry, the editor could work locally and disappear from the Docker image.

```bash
npm run build
```

This runs the template's normal frontend build, including its file pruning.
**Expected:** the command finishes successfully.

Let's check the three files we will need:

```bash
ls node_modules/codemirror/lib/codemirror.js
```

This checks that the editor's JavaScript survived. **Expected:** the file's path.

```bash
ls node_modules/codemirror/lib/codemirror.css
```

This checks its stylesheet. **Expected:** the file's path.

```bash
ls node_modules/codemirror/mode/markdown/markdown.js
```

This checks the Markdown mode. **Expected:** the file's path.
If a check says `No such file`, revisit the keep object before continuing.

```bash
cd ../../..
```

This returns to the repository root.

```bash
dotnet build ./MyOrg.MarkToHtml.sln
```

This checks that the real application still compiles after restoring Program.cs.
**Expected:** `Build succeeded.`

## Checkpoint 2C - Ready to build a page

Check these before moving on:

- Both scratch programs produced the expected output.
- Program.cs contains the original startup code again.
- Both C# packages are referenced by the web project.
- CodeMirror's JavaScript, CSS, and Markdown mode still exist after the frontend build.

Keep the changes to **both** package.json and package-lock.json.
The lock file records the resolved frontend dependencies.

Well done. Now let's [put the conversion on a page](./step3.md).
