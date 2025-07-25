# Model with Conditional Properties

## Context

A conditional property is a property that only exists or is relevant when certain conditions are met, based on the values of other properties in the same model. This is achieved using the `existsIf` attribute in D3E, which takes an expression that determines whether the property should be present. Conditional properties are useful for modeling scenarios where some fields are only applicable in specific cases (e.g., contract details for contract employees, manager-only settings, etc.).

- **Dynamic Presence:** The property is only available if the condition in `existsIf` evaluates to true.
- **Contextual Modeling:** Helps keep models clean and relevant to the current context or state.

## Prompt for Creating

"Create a [ModelName] model with a property [propertyName] that only exists if [condition]"

**Example Prompts:**

- "Create an Employee model with a property contractDetails that only exists if employmentType is 'Contract'"
- "Create a User model with a property accessTwilioConfiguration that only exists if role is Manager"
- "Create a Student model with a property scholarshipAmount that only exists if hasScholarship is true"

## D3E Examples

### Example 1: Employee with Contract Details (Conditional Property)

```d3e
Model {
    name 'Employee'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'Employment Type'
            type String
        }
        {
            name 'Contract Details'
            type String
            existsIf `employmentType == 'Contract'`
        }
    ]
}
```

### Example 2: User with Access Twilio Configuration (Conditional Property)

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Role'
            type UserRole
        }
        {
            name 'Access Twilio Configuration'
            type Boolean
            existsIf `role == UserRole.Manager`
        }
    ]
}
```

### Example 3: Student with Scholarship Amount (Conditional Property)

```d3e
Model {
    name 'Student'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'Has Scholarship'
            type Boolean
        }
        {
            name 'Scholarship Amount'
            type Double
            existsIf `hasScholarship == true`
        }
    ]
}
```

**Note:**

- Use `existsIf` with a valid D3E expression (in backticks) to control when a property is present.
- Conditional properties help keep your data model relevant and avoid unnecessary fields.
- The condition can reference any other property in the same model.
