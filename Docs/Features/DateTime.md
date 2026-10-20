# 🕒 Master Time: The Ultimate UTC Strategy to Solve Timezone Issues

Handling time in web development is a classic pitfall.

  * If your server is in **London** and users are in **Tokyo**.
  * Rendering `DateTime.Now.ToString()` directly on the backend shows users the London time, not their local Tokyo time. This confuses users.

**Principle:** The server should never guess the user's timezone. The server only transmits **UTC (Coordinated Universal Time)**, leaving it to the user's browser (JavaScript) to convert it into local time.

## ❌ Incorrect Approach: Direct Rendering

```html
<span>@doc.CreationTime.ToString("yyyy-MM-dd HH:mm")</span>
```

## ✅ Correct Approach: UTC Placeholder + JS Conversion

In Aiursoft Template, we use the `data-utc-time` attribute in conjunction with built-in JavaScript code to automatically perform the conversion.

### Step 1: Store UTC Only on the Backend

When defining entities (Entity), ensure all date fields are initialized with `DateTime.UtcNow`.

```csharp title="MarkdownDocument.cs"
public class MarkdownDocument
{
    // ...
    // 数据库和内存中，永远只存储纯净的 UTC 时间
    public DateTime CreationTime { get; init; } = DateTime.UtcNow; 
}
```

### Step 2: Use Placeholder Tags in the Frontend

In the view (View), do not output text directly. You need to use the extension method `.ToHtmlDateTime()` provided by `Aiursoft.WebTools` and place the result in the `data-utc-time` attribute.

Please refer to the following implementation in `History.cshtml`:

```html
@using Aiursoft.WebTools
@model MyOrg.MarkToHtml.Models.HomeViewModels.HistoryViewModel
@inject IViewLocalizer Localizer

<div class="table-responsive">
    <table class="table table-hover mb-0">
        <thead>
        <tr>
            <th>@Localizer["Title"]</th>
            <th>@Localizer["Creation Time"]</th> <th>@Localizer["Length"]</th>
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
                
                </tr>
        }
        </tbody>
    </table>
</div>

```

## ⚙️ How does it work?

1. **Backend**: `@doc.CreationTime.ToHtmlDateTime()` formats a C# `DateTime` object into a standard ISO 8601 string (e.g., `2023-10-05T14:30:00Z`).
2. **Transmission**: When the HTML is sent to the browser, the `<label>` element is empty but carries the attribute `data-utc-time="2023-10-05T14:30:00Z"`.
3. **Frontend**: The global JavaScript script included in the Template (located in `aiursoft/uistack`) scans all `[data-utc-time]` elements in the page when `DOMContentLoaded` fires.
4. **Calculation**: The JS retrieves the browser's timezone information (e.g., `Asia/Shanghai`) and adds +8 hours to the UTC time.
5. **Rendering**: The JS modifies the DOM, writing the converted local time (e.g., `2023-10-05 22:30:00`) into the text content of the `<label>`.

**Summary:** Using `data-utc-time`, you can ensure that no matter where your users are—New York, London, or Beijing—they always see the correct time in their own current timezone, without needing complex timezone logic in the backend.
