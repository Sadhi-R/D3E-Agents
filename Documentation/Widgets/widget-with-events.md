# Widget with Events

## What is a Widget with Events?
A **Widget with Events** defines custom events to communicate with parent widgets or the app, or to handle user interactions. Events allow widgets to notify their parent or trigger actions externally.

## Prompt Template
"Create a widget with events that [describe the event, e.g., fires an event when a button is pressed]."

## Example Prompts
- Create a widget that fires an event when a form is submitted.
- Build a widget that emits a custom event when a value changes.
- Make a widget that notifies its parent when a button is clicked.

## D3E Example
```d3e
Widget {
    name 'SubmitButtonWidget'
    events [
        {
            name 'onSubmit'
            params [
                {
                    name 'value'
                    type String
                }
            ]
        }
    ]
    build Button {
        data {
            data 'Submit'
        }
    }
    eventHandlers [
        {
            name 'onPressedHandler'
            type OnEvent
            on Button
            event onPressed
            block ```
                fireEvent('onSubmit', value: 'Submitted!');
            ```
        }
    ]
}
```

## Structure
- Declares events in the `events` block
- Uses event handlers for user actions

## When to Use
- When the widget needs to notify its parent or trigger actions externally. 

## More Real-World Examples

### Example 1: CancelSaveButtonsWidget
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

### Example 2: BooleanRadioView (with event)
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

### Example 3: LabelField (with event)
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