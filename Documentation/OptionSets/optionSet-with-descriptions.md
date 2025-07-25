# OptionSet with Descriptions

## Context

An OptionSet with descriptions provides a human-readable explanation for each option. This is helpful for improving clarity in the UI, documentation, and for developers who need to understand the meaning of each option.

- **Documentation:** Descriptions make it easier for users and developers to understand the purpose of each option.
- **UI Clarity:** Useful for displaying tooltips or help text in forms and interfaces.

## Prompt for Creating

"Create an OptionSet [OptionSetName] with options [Option1:Description1], [Option2:Description2], ..."

**Example Prompts:**
- "Create an OptionSet EmployeeStatus with options Active:Currently employed, OnLeave:Temporarily on leave, Resigned:No longer employed, Retired:Retired from service"
- "Create an OptionSet TaskStatus with options Open:Task is open, InProgress:Task is being worked on, Done:Task is completed"

## D3E Example

```d3e
OptionSet {
    name 'EmployeeStatus'
    options [
        { name 'Active' description 'Currently employed and active' }
        { name 'OnLeave' description 'Temporarily on leave' }
        { name 'Resigned' description 'No longer employed' }
        { name 'Retired' description 'Retired from service' }
    ]
    defaultValue 'Active'
}
```

**Usage in a model property:**

```d3e
{
    name 'Status'
    type EmployeeStatus
    defaultValue `EmployeeStatus.Active`
}
``` 