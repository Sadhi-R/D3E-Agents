# Embedded Model

## Context

An embedded model in D3E is used as a nested, always-present part of another model. Embedded models are not stored independently; they always exist as part of their parent. This is useful for representing value objects or components that do not make sense on their own, such as Address or FamilyInfo.

- **Always Present:** Embedded models cannot be null and are always part of the parent.
- **Not Standalone:** Cannot be created, updated, or deleted independently.
- **Syntax:** Use `embedded true` in the model definition or `child true` in the property.

## Prompt for Creating

"Create a [ParentModelName] model with an embedded [EmbeddedModelName] property"

**Example Prompts:**
- "Create a FamilyInfo model with an embedded collection of Child models"
- "Create a Customer model with an embedded Address property"
- "Create a Profile model with an embedded ContactInfo property"

## D3E Examples

### Example 1: FamilyInfo with Embedded Children

```d3e
Model {
    name 'Family Info'
    creatable false
    properties [
        {
            name 'Children'
            type Child
            collection true
            child true
        }
        // ... other properties ...
    ]
}

Model {
    name 'Child'
    creatable false
    properties [
        {
            name 'age Group'
            type String
        }
        {
            name 'Name'
            type String
        }
    ]
}
```

### Example 2: Customer with Embedded Address

```d3e
Model {
    name 'Customer'
    properties [
        {
            name 'Address'
            type Address
            child true
        }
    ]
}

Model {
    name 'Address'
    embedded true
    properties [
        {
            name 'Street'
            type String
        }
        // ... other address fields ...
    ]
}
```

**Note:**
- Use `embedded true` in the model or `child true` in the property to indicate embedding.
- Embedded models are always present and not managed independently.
