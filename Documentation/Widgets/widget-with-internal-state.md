# Widget with Internal State

## What is a Widget with Internal State?
A **Widget with Internal State** manages its own local state using internal properties, which can be mutated within the widget. This is useful for UI elements that need to track and update their own state independently of their parent.

## Prompt Template
"Create a widget with internal state that [describe the state and its usage, e.g., toggles between ON and OFF]."

## Example Prompts
- Create a widget with a boolean property that toggles when a button is pressed.
- Build a counter widget with an internal count property.
- Make a widget that tracks whether a section is expanded or collapsed.

## D3E Example
```d3e
Widget {
    name 'ToggleSwitchWidget'
    properties [
        {
            name 'isOn'
            type Boolean
            internal true
        }
    ]
    build Row {
        children [
            TextView {
                data {
                    data `isOn ? 'ON' : 'OFF'`
                }
            }
            Switch {
                data {
                    value `isOn`
                }
            }
        ]
    }
    eventHandlers [
        {
            name 'onSwitchToggled'
            type OnEvent
            on Switch
            event onChanged
            block ```
                isOn = !isOn;
            ```
        }
    ]
}
```

## More Real-World Examples

### Example 1: ToggleView
```d3e
Widget {
    package 'lead.management'
    name 'Toggle View'
    category 'UserDefined'
    properties [
        {
            name 'Value'
            type Boolean
            required true
        }
    ]
    build Container {
        name 'id'
        data {
            alignment 'center'
        }
        child Stack {
            name 'stack'
            data {
                alignment 'centerStart'
            }
            children [
                Container {
                    name 'container2'
                    data {
                        cursor 'click'
                        width '45'
                        height '25'
                        decoration {
                            color 'ff616161'
                            borderRadius '15'
                        }
                    }
                    conditionals [
                        {
                            condition `value`
                            values {
                                decoration {
                                    color 'ff1bd51f'
                                    borderRadius '15'
                                }
                            }
                        }
                    ]
                }
                CIf {
                    name 'id'
                    condition `value`
                    then Container {
                        name 'container4'
                        data {
                            margin '2.5'
                            right '0'
                        }
                        child Container {
                            name 'round box'
                            data {
                                decoration {
                                    color '@c14'
                                    borderRadius '15'
                                }
                                height '19'
                                width '20'
                                cursor 'click'
                            }
                        }
                    }
                    else Container {
                        name 'container4'
                        data {
                            margin '2.5'
                            left '0'
                        }
                        child Container {
                            name 'round box'
                            data {
                                decoration {
                                    color '@c14'
                                    borderRadius '15'
                                }
                                height '19'
                                width '20'
                                cursor 'click'
                            }
                        }
                    }
                }
            ]
            behaviours [
                GestureDetector
            ]
        }
    }
    eventHandlers [
        {
            name 'OnChange'
            type OnBehaviour
            on stack
            behaviour GestureDetector
            event onTap
            block ```
                if(this.onChanged != null){
                    onChanged(!value);
                }
            ```
        }
    ]
    events [
        {
            name 'OnChanged'
            params [
                {
                    name 'Value'
                    type Boolean
                }
            ]
        }
    ]
    twoWayBinding true
}
```

