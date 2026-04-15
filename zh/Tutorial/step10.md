# 第十步：基于后台任务的软删除与回收站

在这一步中，我们将实现“软删除（Soft Delete）”功能，并利用后台任务系统自动清理“回收站”中的陈旧已删除项。

## 1. 什么是软删除？

软删除是一种技术，它不从数据库中永久删除记录，而是将其标记为“已删除”（例如，通过设置布尔标志 `IsDeleted = true`）。这样做的好处包括：
-   **项恢复**：如果用户误删了项目，可以随时恢复。
-   **审计**：记录谁在什么时候删除了什么。
-   **后台清理**：稍后再进行后台清理以回收空间。

## 2. 为实体添加软删除支持

假设我们有一个 `Note` 实体。为其添加 `IsDeleted` 和 `DateDeleted` 属性：

```csharp
public class Note
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
    
    // 软删除属性
    public bool IsDeleted { get; set; }
    public DateTime? DateDeleted { get; set; }
}
```

当用户点击“删除”时，不要执行 `db.Notes.Remove(note)`，而是：

```csharp
note.IsDeleted = true;
note.DateDeleted = DateTime.UtcNow;
await db.SaveChangesAsync();
```

## 3. 创建清理后台作业

我们不希望“回收站”无限增长。我们需要一个后台作业，自动删除已经在回收站中超过 30 天的项目。

创建一个新文件 `Services/BackgroundJobs/RecycleBinCleanupJob.cs`：

```csharp
using Aiursoft.Canon.BackgroundJobs;
using Aiursoft.Template.Entities;
using Microsoft.EntityFrameworkCore;

public class RecycleBinCleanupJob(TemplateDbContext db, ILogger<RecycleBinCleanupJob> logger) : IBackgroundJob
{
    public string Name => "回收站清理";
    public string Description => "永久删除在回收站中存放超过 30 天的项目。";

    public async Task ExecuteAsync()
    {
        logger.LogInformation("回收站清理任务启动。");
        
        var threshold = DateTime.UtcNow.AddDays(-30);
        
        // 查找 30 天前被软删除的笔记
        var notesToDelete = await db.Notes
            .Where(n => n.IsDeleted && n.DateDeleted < threshold)
            .ToListAsync();
            
        if (notesToDelete.Any())
        {
            logger.LogInformation("发现 {Count} 个陈旧笔记需要永久删除。", notesToDelete.Count);
            db.Notes.RemoveRange(notesToDelete);
            await db.SaveChangesAsync();
        }
        
        logger.LogInformation("回收站清理任务完成。");
    }
}
```

## 4. 注册与调度作业

现在，在 `Startup.cs` 中注册此作业并设置为定期运行（例如，每天运行一次）。

```csharp
// 1. 注册作业
var recycleJob = services.RegisterBackgroundJob<RecycleBinCleanupJob>();

// 2. 调度它每 24 小时运行一次
services.RegisterScheduledTask(
    registration: recycleJob,
    period:       TimeSpan.FromDays(1),
    startDelay:   TimeSpan.FromMinutes(10) // 应用程序启动 10 分钟后开始
);
```

## 5. 总结

通过将“软删除”标志与调度的后台作业相结合，您创建了一个专业的数据生命周期管理系统。您的用户可以享受到回收站带来的安全性，而您的数据库也会自动保持精简。

您可以随时在 `/Jobs` 看板监控这些清理任务的状态！
