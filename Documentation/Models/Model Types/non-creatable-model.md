# Non-Creatable Model

## Context

A non-creatable model in D3E is used internally as part of other models, but cannot be created or managed directly via API or UI. These models are typically used for components or value objects that only exist as part of a parent, such as Education or Child.

- **Internal Use:** Not exposed for direct creation or management.
- **Composition:** Used as part of other models.
- **Syntax:** Use `creatable false` in the model definition.

## Prompt for Creating

"Create a [ModelName] model with creatable false, used as a child or embedded model in [ParentModelName]"

**Example Prompts:**
- "Create an Education model with creatable false, used as a child in Lead"
- "Create a Child model with creatable false, used as a child in FamilyInfo"
- "Create a ContactInfo model with creatable false, used as an embedded property in Profile"

## D3E Examples

### Example 1: Education as Non-Creatable Child

```d3e
Model {
    name 'Education'
    creatable false
    properties [
        {
            name 'Institution'
            type Institution
            required true
        }
        {
            name 'Degree'
            type String
            required true
        }
        {
            name 'Start Date'
            type Date
            required true
        }
        // ... other properties ...
    ]
}
```

### Example 2: FamilyInfo and Child as Non-Creatable

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

**Note:**
- Use `creatable false` to prevent direct creation or management of the model.
- Non-creatable models are used as part of other models only.