### Example 2: BooleanRadioView
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
    eventHandlers [
        {
            name 'OnFalseSelected'
            type OnEvent
            on falseCheck
            event onChanged
            block ```
                if(this.onChanged != null) {
                    this.onChanged(false);
                }
            ```
        }
        {
            name 'OnTrueSelected'
            type OnEvent
            on truePressed
            event onChanged
            block ```
                if(this.onChanged != null) {
                    this.onChanged(true);
                }
            ```
        }
    ]
    events [
        {
            name 'OnChanged'
            params [
                {
                    name 'Value'
                    type Boolean
                }
            ]
        }
    ]
    twoWayBinding true
}
```

### Example 3: LabelWithInputField
```d3e
Widget {
    name 'LabelWithInputField'
    category 'UserDefined'
    properties [
        {
            name 'Name'
            type String
        }
        {
            name 'PlaceHolder'
            type String
        }
        {
            name 'Is Required'
            type Boolean
            defaultValue `false`
        }
        {
            name 'Value'
            type String
        }
        {
            name 'Errors'
            collection true
            type String
        }
        {
            name 'ObscureText'
            type Boolean
            defaultValue `false`
            stylable true
        }
        {
            name 'FocusNode'
            type FocusNode
            internal true
        }
        {
            name 'Active'
            type Boolean
            internal true
        }
        {
            name 'disable'
            type Boolean
            defaultValue `false`
        }
        {
            name 'Field Color'
            type Color
            stylable true
        }
        {
            name 'MaxLines'
            type Integer
            defaultValue `1`
            stylable true
        }
        {
            name 'Corner Radius'
            type Double
            defaultValue `4.0`
            stylable true
        }
        {
            name 'keyboardType'
            type TextInputType
            stylable true
        }
        {
            name 'Dense'
            type Boolean
            defaultValue `false`
            stylable true
        }
        {
            name 'InputFormatter'
            type RegExp
        }
    ]
    build Column {
        name 'id'
        styles [FieldStyle]
        children [
            CIf {
                name 'id'
                condition `this.name != null && this.name.isNotEmpty`
                then Row {
                    name 'id'
                    data {
                        margin '0 0 5 0'
                    }
                    children [
                        TextView {
                            name 'Nameview'
                            styles [LabelText]
                            data {
                                data `this.name`
                            }
                        }
                        CIf {
                            name 'id'
                            condition `isRequired`
                            then TextView {
                                styles [LabelText]
                                name 'id'
                                data {
                                    data '*'
                                    color 'FFC20F2F'
                                }
                            }
                        }
                    ]
                }
            }
            InputField {
                name 'Field'
                styles [DefaultInputField]
                data {
                    value `value`
                    focusNode `focusNode`
                    obscureText `obscureText`
                    placeHolder `this.placeHolder`
                    disable `disable`
                    maxLines `maxLines`
                    dense `dense`
                    keyboardType `keyboardType`
                    textStyle {
                        fontSize '15'
                        fontWeight 'w500'
                    }
                    cornerRadius `cornerRadius`
                }
                conditionals [
                    {
                        condition `this.disable`
                        values {
                            backgroundColor 'FFB4B4B4'
                        }
                    }
                    {
                        condition `this.fieldColor == null`
                        values {
                            backgroundColor 'FFFFFFFF'
                        }
                    }
                    {
                        condition `errors.isNotEmpty`
                        values {
                            inActiveColor 'FFC20F2F'
                        }
                    }
                ]
            }
            CIf {
                name 'id'
                condition `this.errors.isNotEmpty`
                then Column {
                    name 'id'
                    data {
                        crossAxisAlignment 'start'
                    }
                    children [
                        CFor {
                            name 'Item'
                            var 'item'
                            items `this.errors`
                            type String
                            item TextView {
                                name 'id'
                                styles [ErrorText]
                                data {
                                    data `item`
                                    margin '5 0 0'
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
    eventHandlers [
        {
            name 'OnInit'
            block ```
                focusNode = FocusNode();
                focusNode.addListener(onChangeFocus);
            ```
        }
        {
            name 'OnChangeFocus'
            block ```
                active = focusNode.hasFocus;
                if(active && onTap != null){
                    this.onTap();
                }
            ```
        }
        {
            name 'OnChangeText'
            type OnEvent
            on field
            event onChanged
            block ```
                if(onChanged != null){
                    onChanged(text);
                }
            ```
        }
        {
            name 'onTapHandker'
            type OnEvent
            on field
            event onTap
            block ```
                this.errors.clear();
                if(onTap != null){
                    onTap();
                }
            ```
        }
        {
            name 'OnSubmiitedTextHandler'
            type OnEvent
            on field
            event onSubmitted
            block ```
                if(onSubmitted != null){
                    onSubmitted(text);
                }
            ```
        }
    ]
    events [
        {
            name 'OnChanged'
            params [
                {
                    name 'Value'
                    type String
                }
            ]
        }
    ]
}
```

## Structure
- Declares properties with `internal true`
- Updates internal state in event handlers or build tree

## When to Use
- For widgets that need to track and update their own state independently. 