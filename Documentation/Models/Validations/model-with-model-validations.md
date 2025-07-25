# Model with Model Validations

## Context

Model validations in D3E are rules that check the relationship between multiple properties in a model. These validations help ensure data integrity by enforcing constraints that depend on more than one field, such as date ranges or cross-field dependencies. Model validations are defined in the `validations` block of a model and are evaluated automatically during create and update operations.

- **Cross-Field Check:** Validates rules involving multiple properties.
- **Automatic Enforcement:** The system checks the rule before saving data.
- **Syntax:** Use the `validations` block with an `expression` and `errorMsg`.

## Prompt for Creating

"Create a [ModelName] model with properties [property1, property2, ...] where [validation rule involving multiple properties]"

**Example Prompts:**
- "Create an Event model with startDate and endDate where endDate must be after startDate"
- "Create a Booking model with checkIn and checkOut where checkOut must be after checkIn"
- "Create a Project model with start and deadline where deadline must be after start"

## D3E Examples

### Example 1: End Date After Start Date

```d3e
Model {
    name 'Event'
    properties [
        {
            name 'Start Date'
            type Date
            required true
        }
        {
            name 'End Date'
            type Date
            required true
        }
    ]
    validations [
        {
            errorMsg 'End date must be after start date'
            expression `endDate > startDate`
        }
    ]
}
```

### Example 2: Booking with Check-In and Check-Out

```d3e
Model {
    name 'Booking'
    properties [
        {
            name 'Check In'
            type DateTime
            required true
        }
        {
            name 'Check Out'
            type DateTime
            required true
        }
    ]
    validations [
        {
            errorMsg 'Check-out must be after check-in'
            expression `checkOut > checkIn`
        }
    ]
}
```

### Example 3: Project with Start and Deadline

```d3e
Model {
    name 'Project'
    properties [
        {
            name 'Start'
            type Date
            required true
        }
        {
            name 'Deadline'
            type Date
            required true
        }
    ]
    validations [
        {
            errorMsg 'Deadline must be after start date'
            expression `deadline > start`
        }
    ]
}
```

**Note:**
- Use model validations for rules involving multiple fields.
- The `expression` can reference any property in the model.
- The `errorMsg` is shown if the validation fails.
