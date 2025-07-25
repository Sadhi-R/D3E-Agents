# Model with Read Types

## Context

"Read Type" in D3E Studio is a feature related to access control, specifically governing permissions for reading or writing objects within a model.

### Types of Read Type

| Read Type      | Description                                      |
| -------------- | ------------------------------------------------ |
| Read and Write | Default. Property can be read and written.       |
| Write Once     | Can be set only once, then becomes read-only.    |
| Read Only      | Can only be read, never written after creation.  |
| Local          | Exists only on client, not sent to server.       |

## Prompt for Creating

"Create a [ModelName] model with [property1], [property2], ... and set [propertyX] as [read type]"

**Example Prompts:**

- "Create a Report model with name, title, publishedYear and set the title property as read-only."
- "Create a User model with username, email, password and set the email property as write-once."
- "Create a Session model with token, userId, lastActive and set the token property as local."

## D3E Example

```d3e
(Model Report) {
    name 'Report'
    properties [
        {
            name 'Title'
            type String
            readType ReadOnly // Cannot be changed after creation
        }
        {
            name 'PublishedYear'
            type Integer
            readType WriteOnce // Can be set only once
        }
        {
            name 'DraftNotes'
            type String
            readType Local // Only exists on client
        }
        {
            name 'Summary'
            type String
            // Default is Read and Write
        }
    ]
}
``` 