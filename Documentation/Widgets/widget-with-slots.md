# Widget with Slots

## What is a Widget with Slots?
A **Widget with Slots** allows custom content or widgets to be injected at specific places in its build tree, enabling flexible composition. Slots are used for advanced widget composition and allow parent widgets to provide custom children.

## Prompt Template
"Create a widget with slots that [describe the slot usage, e.g., allows custom buttons to be injected]."

## Example Prompts
- Create a dialog widget with slots for content and action buttons.
- Build a card widget that accepts a custom header and footer via slots.
- Make a layout widget with a slot for main content.

## D3E Example
```d3e
Widget {
    name 'DialogWidget'
    build PopupWrapperView {
        slots [
            {
                slot content
                child Column {
                    // ...
                }
            }
            {
                slot buttons
                children [
                    Button { ... }
                ]
            }
        ]
    }
}
```

## Structure
- Declares `slots` in the build block
- Uses `slot` keyword to define named slots

## When to Use
- When you want to allow parent widgets to inject custom content or controls. 

## More Real-World Examples

### Example 1: PopupWrapperView
```d3e
Widget {
    name 'PopupWrapperView'
    properties [
        {
            name 'Title'
            type String
        }
    ]
    build Column {
        name 'id'
        styles [DefaultPopUp]
        data {
            mainAxisSize 'min'
            crossAxisAlignment 'center'
            constraints {
                maxHeight '500'
            }
        }
        children [
            CIf {
                name 'headerText'
                condition `this.title != null && this.title.isNotEmpty`
                then Row {
                    name 'id'
                    data {
                        mainAxisAlignment 'start'
                        padding '12 0 0 12'
                    }
                    children [
                        TextView {
                            styles [HeadlineFour]
                            name 'title12'
                            data {
                                data `title`
                            }
                        }
                    ]
                }
            }
            HorizontalLine {
                name 'id2323'
                data {
                    visibility `this.title != null && this.title.isNotEmpty`
                    margin '10 0'
                }
            }
            CIf {
                name 'Id3'
                condition `contentPresent`
                then Container {
                    name 'Id4'
                    data {
                        decoration {
                            color '@14'
                        }
                        padding '0 12'
                        vscroll 'true'
                    }
                    child CSlot {
                        name 'content'
                    }
                }
            }
            CIf {
                name 'idd'
                condition `buttonsCount > 0`
                then HorizontalLine {
                    name 'id2323'
                    data {
                        margin '10 0'
                    }
                }
                else Container {
                    name 'container'
                    data {
                        height '20'
                    }
                }
            }
            CIf {
                name 'Id6'
                condition `buttonsCount > 0`
                then Row {
                    name 'id'
                    data {
                        mainAxisAlignment 'start'
                        padding '0 0 12 12'
                    }
                    children [
                        Wrap {
                            name 'id7'
                            data {
                                alignment 'start'
                                spacing '10'
                                crossAxisAlignment 'center'
                            }
                            children [
                                CFor {
                                    name 'Item'
                                    var 'index'
                                    items `Range.to(buttonsCount)`
                                    type Integer
                                    item CSlot {
                                        name 'Buttons'
                                        index `index`
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    slots [
        {
            name 'Content'
        }
        {
            name 'Buttons'
            collection true
        }
    ]
}
```

### Example 2: AddUserView (with slots for buttons)
```d3e
Widget {
    package 'lead.management'
    name 'AddUserView'
    category 'UserDefined'
    properties [
        {
            name 'User'
            type User
            required true
        }
        {
            name 'Errors'
            collection true
            type String
            internal true
        }
        {
            name 'isAdmin'
            type Boolean
            required true
        }
    ]
    build Column {
        children [
            // ... form fields ...
        ]
        slots [
            {
                slot buttons
                children [
                    Button {
                        name 'CancelButton'
                        styles [Secondary]
                        child TextView {
                            name 'ButtonText2'
                            data {
                                data 'Cancel'
                            }
                        }
                    }
                    Button {
                        name 'UserButton'
                        styles [Primary]
                        child TextView {
                            name 'ButtonText'
                            data {
                                data 'Add New User'
                            }
                        }
                    }
                ]
            }
        ]
    }
    // ... eventHandlers and editorFor ...
}
```

### Example 3: DialogWidget (from template)
```d3e
Widget {
    name 'DialogWidget'
    build PopupWrapperView {
        slots [
            {
                slot content
                child Column {
                    // ...
                }
            }
            {
                slot buttons
                children [
                    Button { ... }
                ]
            }
        ]
    }
}
``` 