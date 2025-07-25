# Singleton Model

## Context

A singleton model in D3E is a model for which only one instance can exist in the system. Singleton models are useful for application-wide settings, configuration, or default values that should be unique across the application.

- **Single Instance:** Only one record exists for the model.
- **Use Case:** Application settings, configuration, or default user.
- **Syntax:** Use `singleton true` in the model definition.

## Prompt for Creating

"Create a [ModelName] model with singleton true for application-wide settings or configuration"

**Example Prompts:**
- "Create a DefaultUser model with singleton true for the default admin user"
- "Create a Settings model with singleton true for application configuration"
- "Create a License model with singleton true for license information"

## D3E Examples

### Example 1: DefaultUser as Singleton

```d3e
Model {
    name 'DefaultUser'
    singleton true
    actions [
        {
            name 'CreateAdmin'
            block ```
                // ... admin creation logic ...
            ```
        }
    ]
}
```

### Example 2: Settings as Singleton

```d3e
Model {
    name 'Settings'
    singleton true
    properties [
        {
            name 'Theme'
            type String
        }
        {
            name 'Language'
            type String
        }
    ]
}
```

**Note:**
- Use `singleton true` to ensure only one instance of the model exists.
- Singleton models are ideal for global configuration or default values.
