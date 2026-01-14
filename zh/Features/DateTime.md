# 🕒 掌控时间：彻底解决时区问题的 UTC 策略

在 Web 开发中，处理时间是一个经典的陷阱。

  * 如果你的服务器在**伦敦**，用户在**东京**。
  * 你直接在后端渲染 `DateTime.Now.ToString()`，用户看到的是伦敦时间，而不是他自己的东京时间。这会让用户感到困惑。

**原则：** 服务器永远不要猜测用户的时区。服务器只负责传递 **UTC（世界协调时间）**，让用户的浏览器（JavaScript）负责翻译成当地时间。

## ❌ 错误做法：直接渲染

```html
<span>@doc.CreationTime.ToString("yyyy-MM-dd HH:mm")</span>
```

## ✅ 正确做法：UTC 占位 + JS 转换

在 Aiursoft Template 中，我们通过 `data-utc-time` 属性配合内置的 JavaScript 脚本来自动完成转换。

### 第一步：后端只存 UTC

在定义实体（Entity）时，确保所有的日期字段都初始化为 `DateTime.UtcNow`。

```csharp title="MarkdownDocument.cs"
public class MarkdownDocument
{
    // ...
    // 数据库和内存中，永远只存储纯净的 UTC 时间
    public DateTime CreationTime { get; init; } = DateTime.UtcNow; 
}
```

### 第二步：前端使用占位标签

在视图（View）中，不要直接输出文本。你需要使用 `Aiursoft.WebTools` 提供的扩展方法 `.ToHtmlDateTime()`，并将结果放入 `data-utc-time` 属性中。

请参考以下 `History.cshtml` 的实现：

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

## ⚙️ 它是如何工作的？

1.  **后端**：`@doc.CreationTime.ToHtmlDateTime()` 会将 C\# 的 `DateTime` 对象格式化为一个标准的 ISO 8601 字符串（例如 `2023-10-05T14:30:00Z`）。
2.  **传输**：HTML 发送到浏览器时，那个 `<label>` 标签里是空的，但带着属性 `data-utc-time="2023-10-05T14:30:00Z"`。
3.  **前端**：Template 自带的全局 JavaScript 脚本（位于 `aiursoft/uistack` 中）在 `DOMContentLoaded` 时会扫描全页面所有的 `[data-utc-time]` 元素。
4.  **计算**：JS 获取浏览器的时区信息（例如 `Asia/Shanghai`），将 UTC 时间加上 +8 小时。
5.  **渲染**：JS 修改 DOM，将转换后的当地时间（例如 `2023-10-05 22:30:00`）写入 `<label>` 的文本内容中。

**总结：** 使用 `data-utc-time`，你可以确保无论你的用户身处纽约、伦敦还是北京，他们看到的永远是**自己当前时区**的正确时间，而无需在后端编写复杂的时区判断逻辑。
