# Transient Model

## Context

A transient model in D3E is not persisted or stored in the database. It exists only temporarily during the execution of certain actions or processes and is not permanently saved to data storage. Transient models are useful for representing temporary or calculated values that are needed for a specific operation, calculation, or workflow, but do not need to be retained after the operation completes.

- **Not Persisted:** Transient models are not saved to the database.
- **Temporary Use:** Useful for temporary data, calculations, or workflow state.
- **Syntax:** Use `transient true` in the model definition.

## Prompt for Creating

"Create a [ModelName] model with transient true for temporary or calculated data"

**Example Prompts:**
- "Create a LeadImportFile model with transient true for file import operations"
- "Create a Calculation model with transient true for temporary results"
- "Create a SessionData model with transient true for session-specific information"

## D3E Examples

### Example 1: LeadImportFile as Transient Model

```d3e
Model {
    name 'LeadImportFile'
    properties [
        {
            name 'File'
            type DFile
        }
    ]
    transient true
    actions [
        {
            name 'CreateLead'
            block ```
                ImportCSVFileUtils.createLeadData(this.file);
            ```
        }
    ]
}
```

### Example 2: Calculation as Transient Model

```d3e
Model {
    name 'Calculation'
    properties [
        {
            name 'Input'
            type Double
        }
        {
            name 'Temporary Result'
            type Double
        }
    ]
    transient true
}
```

**Note:**
- Use `transient true` to indicate a model is not persisted.
- Transient models are ideal for temporary or calculated values needed only during a specific process.
