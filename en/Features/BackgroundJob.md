# Aiursoft.Template Background Job System Guide

`Aiursoft.Template` includes a lightweight background job management system that requires no additional infrastructure (such as Redis). It runs within the application process, supports dependency injection, and is ideal for handling "fire-and-forget" asynchronous tasks.

## Core Features

- **Zero Dependencies**: Based on memory (`ConcurrentDictionary`), no external database or message queue configuration is required.
- **Dependency Injection Support**: A new `IServiceScope` is created for each task execution, allowing safe use of scoped services (such as database context `DbContext`).
- **Flexible Concurrency Control**: Use `QueueName` to control whether tasks run in parallel or serially.
- **Visual Dashboard**: Provides a UI interface to view task status (queued, in progress, succeeded, failed) and cancel tasks.

## How to Use

### 1. Inject the Service

Inject [BackgroundJobQueue](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#10-190) into your Controller or Service:

```csharp
public class MyController(BackgroundJobQueue backgroundJobQueue) : Controller
{
    // ...
}
```

### 2. Publish a Task

Use the [QueueWithDependency](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#16-42) method to publish a task. This is the most commonly used method because it automatically handles the dependency injection scope for you.

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

## Core Concepts: Queue & Concurrency

The core of this system lies in the `queueName` parameter, which determines how tasks are executed:

- **Sequential Execution**:
  If you want tasks to execute **in order**, one after another, use the **same** `queueName`.
  *Use case example*: Exporting reports, generating continuous log files, processing webhooks that must arrive in sequence.

- **Parallel Execution**:
  If you want tasks to execute **simultaneously**, without blocking each other, use a **unique** `queueName` for each task (e.g., `Guid.NewGuid().ToString()`).
  *Use case example*: Sending a large number of notification emails, processing multiple independent files uploaded by users.

### Example Comparison

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

## Best Practices

1. **Absolutely禁止 using dependencies from Controller in background tasks**
   Background tasks are **headless**, running in completely independent threads and scopes.
   > ⛔ **Dangerous operations**:
   > *   Do not use `HttpContext`, `User`, `ModelState` inside closures.
   > *   **Do not** directly use services injected into the Controller's constructor (e.g., `_context` or `_userManager`). When background tasks run, the Controller itself may have already been disposed, or those services are request-scoped and no longer valid in the background thread.
   >
   > **Correct approach**:
   > Only use the service `T` injected via `QueueWithDependency<T>`. If you need multiple services (e.g., both `EmailSender` and `LogService`), **do not** attempt to inject multiple services into a single task, nor try to "steal" one from the Controller closure.
   >
   > **Multi-service injection pattern (Composite Service Pattern)**:
   > If the task logic is complex and depends on multiple services, create a new composite service.
   > *   Incorrect: Trying to use both A and B inside a Lambda.
   > *   Correct: Define a `JobHandlerService` that injects A and B in its constructor. Then use `QueueWithDependency<JobHandlerService>`. The dependency injection container will properly manage the lifetimes of A and B.

2. **Pay attention to data persistence (Data Lifecycle)**
   This is an **in-memory** queue system.
   > ⚠️ **Warning**: If the application restarts or crashes, all **pending** and **processing** tasks will be lost.
   For extremely critical tasks that must never be lost (e.g., payment callback handling), use a persistent queue system (such as RabbitMQ or a database-backed task table), or ensure your business logic can tolerate occasional task loss (or includes retry mechanisms).

3. **Exception Handling**
   The system automatically catches exceptions thrown by tasks and marks the task as `Failed`, allowing you to view error messages in the dashboard. It is recommended to also use appropriate `try-catch` blocks within tasks, especially if you need to log specific business logs. The system **will not** automatically retry failed tasks.

4. **Avoid Long-Running Blocking of the Main Thread**
   [QueueWithDependency](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/BackgroundJobQueue.cs#16-42) itself is extremely fast (it merely places tasks into an in-memory dictionary) and does not block the main thread. The actual heavy work is performed in a background thread pool.

5. **Leverage Strongly-Typed Dependencies**
   Always prefer the generic version `QueueWithDependency<TService>`. This not only keeps your code cleaner but also forces you to think about the actual services your task depends on, avoiding the chaotic acquisition of services within a single Scope.

## Frequently Asked Questions

**Q: Why isn't my task running?**
A: Check for deadlocks, or whether a previous task with the same `queueName` is stuck (e.g., infinite loop or indefinite waiting). Since tasks in the same queue run serially, the next task will not start until the previous one completes.

**Q: Can I access the database within a task?**
A: Yes, and it's very convenient. By using `QueueWithDependency<TemplateDbContext>`, you gain access to a dedicated, scoped database context connection. The system automatically releases it after use.

**Q: How do I clean up old task records?**
A: The system includes a built-in scheduled cleanup mechanism (Cron Job). By default, [QueueWorkerService](file:///home/anduin/Source/Repos/Aiursoft/aspnetcore-web/Template/src/Aiursoft.Template/Services/BackgroundJobs/QueueWorkerService.cs#8-122) runs the cleanup logic every 5 minutes, removing task records that completed over 1 hour ago to prevent unbounded memory growth.
