# Widget with Styles

## What is a Widget with Styles?
A **Widget with Styles** applies reusable visual characteristics to its UI elements using style references. Styles ensure consistent appearance and reuse of visual design across widgets.

## Prompt Template
"Create a widget with styles that [describe the style usage, e.g., applies a primary button style]."

## Example Prompts
- Create a button widget that uses the 'Primary' style.
- Build a card widget with custom background and padding styles.
- Make a text widget with a style for font size and color.
- Design a popup widget using a modal style and styled header.
- Apply error and label styles to form fields.

## D3E Examples

### 1. Applying a Style to a Container View
```d3e
Widget {
    name 'UserProfileView'
    build Column {
        styles [BaseViewStyle]
        children [
            // ... other children ...
        ]
    }
}
```
*This applies a reusable `BaseViewStyle` to the main column, ensuring consistent padding, background, or other layout properties.*

---

### 2. Using Multiple Styles for Nested Elements
```d3e
Widget {
    name 'CallRecordingNoteWidget'
    build Column {
        styles [CardPadding]
        children [
            // ... other children ...
            Column {
                styles [CardMargin, CardPadding]
                children [
                    TextView {
                        data {
                            data `interaction.conversation`
                        }
                    }
                ]
            }
        ]
    }
}
```
*Here, both `CardMargin` and `CardPadding` styles are applied to a nested column for combined effects.*

---

### 3. Styling Buttons with Semantic Styles
```d3e
Widget {
    name 'CancelSaveButtonsWidget'
    build Row {
        children [
            Button {
                styles [Secondary]
                child TextView {
                    data { data 'Cancel' }
                }
            }
            Button {
                styles [Primary]
                child TextView {
                    data { data 'Save' }
                }
            }
        ]
    }
}
```
*This demonstrates using `Primary` and `Secondary` button styles for visual hierarchy.*

---

### 4. Styling Text Elements
```d3e
Widget {
    name 'BooleanRadioView'
    build Column {
        children [
            TextView {
                styles [LabelText]
                data { data `this.name` }
            }
            TextView {
                styles [ErrorText]
                data { data `item` }
            }
        ]
    }
}
```
*Text elements use `LabelText` for labels and `ErrorText` for error messages, ensuring consistent typography and color.*

---

### 5. Popup and Dialog Styles
```d3e
Widget {
    name 'ApolloLeadDetailsView'
    build Column {
        styles [DefaultPopUp]
        children [
            TextView {
                styles [HeadlineFour]
                data { data 'Lead Details' }
            }
            // ... more fields ...
        ]
    }
}
```
*The `DefaultPopUp` style is used for modal or popup layouts, while `HeadlineFour` is used for section headers.*

---

## More Real-World Examples

### Example 1: CallRecordingNoteWidget
```d3e
Widget {
    package 'lead.management'
    name 'CallRecordingNoteWidget'
    category 'UserDefined'
    properties [
        {
            name 'Interaction'
            type Interaction
            required true
            synchronise true
        }
        {
            name 'IsaddNote'
            type Boolean
            internal true
        }
        {
            name 'note'
            type String
            internal true
        }
        {
            name 'isNote'
            type Boolean
            internal true
        }
        {
            name 'Conversation'
            type Boolean 
            required true
        }
    ]
    build Column {
        name 'Column2'
        styles [CardPadding]
        data {
            crossAxisAlignment 'start'
            decoration {
                border {
                    color 'ffe8e1e1'
                    width '1'
                }
                borderRadius '3'
            }
            margin '0 30 7 30'
        }
        children [
            // ... (children omitted for brevity) ...
            CIf {
                name 'CIf'
                condition `interaction != null && interaction.file != null && interaction.type == InteractionType.Call`
                then Column {
                    name 'Column'
                    styles [CardMargin, CardPadding]
                    data {
                        crossAxisAlignment 'start'
                    }
                    children [
                        TextView {
                            name 'TextView'
                            data {
                                data `interaction.conversation`
                                fontWeight 'w500'
                                softWrap 'true'
                            }
                        }
                    ]
                }
            }
        ]
    }
}
```

