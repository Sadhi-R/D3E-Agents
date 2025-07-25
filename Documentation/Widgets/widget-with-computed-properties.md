# Widget with Computed Properties

## What is a Widget with Computed Properties?
A **Widget with Computed Properties** uses properties whose values are derived from other properties or expressions. Computed properties are automatically updated when their dependencies change and are useful for displaying derived or formatted data.

## Prompt Template
"Create a widget with computed properties that [describe the computation, e.g., combines first and last name into full name]."

## Example Prompts
- Create a widget that displays a user's full name as a computed property from first and last name.
- Build a widget that shows the sum of two number properties.
- Make a widget with a computed property for formatted date display.

## D3E Example
```d3e
Widget {
    name 'FullNameWidget'
    properties [
        {
            name 'firstName'
            type String
            required true
        }
        {
            name 'lastName'
            type String
            required true
        }
        {
            name 'fullName'
            type String
            computed true
            computation `firstName + ' ' + lastName`
            internal true
        }
    ]
    build TextView {
        data {
            data `fullName`
        }
    }
}
```

## More Real-World Examples

### Example 1: LeadOverviewWidget
```d3e
Widget {
    package 'lead.management'
    name 'Lead Overview Widget'
    category 'UserDefined'
    properties [
        {
            name 'Lead'
            type Lead
            required true
            synchronise true
            fetchData true
        }
        {
            name 'User'
            type User
            required true
        }
        {
            name 'Client'
            type TwilioClient
            required true
        }
        {
            name 'Data'
            type CallData
            required true
        }
    ]
    build Column {
        name 'Column'
        children [
            // ... (children omitted for brevity) ...
        ]
    }
    eventHandlers [
        {
            name 'On Init'
            block ```
                if(false){
                    Interaction i = lead.interactionHistory.first;
                    i.sid = '123';
                    i.type = InteractionType.Call;
                    i.details = 'Call Details';
                    i.toNumber = '1234567890';
                    i.fromNumber = '1234567890';
                    i.duration = Duration(minutes: 5);
                    i.recordingURL = 'http://recording.com';
                    i.startTime = DateTime.now();
                    i.endTime = DateTime.now();
                    i.handledBy = user;
                    i.callStatus = CallStatus.Completed;
                    i.notes = ['Note 1', 'Note 2'];
                } 
            ```
        }
        {
            name 'OnNewMessageButtonPressed'
            type OnEvent
            on view
            event computeNewMessage
            block ```
                Interaction interaction =  Interaction(
                    lead: lead,
                    fromNumber: user.twilioNumber,
                    toNumber: lead.phone,
                    type: InteractionType.SMS,
                    body: body,
                    isIncoming: false,
                    handledBy: user,
                    createdDate: DateTime.now()
                );
                Boolean status = RPCServices.getCallService().sendSMS(interaction).await;
                if(status) {
                    lead.interactionHistory.add(interaction);
                }

            ```
        }
    ]
}
```

### Example 2: NeedsAndPainsCardView
```d3e
Widget {
    package 'lead.management'
    name 'NeedsAndPainsCardView'
    properties [
        {
            name 'lead'
            type Lead
            required true
        }
    ]
    build Column {
        name 'Column'
        styles [BaseViewStyle]
        data {
            crossAxisAlignment 'start'
            mainAxisAlignment 'start'
        }
        children [
            TextView {
                name 'TextView'
                styles [HeadlineFour]
                data {
                    data 'Needs & Pains'
                    margin '0 0 10 0'
                }
            }
            Column {
                name 'Column'
                data {
                    expand 'true'
                    vscroll 'true'
                }
                children [
                    NeedsCardView {
                        name 'NeedsCardView'
                        data {
                            lead `lead`
                        }
                    }
                    PainsCardView {
                        name 'PainsCardView'
                        data {
                            lead `lead`
                            margin '10 0 0 0'
                        }
                    }
                ]
            }
        ]
    }
}
```

### Example 3: BooleanRadioView (with computed property for display)
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
- Declares computed properties using `computed true` and a `computation` expression
- Computed properties can be internal or external

## When to Use
- When a property should always reflect a calculation or combination of other properties. 