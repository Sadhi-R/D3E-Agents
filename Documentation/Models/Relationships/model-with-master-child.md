# Model with Master-Child Relationship

## Context

A master-child relationship in D3E models represents ownership, where the child model is associated with a master (or parent) model. The child cannot exist without the master, and typically, the master manages the lifecycle of its children. This is useful for scenarios like Orders belonging to a Customer, or Employees belonging to a Company.

- **Ownership:** The child is owned by the master and cannot exist independently.
- **Lifecycle:** Deleting the master may delete all its children.
- **Syntax:** Use the `master` keyword in the child model to specify the master model.

## Prompt for Creating

"Create a [ChildModelName] model with a master relationship to [MasterModelName]"

**Example Prompts:**
- "Create an Order model with a master relationship to Customer"
- "Create an Employee model with a master relationship to Company"
- "Create a Task model with a master relationship to Project"

## D3E Examples

### Example 1: Order with Master Customer

```d3e
(Model Order) {
    name 'Order'
    master Customer
    properties [
        {
            name 'Order Number'
            type String
            required true
            unique true
        }
        // ... other properties ...
    ]
}
```

### Example 2: Employee with Master Company

```d3e
(Model Employee) {
    name 'Employee'
    master Company
    properties [
        {
            name 'Name'
            type String
            required true
        }
        // ... other properties ...
    ]
}
```

### Example 3: Task with Master Project

```d3e
(Model Task) {
    name 'Task'
    master Project
    properties [
        {
            name 'Title'
            type String
            required true
        }
        // ... other properties ...
    ]
}
```

**Note:**
- Use the `master` keyword in the child model to establish the relationship.
- The child model cannot exist without the master.
- Master-child relationships help maintain data integrity and reflect real-world ownership.