### Example 2: CancelSaveButtonsWidget
```d3e
Widget {
    package 'lead.management'
    name 'CancelSaveButtonsWidget'
    category 'UserDefined'
    properties [
        {
            name 'Title'
            type String
            required true
        }
        {
            name 'IsNewObj'
            type Boolean
            required true
        }
    ]
    build Column {
        name 'Column'
        styles [CardPadding]
        data {
            crossAxisAlignment 'end'
            mainAxisAlignment 'end'
        }
        children [
            Row {
                name 'Row'
                data {
                    mainAxisAlignment 'end'
                    crossAxisAlignment 'end'
                }
                children [
                    CIf {
                        name 'CancelButtonIf'
                        condition `isNewObj`
                        then Button {
                            name 'CancelButton'
                            styles [Secondary]
                            data {
                                width '100'
                            }
                            child TextView {
                                name 'ButtonText'
                                data {
                                    data 'Cancel'
                                    color '@c1'
                                }
                            }
                        }
                        else Button {
                            name 'SaveAndCancelButton'
                            styles [Secondary]
                            data {}
                            child TextView {
                                name 'ButtonText'
                                data {
                                    data 'Save and Close'
                                    color '@c1'
                                }
                            }
                        }
                    }
                    Button {
                        name 'SaveButton'
                        styles [Primary]
                        data {
                            margin '0 0 0 10'
                            width '110'
                        }
                        child TextView {
                            name 'ButtonText2'
                            data {
                                data `title`
                                color '@c14'
                            }
                        }
                    }
                ]
            }
        ]
    }
}
```

### Example 3: BooleanRadioView
```d3e
Widget {
    name 'Boolean Radio View'
    category 'UserDefined'
    properties [
        {
            name 'Value'
            type Boolean
            required true
        }
        {
            name 'True Name'
            type String
            defaultValue `'Yes'`
            required true
        }
        {
            name 'False Name'
            type String
            defaultValue `'No'`
            required true
        }
        {
            name 'Name'
            type String
        }
        {
            name 'Errors'
            collection true
            type String
        }
        {
            name 'Is Required'
            type Boolean
            defaultValue `false`
        }
        {
            name 'Active Color'
            type Color
            stylable true
        }
        {
            name 'Inactive Color'
            type Color
            stylable true
        }
    ]
    build Column {
        name 'column'
        styles [FieldStyle]
        data {
            crossAxisAlignment 'start'
        }
        children [
            Row {
                name 'id'
                data {
                    margin '0 0 5 0'
                }
                children [
                    CIf {
                        name 'Name'
                        condition `this.name != null && this.name.isNotEmpty`
                        then TextView {
                            name 'nameview'
                            styles [LabelText]
                            data {
                                data `this.name`
                            }
                        }
                    }
                    CIf {
                        name 'id2'
                        condition `isRequired`
                        then TextView {
                            name 'id3'
                            styles [LabelText]
                            data {
                                data '*'
                                color '@c1'
                            }
                        }
                    }
                ]
            }
            Column {
                name 'row'
                children [
                    RoundedCheckbox {
                        name 'True Pressed'
                        data {
                            name `this.trueName`
                            value `this.value`
                            activeColor `activeColor != null ?activeColor : HexColor.fromHexInt(0xFFFFFFFF)`
                            margin '0 0 5 0'
                        }
                    }
                    RoundedCheckbox {
                        name 'falseCheck'
                        data {
                            name `this.falseName`
                            value `!this.value`
                            inActiveColor `inactiveColor`
                        }
                    }
                ]
            }
            CIf {
                name 'id4'
                condition `this.errors.isNotEmpty`
                then Column {
                    name 'id5'
                    data {
                        crossAxisAlignment 'start'
                    }
                    children [
                        CFor {
                            name 'item'
                            var 'item'
                            items `this.errors`
                            type String
                            item TextView {
                                name 'id6'
                                styles [ErrorText]
                                data {
                                    data `item`
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
}
```

## Structure
- Uses the `styles` field in the build tree or on widget nodes
- Styles are defined in the Style/ directory and referenced by name
- Multiple styles can be combined in a list: `styles [StyleA, StyleB]`
- Styles can be applied to any widget node (e.g., Column, Row, Button, TextView, etc.)

## When to Use
- To ensure consistent appearance and reuse of visual design across widgets.
- When you want to centralize and update visual design in one place.
- For enforcing design system standards across your UI.

## Additional Notes
- **Multiple styles** can be combined for cumulative effects.
- **Consistent use of styles** helps maintain a unified look and feel across your application.
- **Styles must be defined** in the `Style/` directory and referenced by their name in the `styles` field. 