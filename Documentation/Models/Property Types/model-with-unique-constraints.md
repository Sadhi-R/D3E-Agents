# Model with Unique Constraints

## Context

A unique property in a model is used to define a uniqueness constraint on a specific property. When a property is marked as unique, it means that each value in that property must be unique across all instances of the model. No two instances of the model can have the same value for the specified unique property. This is useful for fields like email, username, or any identifier that must be distinct.

- **Data Integrity:** Ensures no duplicate values for the property across all records.
- **Validation:** The system will automatically enforce uniqueness during create and update operations.
- **Syntax:** Use `unique true` in the property definition.

## Prompt for Creating

"Add a unique property [propertyName] of type [Type] to the [ModelName] model"

**Example Prompts:**
- "Create a Student model with name, email, phone, age, gender, where email is unique"
- "Create a User model with username, password, email, where username is unique"
- "Create a Product model with productCode, name, price, where productCode is unique"


## D3E Examples

### Example 1: User with Unique Email

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Email'
            type String
            required true
            unique true
        }
    ]
}
```

### Example 2: User with Unique Username

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Username'
            type String
            required true
            unique true
        }
    ]
}
```

### Example 3: Student with Unique Registration Number

```d3e
Model {
    name 'Student'
    properties [
        {
            name 'Registration Number'
            type Integer
            required true
            unique true
        }
    ]
}
```

**Note:**
- Use `unique true` to enforce uniqueness for a property.
- Unique constraints are ideal for identifiers, emails, usernames, or any field that must be distinct.
- The system will automatically validate uniqueness during create and update operations.
- You can combine `unique true` with other attributes (e.g., `required true`).
