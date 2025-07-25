# Model with Lifecycle Actions

## Context

Lifecycle actions in D3E models are special actions that are automatically triggered by changes to the model's data, such as creation, update, or deletion. These actions are used to enforce business rules, automate workflows, or perform side effects when the model changes state.

- **OnCreate**: Runs when a new record is created.
- **OnUpdate**: Runs when a record is updated.
- **OnDelete**: Runs when a record is deleted.
- **OnCreateAndUpdate**: Runs on both create and update events.

> **Warning:** When defining lifecycle actions, do **not** repeat keys (such as `name`, `runOn`, or `block`) within the same action block. Each action should have each key only once. Repeating keys is incorrect and will cause errors. See the examples below for the correct format.

## Prompt for Creating

"Create a [ModelName] model with [property1], [property2], ... and a lifecycle action [ActionName] that runs on [event] and [action description]"

**Example Prompts:**

- "Create an Order model with orderNumber, items, totalAmount and a lifecycle action to calculate the total amount on update"
- "Create a User model with status, email and a lifecycle action to log status changes on update"
- "Create a Document model with mainDocument, createdDate and a lifecycle action to clean up files on delete"

## D3E Examples

> **Note:** The following examples demonstrate the correct way to define lifecycle actions. Each action block should have unique keys (no duplicates). If you see repeated keys in your output, please correct them to match the examples below.

### Example 1: OnUpdate Action

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

### Example 2: OnDelete Action

```d3e
Model {
    name 'Document'
    properties [
        {
            name 'Main Document'
            type DFile
        }
    ]
    actions [
        {
            name 'cleanupFiles'
            runOn OnDelete
            block ```
                // Cleanup logic for files
            ```
        }
    ]
}
```

### Example 3: OnUpdate with Condition

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Status'
            type String
        }
    ]
    actions [
        {
            name 'onStatusChange'
            runOn OnUpdate
            block ```
                if(this.status != old.status) {
                    // Log status change
                    // Send notifications
                }
            ```
        }
    ]
}
```

**Note:**

- Use the `runOn` attribute to specify when the action should be triggered.
- The `block` must be wrapped in triple backticks.
- Do not repeat property keys within the same property or action block.
- Lifecycle actions are ideal for enforcing business rules and automating workflows.

