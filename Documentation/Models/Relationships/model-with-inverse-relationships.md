# Model with Inverse Relationships

## Context

An inverse relationship in D3E models represents a bidirectional association between two models. This means that each model references the other, allowing navigation in both directions. Inverse relationships are useful for scenarios like a Customer having a collection of Orders, and each Order referencing its Customer.

- **Bidirectional:** Both models reference each other.
- **Navigation:** Enables easy access from one model to the related model(s).
- **Syntax:** Use `inverse true` and `inverseProperty` in the collection property.

## Prompt for Creating

"Create a [ModelName] model with a collection of [RelatedModelName] as an inverse relationship"

**Example Prompts:**
- "Create a Customer model with a collection of Orders as an inverse relationship"
- "Create a Project model with a collection of Tasks as an inverse relationship"
- "Create a Department model with a collection of Employees as an inverse relationship"

## D3E Examples

### Example 1: Customer and Orders (Inverse Relationship)

```d3e
Model {
    name 'Customer'
    properties [
        {
            name 'Orders'
            type Order
            collection true
            inverse true
            inverseProperty customer
        }
    ]
}

Model {
    name 'Order'
    properties [
        {
            name 'Customer'
            type Customer
        }
        // ... other order fields ...
    ]
}
```

### Example 2: Project and Tasks (Inverse Relationship)

```d3e
Model {
    name 'Project'
    properties [
        {
            name 'Tasks'
            type Task
            collection true
            inverse true
            inverseProperty project
        }
    ]
}

Model {
    name 'Task'
    properties [
        {
            name 'Project'
            type Project
        }
        // ... other task fields ...
    ]
}
```

### Example 3: Department and Employees (Inverse Relationship)

```d3e
Model {
    name 'Department'
    properties [
        {
            name 'Employees'
            type Employee
            collection true
            inverse true
            inverseProperty department
        }
    ]
}

Model {
    name 'Employee'
    properties [
        {
            name 'Department'
            type Department
        }
        // ... other employee fields ...
    ]
}
```

**Note:**
- Use `inverse true` and `inverseProperty` to establish a bidirectional relationship.
- Inverse relationships enable navigation and data integrity between related models.
