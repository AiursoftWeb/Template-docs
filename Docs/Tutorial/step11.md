# Step 11 - Let the App Speak Another Language

**Our goal:** generate one language, select it in the browser, and check the new pages.
English stays the source language. We will generate resources, not write a second set of views.

Stop the server with **Ctrl+C** before changing resource files.

## 11.1 Check that our text can be found

The tool looks for literal English keys such as this one:

```cshtml
<h1>@Localizer["Recycle bin"]</h1>
```

Our Uploads and RecycleBin views already use this pattern.
The validation model uses the template's DataAnnotations localization support.

Keep browser scripts in separate JavaScript files.
Step 3's hidden HTML attributes carry translated messages to that script.
A JavaScript file cannot evaluate Razor syntax.

## 11.2 Prepare the translation tool

```bash
cd ~/Source/MyOrg.MarkToHtml
```

This returns to the repository root.

```bash
dotnet tool install --global Aiursoft.Dotlang
```

This installs the existing resource-generation tool.
**Expected:** a successful installation message. An already-installed message is fine.

```bash
cd src/MyOrg.MarkToHtml
```

This selects the web project, where the tool can find our csproj.
Do not run these commands in the solution root.

```bash
pwd
```

**Expected:** a path ending in `/src/MyOrg.MarkToHtml`.

## 11.3 Get your own translation access

The following example uses Aiursoft's Ollama-compatible localization endpoint.
You need an authorized API token and access to its localization model.

If you develop outside Aiursoft, substitute your own endpoint and model.
If you do not have access yet, pause this exercise here; the English app still works.
Do not borrow a deployed application's token.

```bash
read -rsp 'Ollama API token: ' OLLAMA_API_KEY
```

This waits for you to paste your own token and press Enter.
The token is not shown while you type. That is intentional.

```bash
printf '\n'
```

This prints a newline so the next terminal output starts on a fresh line.
It does not print the token.

Do not enable shell tracing, take process listings during translation, or commit the token.
The tool receives it as a command argument while it runs.

## 11.4 Generate one kind of resource at a time

```bash
dotlang auto-generate-view-injections-for-aiursoft-template --path .
```

This adds discoverable page-title and navigation keys to the template's existing injector.
`--path .` means the current web-project folder.
**Expected:** the tool reports the strings it found or added.

```bash
dotlang generate-resx-csharp --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
```

This translates C# Localizer keys for Simplified Chinese.
`--languages zh-CN` limits this first exercise to one language.
`--model` and `--instance` choose the authorized model and endpoint.
`-c 2` limits concurrent translation work to two requests.

```bash
dotlang generate-resx-view --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
```

This translates keys from Razor views, including the two new pages.
**Expected:** view resource files under Resources, with translated values.
It can take a while. Wait for the prompt to return.

```bash
dotlang generate-resx-annotations --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
```

This handles display and validation annotations.
Check the actual generated resources; an exit code alone does not prove a key was found.

```bash
dotlang auto-dedup-resx-keys --path .
```

This removes redundant resource keys using the tool's existing rules.
Review its changes along with the generated files.

```bash
unset OLLAMA_API_KEY
```

This removes the token variable from this terminal.
Do this after the generation commands, including when a command fails and you decide to stop.

## Checkpoint 11A - Resources actually exist

In the editor, look under Resources for the generated view files.
Check both Uploads/Index and RecycleBin/Index.

Find the keys `Upload a note image` and `Recycle bin`.
Their zh-CN values should be translated, not empty.

Check the controller, page-title, and annotation resources too.
Keep format placeholders such as `{0}` intact.

Review the diff. The tool can change source injections as well as resx files.
Do not handwrite parallel translation files to hide a missing extraction result.

## Checkpoint 11B - See the language in the app

```bash
cd ../..
```

This returns from the web project to the repository root.

```bash
dotnet build ./MyOrg.MarkToHtml.sln
```

This compiles the generated resources into the application.
**Expected:** a successful build.

```bash
dotnet run --project ./src/MyOrg.MarkToHtml/MyOrg.MarkToHtml.csproj
```

This starts the newly built app.

In the browser:

1.

Sign in and open the language selector.
2.

Select Simplified Chinese.
3.

Open Uploads and RecycleBin.

Check that the headings changed.
4.

Check the page title, validation feedback, and editor Copy feedback.
5.

Switch back to English and confirm the same actions still work.

A changed language code alone is not success. Read the visible text.
English fallback means a resource may be missing; investigate that key.

Save the reviewed injections and generated resources together in Git.
Press **Ctrl+C** when you are done checking.

Continue with [Step 12](./step12.md).
