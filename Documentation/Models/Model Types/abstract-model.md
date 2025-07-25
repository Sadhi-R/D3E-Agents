# Abstract Model

## Context

An abstract model in D3E is a conceptual model that is not intended to be instantiated directly. Abstract models are used as base types for other models to inherit common properties and logic. They help promote reuse and consistency across related models.

- **Not Instantiable:** Cannot be created directly.
- **Base for Inheritance:** Used as a parent for other models.
- **Syntax:** Use `abstract true` in the model definition (hypothetical, as D3E may not have explicit abstract keyword, but conceptually this is how it works).

## Prompt for Creating

"Create an abstract [ModelName] model to be used as a parent for other models"

**Example Prompts:**
- "Create an abstract BaseUser model to be inherited by User and Customer"
- "Create an abstract Account model to be inherited by PremiumAccount and StandardAccount"
- "Create an abstract Document model to be inherited by Invoice and Receipt"

## D3E Examples

### Example 1: BaseUser as Abstract Model

```d3e
Model {
    name 'BaseUser'
    // abstract true (conceptual)
    properties [
        {
            name 'Username'
            type String
        }
        {
            name 'Email'
            type String
        }
    ]
}

Model {
    name 'User'
    parent BaseUser
    properties [
        {
            name 'Role'
            type UserRole
        }
    ]
}

Model {
    name 'Customer'
    parent BaseUser
    properties [
        {
            name 'Customer Type'
            type String
        }
    ]
}
```

**Note:**
- Abstract models are not instantiated directly.
- They are used as parents for other models to promote reuse and consistency.
