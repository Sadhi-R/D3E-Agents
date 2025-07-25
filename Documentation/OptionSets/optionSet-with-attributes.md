# OptionSet with Attributes

## Context

OptionSets in D3E can be extended with attributes—additional fields that provide more information or functionality for each option. Attributes are useful when each option needs to store extra data, such as a display color, a code, or a list of related values.

- **Rich Metadata:** Use attributes to add structured data to each option.
- **Validation:** Attributes can be required or optional, and can be single values or collections.

## Prompt for Creating

"Create an OptionSet [OptionSetName] with attributes [Attribute1:Type1], [Attribute2:Type2], ... and options [Option1], [Option2], ..."

**Example Prompts:**
- "Create an OptionSet Countries with attributes timezone:String (collection), currency:String (required) and options USA, Japan"
- "Create an OptionSet Status with attribute color:String and options Active, Inactive, Pending"

## D3E Example

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

**Usage in a model property:**

```d3e
{
    name 'Country'
    type Countries
    required true
}
```

## Best Practices

1. **Use attributes for extra metadata:** Only add attributes when options need more than just a name/value.
2. **Type and validation:** Always specify the correct type and use `required` for essential data.
3. **Collections:** Use `collection true` for lists (e.g., multiple timezones).
4. **Documentation:** Add descriptions to attributes for clarity. 