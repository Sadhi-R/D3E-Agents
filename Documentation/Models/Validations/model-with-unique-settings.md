# Model with Unique Settings

## Context

Unique settings in D3E models allow you to define a combination of properties that must be unique together. This ensures that no two records in the model have the same combination of values for the selected properties. Unique settings are useful for enforcing business rules where uniqueness depends on multiple fields, such as a combination of employee ID and email, or product code and warehouse location. You can also specify a custom error message to be displayed when the uniqueness constraint is violated.

- **Composite Uniqueness:** Ensures a combination of properties is unique across all records.
- **Custom Error Message:** Provides a clear message when the uniqueness rule is not satisfied.
- **Syntax:** Use the `uniqueSettings` block with `properties` and `errorMessage`.

## Prompt for Creating

"Create a [ModelName] model with properties [property1, property2, ...] where the combination of [propertyA, propertyB, ...] must be unique, with error message '[error message]'"

**Example Prompts:**

- "Create an Employee model with employeeId, email, and department, where the combination of employeeId and email must be unique, with error message 'Combination of Employee ID and Email must be unique.'"
- "Create a Product model with productCode and warehouse, where the combination of productCode and warehouse must be unique, with error message 'Product code must be unique per warehouse.'"
- "Create a Booking model with roomNumber and date, where the combination of roomNumber and date must be unique, with error message 'Room is already booked for this date.'"

## D3E Examples

### Example 1: Employee with Unique Employee ID and Email

```d3e
Model {
    name 'Employee'
    properties [
        {
            name 'employeeId'
            type String
        }
        {
            name 'email'
            type String
        }
        {
            name 'department'
            type String
        }
    ]
    uniqueSettings [
        {
            properties [ 'employeeId', 'email' ]
            errorMessage 'Combination of Employee ID and Email must be unique.'
        }
    ]
}
```

### Example 2: Product with Unique Product Code per Warehouse

```d3e
Model {
    name 'Product'
    properties [
        {
            name 'productCode'
            type String
        }
        {
            name 'warehouse'
            type String
        }
    ]
    uniqueSettings [
        {
            properties [ 'productCode', 'warehouse' ]
            errorMessage 'Product code must be unique per warehouse.'
        }
    ]
}
```

### Example 3: Booking with Unique Room and Date

```d3e
Model {
    name 'Booking'
    properties [
        {
            name 'roomNumber'
            type String
        }
        {
            name 'date'
            type Date
        }
    ]
    uniqueSettings [
        {
            properties [ 'roomNumber', 'date' ]
            errorMessage 'Room is already booked for this date.'
        }
    ]
}
```

**Note:**

- Use `uniqueSettings` for composite uniqueness constraints.
- The `properties` list defines which fields must be unique together.
- The `errorMessage` provides user-friendly feedback when the rule is violated.
