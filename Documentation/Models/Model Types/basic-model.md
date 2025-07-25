# Basic Model

## Context

A basic (standard) model in D3E represents persistent data stored in the database. It is the default model type and is used for most business entities, such as User, Lead, or Company. Basic models support CRUD operations and are the foundation for API generation.

- **Persistence:** Data is stored in the database.
- **Default Type:** No special keywords required.
- **Use Case:** Most business entities.

## Prompt for Creating

"Create a [ModelName] model with fields [field1, field2, ...]"

**Example Prompts:**
- "Create a User model with firstName, lastName, email, password, and role"
- "Create a Company model with name, isLeadService, isCustomerService"
- "Create a Lead model with name, email, phone, status"

## D3E Examples

### Example 1: User Model

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

### Example 2: Company Model

```d3e
Model {
    name 'Company'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'Is Lead Service'
            type Boolean
        }
        {
            name 'Is Customer Service'
            type Boolean
        }
    ]
}
```

### Example 3: Lead Model

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
            name 'Email'
            type String
        }
        {
            name 'Phone'
            type String
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
- Basic models are the most common type in D3E.
- No special keywords are needed unless you want to specify a different type (embedded, singleton, etc.).
