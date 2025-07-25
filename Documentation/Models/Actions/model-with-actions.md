# Model with Actions

## Context

Actions in D3E models allow you to define custom logic that can be executed in response to certain events or user interactions. Actions can be triggered automatically (lifecycle actions), by user selection, or on a schedule. They are essential for implementing business logic, automation, and workflows within your application.

- **Lifecycle Actions**: Run on create, update, or delete events.
- **User Selection Actions**: Triggered by user actions in the UI.
- **Scheduled Actions**: Run at specified times or intervals.

> **Warning:** When defining actions in a model, do **not** repeat keys (such as `name`, `runOn`, or `block`) within the same action block. Each action should have each key only once. Repeating keys is incorrect and will cause errors. See the examples below for the correct format.

## Prompt for Creating

"Create a [ModelName] model with [property1], [property2], ... and an action [ActionName] that [action description]"

**Example Prompts:**

- "Create a LeadImportFile model with fileName, uploadDate and an action to import leads from a file"
- "Create a Lead Assignment model with lead, assignedTo, assignedDate and an action to set the assigned date when a lead is assigned"
- "Create an Order model with orderNumber, items, totalAmount and an action to calculate the total amount whenever items are updated"

## D3E Examples

> **Note:** The following examples demonstrate the correct way to define actions. Each action block should have unique keys (no duplicates). If you see repeated keys in your output, please correct them to match the examples below.

### Example 1: Custom Action

```d3e
Model {
    name 'LeadImportFile'
    properties [
        {
            name 'File'
            type DFile
        }
    ]
    transient true 
    actions [
        {
            name 'CreateLead'
            block ```
                ImportCSVFileUtils.createLeadData(this.file);
            ```
        }
    ]
}
```

### Example 2: Lifecycle Action

```d3e
Model {
    name 'Lead Assignment'
    properties [
        {
            name 'Lead'
            type Lead
            required true
        }
        {
            name 'Assigned To'
            type User
            required true
        }
        {
            name 'Assigned Date'
            type Date
        }
        {
            name 'Assigned By'
            type User
            required true
        }
        {
            name 'Is Unknown Incoming'
            type Boolean
        }
    ]
    actions [
        {
            name 'OnCreateAssignedBy'
            block ```
                this.assignedDate = Date.now();
            ```
        }
    ]
}
```

### Example 3: Lifecycle Action with runOn

```d3e
Model {
    name 'Order'
    properties [
        {
            name 'Order Number'
            type String
            required true
            unique true
        }
        {
            name 'Items'
            type OrderItem
            collection true
            child true
        }
        {
            name 'Total Amount'
            type Double
            computed true
            computation `items.fold(0.0, (sum, item) => sum + item.total)`
        }
        {
            name 'Status'
            type OrderStatus
            defaultValue `OrderStatus.Pending`
        }
    ]
    actions [
        {
            name 'calculateTotal'
            runOn OnUpdate
            block ```
                Double total = 0.0;
                for(OrderItem item in items) {
                    total = total + item.total;
                }
                this.totalAmount = total;
            ```
        }
    ]
    needCreatedDate true
    needUpdatedDate true
}
```

**Note:**

- Use the `actions` block to define one or more actions for a model.
- For lifecycle actions, specify the `runOn` attribute (`OnCreate`, `OnUpdate`, `OnDelete`, or `OnCreateAndUpdate`).
- The `block` must be wrapped in triple backticks.
- Do not repeat property keys within the same property or action block.
- Actions can access and modify model properties, call utility functions, and perform business logic.

