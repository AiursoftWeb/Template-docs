# Step 10: Soft Delete and Recycle Bin Based on Background Tasks

In this step, we will implement a "Soft Delete" feature and use the background task system to automatically clean up old deleted items from the "Recycle Bin."

## 1. What is Soft Delete?

Soft delete is a technique where instead of permanently removing a record from the database, you mark it as "deleted" (e.g., by setting a boolean flag `IsDeleted = true`). This allows you to:
-   **Restore items** if the user deleted them by mistake.
-   **Audit** who deleted what and when.
-   **Perform background cleanup** later to reclaim space.

## 2. Add Soft Delete to Your Entity

Let's assume we have a `Note` entity. Add `IsDeleted` and `DateDeleted` properties to it:

```csharp
public class Note
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Content { get; set; }
    
    // Soft delete properties
    public bool IsDeleted { get; set; }
    public DateTime? DateDeleted { get; set; }
}
```

When a user clicks "Delete," instead of `db.Notes.Remove(note)`, you do:

```csharp
note.IsDeleted = true;
note.DateDeleted = DateTime.UtcNow;
await db.SaveChangesAsync();
```

## 3. Create a Cleanup Background Job

We don't want the "Recycle Bin" to grow forever. We want a background job that automatically deletes items that have been in the recycle bin for more than 30 days.

Create a new file `Services/BackgroundJobs/RecycleBinCleanupJob.cs`:

```csharp
using Aiursoft.Canon.BackgroundJobs;
using Aiursoft.Template.Entities;
using Microsoft.EntityFrameworkCore;

public class RecycleBinCleanupJob(TemplateDbContext db, ILogger<RecycleBinCleanupJob> logger) : IBackgroundJob
{
    public string Name => "Recycle Bin Cleanup";
    public string Description => "Permanently deletes items that have been in the recycle bin for more than 30 days.";

    public async Task ExecuteAsync()
    {
        logger.LogInformation("RecycleBinCleanupJob started.");
        
        var threshold = DateTime.UtcNow.AddDays(-30);
        
        // Find notes that were soft-deleted more than 30 days ago
        var notesToDelete = await db.Notes
            .Where(n => n.IsDeleted && n.DateDeleted < threshold)
            .ToListAsync();
            
        if (notesToDelete.Any())
        {
            logger.LogInformation("Found {Count} old notes to permanently delete.", notesToDelete.Count);
            db.Notes.RemoveRange(notesToDelete);
            await db.SaveChangesAsync();
        }
        
        logger.LogInformation("RecycleBinCleanupJob finished.");
    }
}
```

## 4. Register and Schedule the Job

Now, go to `Startup.cs` to register this job and set it to run on a schedule (e.g., every day).

```csharp
// 1. Register the job
var recycleJob = services.RegisterBackgroundJob<RecycleBinCleanupJob>();

// 2. Schedule it to run every 24 hours
services.RegisterScheduledTask(
    registration: recycleJob,
    period:       TimeSpan.FromDays(1),
    startDelay:   TimeSpan.FromMinutes(10) // Start 10 mins after app launch
);
```

## 5. Summary

By combining a "Soft Delete" flag with a scheduled background job, you've created a professional data lifecycle management system. Your users get the safety of a recycle bin, and your database stays lean automatically.

You can monitor the status of these cleanup tasks anytime at the `/Jobs` dashboard!
