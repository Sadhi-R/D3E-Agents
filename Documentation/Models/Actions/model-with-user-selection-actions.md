# Model with User Selection Actions

## Context

User selection actions in D3E models are actions that can be triggered directly by users from the UI, such as buttons or menu options. These actions are useful for implementing custom workflows, data processing, or any logic that should be executed on demand by the user.

- **User-Triggered**: These actions are exposed in the UI and can be invoked by users as needed.

> **Warning:** When defining user selection actions, do **not** repeat keys (such as `name` or `block`) within the same action block. Each action should have each key only once. Repeating keys is incorrect and will cause errors. See the examples below for the correct format.

## Prompt for Creating

"Create a [ModelName] model with [property1], [property2], ... and a user selection action [ActionName] that [action description]"

**Example Prompts:**

- "Create a Customer model with name, email and a user selection action to send a welcome email"
- "Create a Lead model with name, status, assignedTo and a user selection action to assign the lead to a sales rep"
- "Create a Document model with title, content and a user selection action to generate a PDF"

## D3E Examples

> **Note:** The following examples demonstrate the correct way to define user selection actions. Each action block should have unique keys (no duplicates). If you see repeated keys in your output, please correct them to match the examples below.

### Example 1: User Selection Action

```d3e
Model {
    name 'Customer'
    properties [
        {
            name 'Email'
            type String
        }
    ]
    actions [
        {
            name 'sendWelcomeEmail'
            block ```
                // Logic to send welcome email to customer
            ```
        }
    ]
}
```

### Example 2: User Selection Action with Parameters

```d3e
Model {
    name 'Document'
    properties [
        {
            name 'Title'
            type String
        }
    ]
    actions [
        {
            name 'generatePDF'
            block ```
                // Logic to generate PDF for the document
            ```
        }
    ]
}
```

**Note:**

- User selection actions are exposed in the UI for users to trigger.
- The `block` must be wrapped in triple backticks.
- Do not repeat property keys within the same property or action block.
- User selection actions are ideal for implementing custom workflows and on-demand logic.

