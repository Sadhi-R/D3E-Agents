# Model with OptionSet Properties

## Context

An OptionSet property allows a model to restrict the value of a property to a predefined set of options, similar to enums in other languages. This is useful for fields where only certain values are valid, such as status, priority, or roles. OptionSets are defined separately and referenced as the type of a property in a model. This ensures data consistency and makes the model more expressive and robust.

- **Type:** The type of the property is set to the name of the OptionSet (e.g., `LeadStatus`, `UserRole`).
- **Validation:** The property can only take values defined in the referenced OptionSet.
- **Usage:** OptionSet properties can be required, have default values, or be used in conditional logic.
- **OptionSet Syntax:**
    - Use `options` (not `values`).
    - Each option is an object with a `name` field.
    - Optionally, include a `package` field for namespacing.

## Prompt for Creating

"Create a [ModelName] model with [property1] ([OptionSet1]), [property2] ([OptionSet2]), and [property3] ([OptionSet3])"

**Example Prompts:**
- "Create a User model with first name, last name, email, role (UserRole), and marital status (MaritalStatus)"
- "Create an Employee model with employee ID, full name, email, department (Department), employment type (EmploymentType), and experience level (ExperienceLevel)"
- "Create a Task model with title, description, category (TaskCategory), status (TaskStatus), and priority (TaskPriority)"
- "Create a MicroSoftAcc model with oauthStatus (OAuthCredentialsStatus)"

## D3E Examples

### Example 1: User with Role and Marital Status (OptionSets)

```d3e
Model {
    name 'User'
    properties [
        {
            name 'First Name'
            type String
            required true
        }
        {
            name 'Last Name'
            type String
            required true
        }
        {
            name 'Email'
            type String
            required true
        }
        {
            name 'Role'
            type UserRole
            required true
        }
        {
            name 'Marital Status'
            type MaritalStatus
            required false
        }
    ]
}

OptionSet {
    package 'lead.management'
    name 'UserRole'
    options [
        { name 'Sales Person' },
        { name 'Manager' },
        { name 'Admin' }
    ]
}

OptionSet {
    name 'MaritalStatus'
    options [
        { name 'Single' },
        { name 'Married' },
        { name 'Divorced' },
        { name 'Widowed' },
        { name 'Prefer Not To Say' }
    ]
}
```

### Example 2: Family Info with Marital Status (OptionSet)

```d3e
Model {
    name 'Family Info'
    creatable false
    properties [
        {
            name 'Spouse Name'
            type String
        }
        {
            name 'Children'
            type Child
            collection true
            child true
        }
        {
            name 'Marrital Status'
            type MaritalStatus
        }
        {
            name 'Family Income'
            type Double
        }
    ]
}

OptionSet {
    name 'MaritalStatus'
    options [
        { name 'Single' },
        { name 'Married' },
        { name 'Divorced' },
        { name 'Widowed' },
        { name 'Prefer Not To Say' }
    ]
}
```

### Example 3: Interaction with Type, Call Status, and Message Status (OptionSets)

```d3e
Model {
    name 'Interaction'
    properties [
        {
            name 'Type'
            type InteractionType
        }
        {
            name 'Call Status'
            type CallStatus
        }
        {
            name 'Message Status'
            type MessageStatus
        }
    ]
}

OptionSet {
    package 'lead.management'
    name 'InteractionType'
    options [
        { name 'Call' },
        { name 'SMS' },
        { name 'WhatsApp' },
        { name 'Video Call' },
        { name 'Email' },
        { name 'Meeting' },
        { name 'Demo' },
        { name 'Webinar' },
        { name 'Conference' },
        { name 'Other' },
        { name 'Voicemail' }
    ]
}

OptionSet {
    name 'CallStatus'
    options [
        { name 'Initiated' },
        { name 'InProgress' },
        { name 'Ringing' },
        { name 'Answered' },
        { name 'Completed' },
        { name 'Failed' },
        { name 'Busy' },
        { name 'Unanswered' },
        { name 'Unknown' },
        { name 'Connecting' },
        { name 'Cancelled' },
        { name 'Rejected' }
    ]
}

OptionSet {
    name 'MessageStatus'
    options [
        { name 'Sent' },
        { name 'Delivered' },
        { name 'Read' },
        { name 'Failed' }
    ]
}
```

### Example 4: MicroSoftAcc with OAuthCredentialsStatus (OptionSet)

```d3e
Model {
    name 'MicroSoftAcc'
    properties [
        {
            name 'user'
            type User
        }
        {
            name 'accessToken'
            type String
            longText true
        }
        {
            name 'refreshToken'
            type String
            longText true
        }
        {
            name 'tokenExpersAt'
            type DateTime
        }
        {
            name 'oauthStatus'
            type OAuthCredentialsStatus
        }
    ]
}

OptionSet {
    name 'OAuthCredentialsStatus'
    options [
        { name 'Active' },
        { name 'Expired' },
        { name 'Revoked' }
    ]
}
```

**Note:**
- Use OptionSet properties to enforce valid values and improve data quality.
- OptionSet types can be used in conditional logic (e.g., `existsIf`), required fields, or with default values.
- OptionSets are defined separately and referenced by name in the model property type. 