# Aiursoft.Template 后台任务系统

`Aiursoft.Template` 集成了一个强大且可观测的后台任务系统，由 [Aiursoft.Canon](https://github.com/AiursoftWeb/Aiursoft.Canon) 提供支持。该系统允许您在不阻塞主请求线程的情况下运行重型或定期任务（如发送电子邮件、清理文件或同步数据）。

## 核心架构

该系统基于 `Aiursoft.Canon` 的多个层级构建：

1.  **ServiceTaskQueue**：一个命名、按队列串行的任务引擎，具有完整的状态跟踪。
2.  **BackgroundJobs**：一个全局注册表，允许按类型发现和触发作业。
3.  **ScheduledTasks**：一个基于定时器的系统，用于按定期计划运行作业。

## 主要特性

-   **可观测性**：实时跟踪任务状态（排队中、进行中、成功、失败、已取消）。
-   **管理看板**：内置在 `/Jobs` 的 UI 界面，用于查看历史记录并手动触发作业。
-   **依赖注入**：为每个任务运行自动创建一个全新的 `IServiceScope`，可以安全地使用 Scoped 服务（如 `DbContext`）。
-   **灵活调度**：轻松为任何已注册的作业附加定期计划。
-   **错误报告**：直接在管理 UI 中捕获并显示异常消息，方便调试。

## 如何定义后台任务

要创建新的后台任务，请实现 `IBackgroundJob` 接口。

```csharp
using Aiursoft.Canon.BackgroundJobs;

public class MyBackgroundJob(ILogger<MyBackgroundJob> logger, MyDbContext db) : IBackgroundJob
{
    // 在管理看板中显示的元数据
    public string Name => "我的后台任务";
    public string Description => "此任务每小时执行一次重型操作。";

    public async Task ExecuteAsync()
    {
        logger.LogInformation("开始执行后台工作...");
        
        // 您可以在这里安全地使用注入的 Scoped 服务（如 'db'）。
        var count = await db.Users.CountAsync();
        
        await Task.Delay(5000); // 模拟工作
        
        logger.LogInformation("工作完成。用户计数：{Count}", count);
    }
}
```

## 注册与配置

在 `Startup.cs` 的 `ConfigureServices` 方法中注册您的作业。

### 1. 初始化引擎
```csharp
// 注册 ServiceTaskQueue + TaskQueueWorkerService
services.AddTaskQueueEngine();

// 注册基于定时器的托管服务
services.AddScheduledTaskEngine();
```

### 2. 注册您的作业
```csharp
// 注册为单次作业（可以从 /Jobs 手动触发）
services.RegisterBackgroundJob<MyBackgroundJob>();

// 注册并捕获描述符以附加计划
var cleanupJob = services.RegisterBackgroundJob<OrphanAvatarCleanupJob>();
```

### 3. 附加计划（可选）
```csharp
services.RegisterScheduledTask(
    registration: cleanupJob,
    period:       TimeSpan.FromHours(6),   // 每 6 小时运行一次
    startDelay:   TimeSpan.FromMinutes(5)  // 应用程序启动后的初始延迟
);
```

## 管理看板

`Aiursoft.Template` 包含一个内置的管理界面，位于 `/Jobs`。

-   **已注册作业**：系统中所有可用作业及其说明的列表。
-   **立即触发**：一个手动将任何作业排入立即运行队列的按钮。
-   **历史记录**：最近执行的日志，显示开始时间、持续时间和状态。
-   **错误详情**：如果任务失败，此处将显示异常消息，以便于调试。

## 以编程方式触发作业

虽然大多数作业按计划运行，但您也可以从代码中手动触发它们（例如，在用户操作后的控制器中）：

```csharp
public class MyController(BackgroundJobRegistry registry) : Controller
{
    public IActionResult RunNow()
    {
        // 立即在后台将任务排队
        registry.TriggerNow<MyBackgroundJob>();
        return Ok("任务已排队！");
    }
}
```

## 最佳实践

1.  **无状态性**：作业理想情况下应该是无状态的。如果需要持久化状态，请使用数据库。
2.  **并发控制**：相同名称队列中的任务将串行运行。默认情况下，`TriggerNow<T>` 使用类型名称作为队列名称。
3.  **作用域安全**：始终使用通过构造函数注入提供的依赖项。系统确保这些依赖项是从全新的作用域中解析的。
4.  **日志记录**：在您的作业中使用 `ILogger`。日志将被您配置的记录器（如 ClickHouse）捕获。
