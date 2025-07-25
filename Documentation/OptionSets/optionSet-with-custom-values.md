# OptionSet with Custom Values

## Context

An OptionSet with custom values allows each option to have a specific value, which may be different from its name. This is useful when you need to map options to codes, numbers, or other identifiers for integration, storage, or display purposes.

- **Custom Mapping:** Use when options need to correspond to specific values (e.g., for APIs, databases, or business logic).
- **Clarity:** Makes it clear what value is stored or transmitted for each option.

## Prompt for Creating

"Create an OptionSet [OptionSetName] with options [Option1:Value1], [Option2:Value2], ..."

**Example Prompts:**
- "Create an OptionSet PriorityLevel with options Low:1, Medium:2, High:3, Critical:4"
- "Create an OptionSet AccessLevel with options Guest:0, User:1, Admin:2"

## D3E Example

```d3e
OptionSet {
    name 'PriorityLevel'
    options [
        { name 'Low' value '1' }
        { name 'Medium' value '2' }
        { name 'High' value '3' }
        { name 'Critical' value '4' }
    ]
    defaultValue 'Low'
}
```

**Usage in a model property:**

```d3e
{
    name 'Level'
    type PriorityLevel
    defaultValue `PriorityLevel.Low`
}
``` 