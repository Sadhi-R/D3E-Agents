# Model with Computed Properties

## Context 

The term "Computed" typically refers to computed properties or computed fields within a model. Computed properties allow you to define dynamic values that are calculated based on the values of other properties within the same model. These computed properties are not stored directly in the database but are calculated on-the-fly when requested.

Computed properties are useful for deriving values dynamically, performing calculations, or aggregating data without directly storing the computed result in the database.

A computed property is a property whose value is automatically calculated based on other properties in the model, using an expression. Computed properties are read-only and cannot be set directly by users or APIs. They are useful for deriving values, combining fields, or performing calculations that should always reflect the current state of the model.

- **Automatic Calculation:** The value is always up-to-date, based on the computation expression.
- **Read-Only:** Computed properties cannot be set directly; they are derived from other data.
- **Syntax:** Use `computed true` and provide a `computation` expression in backticks.

## Prompt for Creating

"Create a [ModelName] model with a computed property [propertyName] that calculates [description of computation]"

**Example Prompts:**

- "Create a User model with a computed property fullName that combines firstName and lastName"
- "Create a Student model with a computed property isAdult that is true if age >= 18"
- "Create a Lead model with a computed property handlingUser that returns the assigned user from leadAssignment"

## D3E Examples

### Example 1: User with Full Name (Simple Computation)

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
            name 'Full Name'
            type String
            computed true
            computation `firstName + ' ' + lastName`
        }
    ]
}
```

### Example 2: Student with isAdult (Conditional Computation)

```d3e
Model {
    name 'Student'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'Age'
            type Integer
        }
        {
            name 'isAdult'
            type Boolean
            computed true
            computation `age >= 18`
        }
    ]
}
```

### Example 3: Lead with handling User (Reference Computation)

```d3e
Model {
    name 'Lead'
    properties [
        // ... other properties ...
        {
            name 'Lead Assignment'
            type LeadAssignment
        }
        {
            name 'handling User'
            type User
            computed true
            computation `leadAssignment != null ? leadAssignment.assignedTo : null`
        }
    ]
}
```

**Note:**

- Use `computed true` to mark a property as computed.
- The `computation` attribute must be a valid D3E expression, wrapped in backticks.
- Computed properties are always read-only and cannot be set directly.
- Computed properties can reference other properties, perform calculations, or use conditional logic.

