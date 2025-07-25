# Model with Required Properties

## Context

A required property is a property that must have a value when creating or updating a model. Marking a property as required ensures that the field cannot be left empty, enforcing data integrity and preventing incomplete records. In D3E, you specify a property as required by adding the `required true` attribute to the property definition.

- **Validation:** Required properties are validated automatically; the system will not allow saving a model instance without a value for these fields.
- **Applicability:** Any property (primitive, reference, collection, etc.) can be marked as required.
- **Syntax:** Use `required true` in the property definition.

## Prompt for Creating

"Create a [ModelName] model with required property [propertyName] of type [Type]"

**Example Prompts:**
- "Create a User model with required properties firstName, lastName, email, password, and role"
- "Create a Lead model with required properties name and status"
- "Create an Education model with required properties institution, degree, and startDate"

## D3E Examples

### Example 1: User with Required Properties

```d3e
Model {
    name 'User'
    properties [
        {
            name 'First Name'
            type String
            required true
        }
        {
            name 'Last Name'
            type String
            required true
        }
        {
            name 'Email'
            type String
            required true
            unique true
        }
        {
            name 'Password'
            type String
            required true
        }
        {
            name 'Role'
            type UserRole
            required true
        }
    ]
}
```

### Example 2: Lead with Required Properties

```d3e
Model {
    name 'Lead'
    properties [
        {
            name 'Name'
            type String
            required true
        }
        {
            name 'Status'
            type LeadStatus
            required true
        }
    ]
}
```

**Note:**

- Use `required true` to enforce that a property must have a value.
- Required properties help maintain data quality and prevent incomplete records.
- You can combine `required true` with other attributes (e.g., `unique true`, `collection true`).
- The system will automatically validate required properties during create and update operations.
