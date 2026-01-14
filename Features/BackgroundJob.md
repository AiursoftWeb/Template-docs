# Aiursoft.Template 后台任务系统使用指南

`Aiursoft.Template` 内置了一套轻量级、无需额外基础设施（如 Redis）的后台任务管理系统。它运行在应用程序进程内，支持依赖注入，非常适合处理“即发即弃”（Fire-and-forget）的异步任务。

## 核心特性

- **零依赖**：基于内存（`ConcurrentDictionary`），无需配置外部数据库或消息队列。
- **依赖注入支持**：每个任务执行时都会创建一个全新的 `IServiceScope`，可以安全地使用 Scoped 服务（如数据库上下文 `DbContext`）。
- **灵活的并发控制**：通过 `QueueName` 控制任务是并行还是串行执行。
- **可视化面板**：提供 UI 界面查看任务状态（排队中、进行中、成功、失败）和取消任务。

## 如何使用

### 1. 注入服务

在你的 Controller 或 Service 中注入 [BackgroundJobQueue](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#10-190)：

```csharp
public class MyController(BackgroundJobQueue backgroundJobQueue) : Controller
{
    // ...
}
```

### 2. 发布任务

使用 [QueueWithDependency](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#16-42) 方法发布任务。这是最常用的方法，因为它为你自动处理了依赖注入的作用域。

```csharp
// 示例：发布一个发送邮件的任务
backgroundJobQueue.QueueWithDependency<IEmailSender>(
    queueName: "EmailQueue", // 队列名称
    jobName: $"Send welcome email to {user.Email}", // 任务名称（用于显示）
    job: async (emailSender) => // 这里拿到的 emailSender 是在独立 Scope 中的
    {
        await emailSender.SendEmailAsync(user.Email, "Welcome", "...");
    });
```

## 核心概念：队列与并发 (Queue & Concurrency)

本系统的核心在于 `queueName` 参数，它决定了任务的执行方式：

- **串行执行（Sequential）**：
  如果你希望任务**按顺序**一个接一个执行，请使用**相同**的 `queueName`。
  *场景示例*：导出报表、生成连续的日志文件、处理必须按顺序到达的 webhook。

- **并行执行（Parallel）**：
  如果你希望任务**同时**执行，互不阻塞，请为每个任务使用**唯一**的 `queueName`（例如 `Guid.NewGuid().ToString()`）。
  *场景示例*：发送大量通知邮件、处理用户上传的多个独立文件。

### 示例对比

```csharp
// 串行：任务 B 会等待任务 A 完成后才开始
backgroundJobQueue.QueueWithDependency<ILogger>(
    queueName: "ReportQueue", 
    jobName: "Task A", 
    job: async (logger) => { await Task.Delay(5000); });

backgroundJobQueue.QueueWithDependency<ILogger>(
    queueName: "ReportQueue", // 相同的队列名
    jobName: "Task B", 
    job: async (logger) => { ... });

// 并行：任务 X 和 任务 Y 会几乎同时开始
backgroundJobQueue.QueueWithDependency<ILogger>(
    queueName: Guid.NewGuid().ToString(), // 唯一的队列名
    jobName: "Task X", 
    job: async (logger) => { ... });

backgroundJobQueue.QueueWithDependency<ILogger>(
    queueName: Guid.NewGuid().ToString(), // 唯一的队列名
    jobName: "Task Y", 
    job: async (logger) => { ... });
```

## 最佳实践 (Best Practices)

1. **绝对禁止在后台任务中使用 Controller 中的依赖**
   后台任务是**无头（Headless）**的，它在完全独立的线程和 Scope 中运行。
   > ⛔ **危险操作**：
   > *   不要在闭包中使用 `HttpContext`、`User`、`ModelState`。
   > *   **不要**直接使用 Controller 构造函数中注入的服务（例如 `_context` 或 `_userManager`）。因为当后台任务运行时，Controller 本身可能已经被销毁，或者那些服务是基于 HTTP 请求 Scope 的，在后台线程中已失效。
   >
   > **正确做法**：
   > 只使用通过 `QueueWithDependency<T>` 泛型注入进来的那个服务 `T`。如果你需要多个服务（例如同时需要 `EmailSender` 和 `LogService`），**不要**试图在一个任务里注入多个，也不要从 Controller 闭包里“偷”一个进去。
   >
   > **多服务注入模式（Composite Service Pattern）**：
   > 如果任务逻辑复杂，依赖多个服务，请创建一个新的聚合服务。
   > *   错误：试图在 Lambda 里同时用 A 和 B。
   > *   正确：定义一个 `JobHandlerService`，在它的构造函数里注入 A 和 B。然后 `QueueWithDependency<JobHandlerService>`。这样依赖注入容器会为你正确管理 A 和 B 的生命周期。

2. **注意数据生命周期（Data Persistance）**
   这是一个**内存（In-Memory）** 队列系统。
   > ⚠️ **警告**：如果应用程序重启或崩溃，所有**等待中（Pending）**和**进行中（Processing）**的任务都会丢失。
   对于极其关键、绝对不能丢失的任务（如支付回调处理），请使用持久化的队列系统（如 RabbitMQ 或基于数据库的任务表），或者确保你的业务逻辑允许任务偶尔丢失（或有重试机制）。

3. **异常处理**
   系统会自动捕获任务抛出的异常，并将任务标记为 `Failed`，你可以在面板中看到错误信息。建议在任务内部也进行适当的 `try-catch`，特别是如果你需要记录特定的业务日志。系统**不会**自动重试失败的任务。

4. **避免长时间阻塞主线程**
   [QueueWithDependency](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#16-42) 本身是极快的（只是将任务放入内存字典），不会阻塞主线程。真正的繁重工作是在后台线程池中完成的。

5. **利用强类型依赖**
   始终优先使用泛型版本 `QueueWithDependency<TService>`。这不仅让代码更加整洁，也强制你思考任务真正依赖的服务，避免在一个 Scope 中杂乱地获取服务。

## 常见问答

**Q: 为什么我的任务没有执行？**
A: 检查是否有死锁，或者是否有同一个 `queueName` 的前序任务卡住了（死循环或无限等待）。因为同一个队列是串行的，前一个不结束，后一个不会开始。

**Q: 我可以在任务里访问数据库吗？**
A: 可以，而且非常方便。通过 `QueueWithDependency<TemplateDbContext>` 即可获得一个独立的、Scoped 的数据库上下文连接。用完后系统会自动释放它。

**Q: 如何清理历史任务记录？**
A: 系统内置了定时清理机制（Cron Job）。默认情况下，[QueueWorkerService](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/QueueWorkerService.cs#8-122) 会每 5 分钟运行一次清理逻辑，移除 1 小时前完成的任务记录，防止内存无限增长。
