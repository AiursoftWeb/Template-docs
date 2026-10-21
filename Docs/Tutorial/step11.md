# Step 11 - Localize the Application

Keep English as the source language. The template already supports view localization and localized validation. Translate resources for the existing application rather than adding translated copies of controllers or views.

## 11.1 Make new strings discoverable

The views in this tutorial use literal keys, for example:

```cshtml
<h1>@Localizer["Recycle bin"]</h1>
```

Use localized DataAnnotations as shown in [Model Validation](../Features/Validation.md). New page titles and permission labels must also be discoverable through the existing view-model injection and permission definitions. Do not build localization keys from user input.

JavaScript stays in separate files. Pass localized messages through hidden HTML or data attributes, as in Step 3; a JavaScript file containing `@Localizer[...]` is not processed by Razor.

## 11.2 Generate one language first

Install the existing translation tool:

```bash
dotnet tool install --global Aiursoft.Dotlang
```

Open a Bash shell in `src/MyOrg.MarkToHtml` (the directory containing the web csproj). Obtain your own authorized Ollama endpoint, model and API token. The following uses the Aiursoft localization endpoint as an example; substitute your own values if you are developing outside Aiursoft.

```bash
# Working directory: src/MyOrg.MarkToHtml
read -rsp 'Ollama API token: ' OLLAMA_API_KEY
printf '\n'
dotlang auto-generate-view-injections-for-aiursoft-template --path .
dotlang generate-resx-csharp --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
dotlang generate-resx-view --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
dotlang generate-resx-annotations --path . --languages zh-CN --model aiursoft-localization:latest --token "$OLLAMA_API_KEY" --instance https://ollama.aiursoft.com/api/chat -c 2
dotlang auto-dedup-resx-keys --path .
unset OLLAMA_API_KEY
```

Do not enable shell tracing or commit the token. The token is passed as a CLI argument, so do not capture process listings while translation runs. These commands can modify source injections as well as resources: inspect the diff before committing. For larger language sets, expand `--languages` after verifying one language. Translation requires a reachable service and an authorized token; it is not an offline build step.

## 11.3 Verify the output

Inspect the generated `Resources` files for Home, Uploads and RecycleBin, and confirm that new labels such as `Recycle bin` and `Upload a note image` have translated values. A successful process exit is not evidence that every key was extracted. Check that DataAnnotations resources match their actual model type and that placeholders remain intact.

Build from the repository root, restart the app and select the target language from the language selector. Check navigation, page titles, form labels, invalid-input messages and the editor's Copy feedback. English fallback is expected for missing resources, but it is not proof that translation succeeded. Commit the generated resources and reviewed source injections together.

Continue with [Step 12](./step12.md).
