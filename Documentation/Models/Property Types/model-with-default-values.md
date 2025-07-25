# Model with Default Values

## Context

A default value is a value that is automatically assigned to a property when a new instance of a model is created, unless a different value is provided. Default values help ensure that properties have meaningful initial values and can simplify data entry and validation. In D3E, default values are specified using the `defaultValue` attribute with an expression in backticks.

- **Automatic Initialization:** Properties get a predefined value if not explicitly set.
- **Data Consistency:** Helps avoid nulls or uninitialized fields.
- **Simplifies Creation:** Reduces the need for users or code to always provide a value.

## Prompt for Creating

"Create a [ModelName] model with a property [propertyName] of type [Type] with a default value of [value]"

**Example Prompts:**

- "Create a User model with name, email, and status (Boolean, default true)"
- "Create a SearchCriteria struct with page (Integer, default 1) and perPage (Integer, default 20)"
- "Create a Lead model with hasUnreadInteractions (Boolean, default false) and unreadInteractionsCount (Integer, default 0)"
- "Create an Interaction model with isIncoming (Boolean, default false)"

## D3E Examples

### Example 1: User with Status and Chat Page Size (Default Values)

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Status'
            type Boolean
            defaultValue `true`
        }
        {
            name 'chatPageSize'
            type Integer
            defaultValue `10`
        }
    ]
}
```

### Example 2: SearchCriteria Struct with Default Values

```d3e
Struct {
    name 'SearchCriteria'
    properties [
        {
            name 'page'
            type Integer
            defaultValue `1`
        }
        {
            name 'perPage'
            type Integer
            defaultValue `20`
        }
    ]
}
```

### Example 3: Lead with Boolean and Integer Defaults

```d3e
Model {
    name 'Lead'
    properties [
        {
            name 'Has Unread Interactions'
            type Boolean
            defaultValue `false`
        }
        {
            name 'unreadInteractionsCount'
            type Integer
            defaultValue `0`
        }
    ]
}
```

### Example 4: Interaction with Boolean Defaults

```d3e
Model {
    name 'Interaction'
    properties [
        {
            name 'isIncoming'
            type Boolean
            defaultValue `false`
        }
        {
            name 'isConference'
            type Boolean
            defaultValue `false`
        }
    ]
}
```

**Note:**

- Use `defaultValue` with a valid D3E expression (in backticks) to set the default.
- Only specify `defaultValue` for non-default values. For primitive types, the default is:
  - String: `null`
  - Integer: `0`
  - Double: `0.0`
  - Boolean: `false`
- Do not use `defaultValue` for the default of the type (e.g., don't set `defaultValue 'false'` for Boolean unless you want to be explicit).
