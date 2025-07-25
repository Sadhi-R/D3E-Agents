# D3E OptionSets STRUCTURE

## Introduction

In D3E Studio, **OptionSets** are used to define a fixed set of possible values for a property, similar to enums in other programming languages. OptionSets help enforce data integrity, improve readability, and simplify validation by restricting a property's value to a predefined list of options.

OptionSets are commonly used for statuses, categories, types, and any field where the value should be chosen from a limited set.

---


## OptionSet Syntax

A D3E OptionSet is defined using the following structure. The `package` field is optional and not required for most OptionSets:

```d3e
OptionSet {
    name 'OptionSetName'
    options [
        {
            name 'OptionName1'
        }
        {
            name 'OptionName2'
        }
        // ... more options ...
    ]
}
```

If you need to group OptionSets by package, you can add the `package` field, but it is not mandatory for most use cases.

For advanced OptionSets with attributes, use:

```d3e
OptionSet {
    name 'OptionSetName'
    attributes [
        {
            name 'AttributeName'
            type Type
            [collection true]
            [required true]
            [description 'Description of the attribute']
        }
        // ... more attributes
    ]
    options [
        {
            name 'OptionName'
            [attributes {
                AttributeName AttributeValue
                // ... more attribute values
            }]
        }
        // ... more options
    ]
}
```

### D3E OptionSet Syntax Rules

- **NO COMMAS**: Never use commas between items in collections or arrays
- **Identities**: Computed from names using camelCase/PascalCase
- **Optional Fields**: Properties in brackets [ ] are optional
- **Option Values**: If not specified, the option's name is used as its value

---

## OptionSet Fields

| Field           | Description                                                      |
| --------------- | --------------------------------------------------------------- |
| **Name**        | The unique identifier for the OptionSet or option                |
| **Options**     | The list of possible values                                      |
| **Value**       | The actual value stored (optional, defaults to option name)      |
| **Description** | Human-readable explanation of the option                         |
| **DefaultValue**| The default option if none is specified (optional)               |

---

## OptionSet Attributes

OptionSets in D3E can be extended with **attributes**—additional fields that provide more information or functionality for each option. Attributes are useful when each option needs to store extra data, such as a display color, a code, or a list of related values.

### Attribute Fields

| Field         | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **name**      | The unique identifier for the attribute within the OptionSet.               |
| **type**      | The data type of the attribute (e.g., String, Integer, Boolean, OptionSet). |
| **collection**| If true, the attribute holds a list of values (array).                      |
| **required**  | If true, the attribute must have a value for each option.                   |
| **description**| Human-readable explanation of the attribute.                               |


### Simple OptionSet Example (Most Common)

```d3e
OptionSet {
    name 'InteractionType'
    options [
        { name 'Call' }
        { name 'SMS' }
        { name 'WhatsApp' }
        { name 'Video Call' }
        { name 'Email' }
        { name 'Meeting' }
        { name 'Demo' }
        { name 'Webinar' }
        { name 'Conference' }
        { name 'Other' }
        { name 'Voicemail' }
    ]
}
```

```d3e
OptionSet {
    name 'LeadStatus'
    options [
        { name 'New' }
        { name 'Contacted' }
        { name 'Inprogress' }
        { name 'Closed' }
    ]
}
```

### OptionSet with Attributes: Syntax

```d3e
OptionSet {
    name 'Countries'
    attributes [
        {
            name 'timezone'
            type String
            collection true
            description 'List of timezones for the country'
        }
        {
            name 'currency'
            type String
            required true
            description 'Primary currency'
        }
    ]
    options [
        {
            name 'USA'
            attributes {
                timezone [ 'UTC-5', 'UTC-6', 'UTC-7', 'UTC-8' ]
                currency 'USD'
            }
        }
        {
            name 'Japan'
            attributes {
                timezone [ 'UTC+9' ]
                currency 'JPY'
            }
        }
    ]
}
```

---

## Example OptionSets

### Basic OptionSet

```d3e
OptionSet {
    name 'OrderStatus'
    options [
        { name 'Pending' }
        { name 'Processing' }
        { name 'Completed' }
        { name 'Cancelled' }
    ]
    defaultValue 'Pending'
}
```

### OptionSet with Attributes

```d3e
OptionSet {
    name 'Countries'
    attributes [
        {
            name 'timezone'
            type String
            collection true
        }
        {
            name 'currency'
            type String
            required true
        }
    ]
    options [
        {
            name 'USA'
            attributes {
                timezone [ 'UTC-5', 'UTC-6', 'UTC-7', 'UTC-8' ]
                currency 'USD'
            }
        }
        {
            name 'Japan'
            attributes {
                timezone [ 'UTC+9' ]
                currency 'JPY'
            }
        }
    ]
}
```

---

## Using OptionSets in Models

OptionSets are referenced in model properties to restrict values:

```d3e
{
    name 'Status'
    type OrderStatus
    defaultValue `OrderStatus.Pending`
}
```

- The property type is set to the OptionSet name.
- The default value can reference an OptionSet option.

---

## Best Practices

1. **Naming**: Use clear, descriptive names for OptionSets and options
2. **Descriptions**: Add descriptions for clarity, especially for non-obvious options
3. **Default Values**: Specify a default option when appropriate
4. **Consistency**: Use OptionSets for all fields with a limited set of valid values
5. **Attributes**: Use attributes for extra metadata when options need more than just a name/value
6. **Type and validation**: Always specify the correct type and use `required` for essential data
7. **Collections**: Use `collection true` for lists (e.g., multiple timezones)
8. **Documentation**: Add descriptions to attributes for clarity
9. **Package Organization**: Group related OptionSets in packages

---

## Summary

OptionSets in D3E provide a robust way to define and enforce fixed sets of values for model properties. With attributes, OptionSets become even more powerful, allowing each option to carry additional structured data. This improves data integrity, code readability, and validation, and supports advanced use cases for building reliable and maintainable D3E applications.
