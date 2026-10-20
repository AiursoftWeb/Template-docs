# Background Job System in Aiursoft.Template

`Aiursoft.Template` integrates a powerful and observable background job system powered by [Aiursoft.Canon](https://github.com/AiursoftWeb/Aiursoft.Canon). This system allows you to run heavy or recurring tasks (like sending emails, cleaning up files, or synchronizing data) without blocking the main request thread.

## Core Architecture

The system is built on several layers of `Aiursoft.Canon`:

1.  **ServiceTaskQueue**: A named, per-queue-serial task engine with full status tracking.
2.  **BackgroundJobs**: A global registry that allows discovering and triggering jobs by type.
3.  **ScheduledTasks**: A timer-based system to run jobs on a recurring schedule.

## Key Features

-   **Observable**: Track task status (Pending, Processing, Success, Failed, Cancelled) in real-time.
-   **Admin Dashboard**: Built-in UI at `/Jobs` to view history and manually trigger jobs.
-   **Dependency Injection**: Automatically creates a fresh `IServiceScope` for every task run, making it safe to use Scoped services like `DbContext`.
-   **Flexible Scheduling**: Easily attach recurring schedules to any registered job.
-   **Error Reporting**: Captures and displays exception messages directly in the admin UI.

## How to Define a Background Job

To create a new background job, implement the `IBackgroundJob` interface.

```csharp
using Aiursoft.Canon.BackgroundJobs;

public class MyBackgroundJob(ILogger<MyBackgroundJob> logger, MyDbContext db) : IBackgroundJob
{
    // Metadata shown in the admin dashboard
    public string Name => "My Background Task";
    public string Description => "This task performs a heavy operation every hour.";

    public async Task ExecuteAsync()
    {
        logger.LogInformation("Starting background work...");
        
        // You can safely use injected Scoped services like 'db' here.
        var count = await db.Users.CountAsync();
        
        await Task.Delay(5000); // Simulate work
        
        logger.LogInformation("Work finished. User count: {Count}", count);
    }
}
```

## Registration and Configuration

Register your jobs in `Startup.cs` within the `ConfigureServices` method.

### 1. Initialize the Engine
```csharp
// registers ServiceTaskQueue + TaskQueueWorkerService
services.AddTaskQueueEngine();

// registers the timer-based hosted service
services.AddScheduledTaskEngine();
```

### 2. Register Your Jobs
```csharp
// Register as a one-off job (can be triggered manually from /Jobs)
services.RegisterBackgroundJob<MyBackgroundJob>();

// Register and capture the descriptor to attach a schedule
var cleanupJob = services.RegisterBackgroundJob<OrphanAvatarCleanupJob>();
```

### 3. Attach a Schedule (Optional)
```csharp
services.RegisterScheduledTask(
    registration: cleanupJob,
    period:       TimeSpan.FromHours(6),   // Run every 6 hours
    startDelay:   TimeSpan.FromMinutes(5)  // Initial delay after app starts
);
```

## Admin Dashboard

The `Aiursoft.Template` includes a built-in administration interface located at `/Jobs`. 

-   **Registered Jobs**: List of all jobs available in the system with their descriptions.
-   **Trigger Now**: A button to manually enqueue an immediate run of any job.
-   **History**: A log of recent executions showing start time, duration, and status.
-   **Error Details**: If a task fails, the exception message is displayed here for easy debugging.

## Triggering Jobs Programmatically

While most jobs run on a schedule, you can also trigger them manually from your code (e.g., from a Controller after a user action):

```csharp
public class MyController(BackgroundJobRegistry registry) : Controller
{
    public IActionResult RunNow()
    {
        // Enqueues the job immediately in the background
        registry.TriggerNow<MyBackgroundJob>();
        return Ok("Task enqueued!");
    }
}
```

## Best Practices

1.  **Statelessness**: Jobs should ideally be stateless. If you need to persist state, use the database.
2.  **Concurrency**: Tasks in the same named queue run serially. By default, `TriggerNow<T>` uses the type name as the queue name.
3.  **Scope Safety**: Always use the dependencies provided via constructor injection. The system ensures these are resolved from a fresh scope.
4.  **Logging**: Use `ILogger` within your jobs. Logs will be captured by your configured logger (e.g., ClickHouse).
