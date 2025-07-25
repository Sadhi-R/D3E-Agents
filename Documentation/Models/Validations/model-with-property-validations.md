# Model with Property Validations

## Context

Property validations in D3E are rules that check the value of a single property before accepting it. These validations help ensure data integrity by enforcing constraints such as uniqueness, format, or value range at the property level. Property validations are defined in the `validations` block of a model and are evaluated automatically during create and update operations.

- **Single-Field Check:** Validates one property at a time.
- **Automatic Enforcement:** The system checks the rule before saving data.
- **Syntax:** Use the `validations` block with an `expression` and `errorMsg`.

## Prompt for Creating

"Create a [ModelName] model with a property [propertyName] that must satisfy [validation rule]"

**Example Prompts:**

- "Create a User model with an email property that must be unique"
- "Create a Student model with an age property that must be greater than 0"
- "Create a Product model with a price property that must be positive"

## D3E Examples

### Example 1: Unique Email Validation

```d3e
Model {
    name 'User'
    properties [
        {
            name 'Email'
            type String
            required true
            unique true
            validations [
        {
            errorMsg 'Email must be unique'
            expression `email.isUnique()`
        }
    ]
        }
    ]

}
```

### Example 2: Age Greater Than Zero

```d3e
Model {
    name 'Student'
    properties [
        {
            name 'Age'
            type Integer
            required true
            validations [
        {
            errorMsg 'Age must be greater than 0'
            expression `age > 0`
        }
    ]
        }
    ]

}
```

### Example 3: Positive Price

```d3e
Model {
    name 'Product'
    properties [
        {
            name 'Price'
            type Double
            required true
            validations [
        {
            errorMsg 'Price must be positive'
            expression `price > 0`
        }
    ]
        }
    ]

}
```

**Note:**

- Use property validations to enforce rules on individual fields.
- The `expression` should reference only the property being validated.
- The `errorMsg` is shown if the validation fails.
