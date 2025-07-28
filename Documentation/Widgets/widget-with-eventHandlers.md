# Widget with Event Handlers

## What is a Widget with Event Handlers?
A **Widget with Event Handlers** responds to user actions or lifecycle events by executing code blocks. Event handlers are used to update state, trigger actions, or communicate with other widgets.

## Prompt Template
"Create a widget with event handlers that [describe the event and action, e.g., increments a counter when a button is pressed]."

## Example Prompts
- Create a widget that increases a count when a button is clicked.
- Build a widget that resets a value on initialization.
- Make a widget that toggles a boolean property on a switch event.

## D3E Example
```d3e
Widget {
    name 'ClickCounterWidget'
    properties [
        {
            name 'count'
            type Integer
            internal true
        }
    ]
    build Button {
        data {
            data `count.toString()`
        }
    }
    eventHandlers [
        {
            name 'onButtonPressed'
            type OnEvent
            on Button
            event onPressed
            block ```
                count = count + 1;
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
    eventHandlers [
        {
            name 'onCancelHandler'
            type OnEvent
            on cancelButton
            event onPressed
            block ```
                if(onCancel != null) {
                    onCancel();
                }
            ```
        }
        {
            name 'onSaveHandler'
            type OnEvent
            on saveButton
            event onPressed
            block ```
                if(onSave != null) {
                    onSave();
                }
            ```
        }   
        {
            name 'onSaveAndCancelHandler'
            type OnEvent
            on saveAndCancelButton
            event onPressed
            block ```
                if(onSaveAndCancel != null) {
                    onSaveAndCancel();
                }
            ```
        }
    ]
    events [
        {
            name 'onCancel'
        }
        {
            name 'onSave'
        }
        {
            name 'onSaveAndCancel'
        }
    ]
}
```

### Example 3: LabelField
```d3e
Widget {
    name 'LabelField'
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
- Declares `eventHandlers` block
- Each handler specifies the widget node, event, and code to run

## When to Use
- When the widget needs to react to user input or lifecycle events. 