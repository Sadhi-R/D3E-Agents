# Model with Long Text Properties

## Context

A long text property is used when a model needs to store large amounts of textual data, such as descriptions, notes, email bodies, or conversations. In D3E, you mark a property as long text using the `longText true` attribute. This signals that the property may contain more data than a typical short string, and the UI or storage may optimize for large text blocks (e.g., multi-line editors, larger database fields).

- **Purpose:** For storing large or multi-line text, such as descriptions, messages, or logs.
- **Type:** Always used with `type String`.
- **Attribute:** Use `longText true` to indicate the property is intended for long text.

## Prompt for Creating

"Create a [ModelName] model with a long text property [propertyName]"

**Example Prompts:**
- "Create a Lead model with a long text property Expressed Needs"
- "Create an Interaction model with a long text property Conversation"
- "Create a MailMessage model with a long text property Body"
- "Create a model with a property Description for storing detailed notes (long text)"

## D3E Examples

### Example 1: Lead with Expressed Needs and Identified Pain Points (Long Text)

```d3e
Model {
    name 'Lead'
    properties [
        {
            name 'Expressed Needs'
            type String
            longText true
        }
        {
            name 'Identified Pain Points'
            type String
            longText true
        }
    ]
}
```

### Example 2: Interaction with Conversation and Body (Long Text)

```d3e
Model {
    name 'Interaction'
    properties [
        {
            name 'Conversation'
            type String
            longText true
        }
        {
            name 'Body'
            type String
            longText true
        }
    ]
}
```

### Example 3: Mail Message with Body and Content (Long Text)

```d3e
Model {
    name 'Mail Message'
    properties [
        {
            name 'Body'
            type String
            longText true
        }
        {
            name 'Content'
            type String
            longText true
        }
    ]
}
```

**Note:**
- Use `longText true` only with properties of type `String`.
- Long text properties are ideal for fields that may contain paragraphs, formatted text, or large notes.
- The UI may render long text fields as multi-line editors or text areas.
- There is no enforced maximum length, but use long text only when necessary for performance and clarity.
