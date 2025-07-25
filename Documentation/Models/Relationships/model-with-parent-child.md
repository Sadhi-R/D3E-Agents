# Model with Parent-Child (Inheritance) Relationship

## Context

A parent-child relationship in D3E models represents inheritance, where a child model extends or specializes a parent model. The child inherits all properties and behaviors of the parent, and can add its own specific properties. This is useful for scenarios like Customer extending BaseUser, or Manager extending Employee.

- **Inheritance:** The child model inherits properties and logic from the parent model.
- **Specialization:** The child can add or override properties and behaviors.
- **Syntax:** Use the `parent` keyword in the child model to specify the parent model.

## Prompt for Creating

"Create a [ChildModelName] model with a parent relationship to [ParentModelName]"

**Example Prompts:**
- "Create a Customer model with a parent relationship to BaseUser"
- "Create a Manager model with a parent relationship to Employee"
- "Create a PremiumAccount model with a parent relationship to Account"

## D3E Examples

### Example 1: Customer with Parent BaseUser

```d3e
(Model Customer) {
    name 'Customer'
    parent BaseUser
    properties [
        {
            name 'Customer Type'
            type String
        }
        // ... other properties ...
    ]
}
```

### Example 2: Manager with Parent Employee

```d3e
(Model Manager) {
    name 'Manager'
    parent Employee
    properties [
        {
            name 'Department'
            type String
        }
        // ... other properties ...
    ]
}
```

### Example 3: PremiumAccount with Parent Account

```d3e
(Model PremiumAccount) {
    name 'PremiumAccount'
    parent Account
    properties [
        {
            name 'Benefits'
            type String
        }
        // ... other properties ...
    ]
}
```

**Note:**
- Use the `parent` keyword in the child model to establish inheritance.
- The child model inherits all properties and logic from the parent.
- Parent-child (inheritance) relationships help organize models and promote reuse.
