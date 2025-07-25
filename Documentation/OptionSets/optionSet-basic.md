# Basic OptionSet

## Context

A basic OptionSet defines a fixed set of possible values for a property, similar to an enum in other languages. It is used when you want to restrict a property to a small, well-defined set of options. Basic OptionSets are ideal for simple status fields, categories, or types where no extra metadata is needed for each option.

- **Simplicity:** Use a basic OptionSet when you only need option names, without custom values or descriptions.
- **Data Integrity:** Ensures only valid, predefined values are used for a property.

## Prompt for Creating

"Create an OptionSet [OptionSetName] with options [Option1], [Option2], [Option3]"

**Example Prompts:**
- "Create an OptionSet PaymentMethod with options Cash, CreditCard, BankTransfer, UPI"
- "Create an OptionSet OrderStatus with options Pending, Processing, Completed, Cancelled"

## D3E Example

```d3e
OptionSet {
    name 'PaymentMethod'
    options [
        { name 'Cash' }
        { name 'CreditCard' }
        { name 'BankTransfer' }
        { name 'UPI' }
    ]
}
```
