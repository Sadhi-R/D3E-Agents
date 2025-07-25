# Model with Transient Properties

## Context

A transient property is a property that is not persisted or stored in the database. It exists only temporarily during the execution of certain actions or processes and is not permanently saved to data storage. Transient properties are useful for representing temporary or calculated values that are needed for a specific operation, calculation, or workflow, but do not need to be retained after the operation completes.

- **Not Persisted:** Transient properties are not saved to the database.
- **Temporary Use:** Useful for temporary data, calculations, or workflow state.
- **Syntax:** Use `transient true` in the property definition.

## Prompt for Creating

"Create a [ModelName] model with fields [field1, field2, ...], where [fieldX] is transient"

**Example Prompts:**
- "Create a Calculation model with input, temporaryResult, where temporaryResult is transient"
- "Create an UploadSession model with sessionId, uploadToken, where uploadToken is transient"
- "Create a Report model with title, content, cache, where cache is transient"

## D3E Examples

### Example 1: Calculation with Transient Property

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
            transient true
        }
    ]
}
```

### Example 2: UploadSession with Transient Token

```d3e
Model {
    name 'UploadSession'
    properties [
        {
            name 'SessionId'
            type String
            required true
        }
        {
            name 'UploadToken'
            type String
            transient true
        }
    ]
}
```

**Note:**
- Use `transient true` to indicate a property or model is not persisted.
- Transient properties are ideal for temporary or calculated values needed only during a specific process.
- They are not available after the operation completes or after the model is reloaded from the database.
