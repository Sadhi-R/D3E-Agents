
### Context

The `referenceFrom` attribute is used to specify that a property in a model references another property within the same model. This is useful for establishing relationships or associations between different properties of the same model, such as parent-child hierarchies or linked tasks.

- **Use Case:** Use `referenceFrom` when you want to relate two properties within the same model, such as a parent task referencing a collection of tasks.
- **Independence:** Reference properties using `referenceFrom` are still independent and do not embed the referenced data.

### Example Prompt

"Create a TaskModel with a property parentTask that references the tasks property in the same model."

### D3E Example

```d3e
Model {
    name 'TaskModel'
    properties [
        {
            name 'parentTask'
            type TaskModel
            referenceFrom tasks
        }
        {
            name 'tasks'
            type Tasks
        }
    ]
}
```

### Notes
- Use `referenceFrom` to indicate intra-model references, such as parent-child or linked relationships.
- The referenced property (e.g., `tasks`) should exist in the same model.
- This is useful for hierarchical or graph-like data structures.

---

**General Notes:**
- Reference properties are used to create links between models, enabling navigation and queries across related data.
- Use the model name as the type for reference properties.
- For bidirectional relationships, use `inverse true` and specify `inverseProperty`.
- Reference properties can be required or optional.
- Use `collection true` if a property should reference multiple instances of another model.
