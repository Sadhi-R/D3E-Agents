# Model with Collection Properties

## Context

A collection property allows a model to hold a list (array) of values, rather than a single value. Collections are useful when you need to represent multiple items of the same type within a model, such as a list of skills, emails, or related entities. Collections can be of primitive types (e.g., String, Integer) or references to other models. Collections are defined using the `collection true` attribute in D3E.

- **Multiplicity:** Collection properties represent zero or more values of the specified type.
- **Type:** The type can be a primitive (String, Integer, etc.), an OptionSet, or another Model.
- **Independence:** Unlike child properties, collection items do not have to be dependent on the parent unless also marked as `child true`.

## Prompt for Creating

"Create a [ModelName] model with a collection property [propertyName] of type [Type]"

**Example Prompts:**
- "Create a student model with name, email,phone number,passed Subjects and Enrolled Courses ,and age "
- "Create a Lead model with a collection of skills (String) and a collection of education history (Education model)"
- "Create a Contact model with phone numbers as a collection of strings"

## D3E Examples

### Example 1: Lead with Skills and Education History (Collections)

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
            name 'Skills'
            type String
            collection true
        }
        {
            name 'Education History'
            type Education
            collection true
            child true // If Education is a child, otherwise omit
        }
    ]
}

Model {
    name 'Education'
    creatable false
    properties [
        {
            name 'Institution'
            type String
            required true
        }
        {
            name 'Degree'
            type String
            required true
        }
    ]
}
```

### Example 2: Interaction with Notes and Participants (Primitive Collections)

```d3e
Model {
    name 'Interaction'
    properties [
        {
            name 'Notes'
            type String
            collection true
        }
        {
            name 'Participants'
            type String
            collection true
        }
    ]
}
```

### Example 3: Contact with Phone Numbers (Primitive Collection)

```d3e
Model {
    name 'Contact'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'Phone Numbers'
            type String
            collection true
        }
    ]
}
```

**Note:**

- Use `collection true` to indicate a property is a list/array.
- The type can be primitive, OptionSet, or another Model.
- If the collection is of another model and should be tightly coupled (created/deleted with parent), also use `child true`.
- Collections can be empty (zero items) or have multiple items.
- Do not use commas between items in D3E syntax.