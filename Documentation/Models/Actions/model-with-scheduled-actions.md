# Model with Scheduled Actions

## Context

Scheduled actions in D3E models allow you to define logic that runs automatically at specified times or intervals, independent of user interaction. These are useful for periodic tasks such as sending reminders, generating reports, or performing maintenance.

- **Scheduling**: Scheduled actions are configured to run at specific times, dates, or intervals (e.g., daily, weekly).

> **Warning:** When defining scheduled actions, do **not** repeat keys (such as `name`, `schedule`, or `block`) within the same action block. Each action should have each key only once. Repeating keys is incorrect and will cause errors. See the examples below for the correct format.

## Prompt for Creating

"Create a [ModelName] model with [property1], [property2], ... and a scheduled action [ActionName] that runs [schedule description] and [action description]"

**Example Prompts:**

- "Create a Report model with name, title, publishedYear and a scheduled action to generate a summary every day at midnight"
- "Create a Notification model with recipient, message, sentDate and a scheduled action to send reminders every Monday"
- "Create a Backup model with backupFile, backupDate and a scheduled action to perform backup every week"

## D3E Examples

> **Note:** The following examples demonstrate the correct way to define scheduled actions. Each action block should have unique keys (no duplicates). If you see repeated keys in your output, please correct them to match the examples below.

### Example 1: Daily Scheduled Action

```d3e
Model {
    name 'Report'
    properties [
        {
            name 'Title'
            type String
        }
    ]
    actions [
        {
            name 'generateSummary'
            schedule '0 0 * * *' // Every day at midnight (cron syntax)
            block ```
                // Logic to generate summary report
            ```
        }
    ]
}
```

### Example 2: Weekly Scheduled Action

```d3e
Model {
    name 'Backup'
    properties [
        {
            name 'Backup File'
            type DFile
        }
    ]
    actions [
        {
            name 'performBackup'
            schedule '0 0 * * 0' // Every Sunday at midnight
            block ```
                // Logic to perform backup
            ```
        }
    ]
}
```

**Note:**

- Use the `schedule` attribute to specify when the action should run (typically using cron syntax).
- The `block` must be wrapped in triple backticks.
- Do not repeat property keys within the same property or action block.
- Scheduled actions are ideal for automating periodic or time-based tasks.

