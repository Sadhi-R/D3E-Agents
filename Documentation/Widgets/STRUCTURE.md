# D3E Widget Structure

## Introduction

In D3E Studio, **widgets** are the core building blocks of the user interface. Widgets define the structure, appearance, and behavior of UI components, from simple buttons to complex, data-driven views. Widgets are reusable, composable, and encapsulate both presentation and logic. This document is the single source of truth for designing and generating widgets in this project—intended for both developers and AI agents.

-   UI element that can be used as part of a Page
    -   Reusable component with specific functionality
    -   Can be composed to create complex interfaces
    -   Often connected to specific data models
    -   There are some widgets that are already defined in D3E. We can use them directly. (Like all basic input widgets, button, label, etc.)
    -   We normally prefer to create one widget for create/update/view. Until there will be a specific reason to create different widgets.
    -   D3E provides wide range of widgets for buttons, inputs, lists, tables, etc. So, we can use them directly. No need to create a new widget for that.

---
# Core Components

Properties listed in brackets () for each component indicate all available properties. Properties marked with (Required) must be provided when using the component, while others are optional.

## Buttons
- TextButton (lable (Required), disable)
- IconButton (icon (Required), disable)
- LoadingButton (label, loading, disable)
- TextIconButton (icon (Required), text (Required), iconRight, disable)
- SideMenuButton (title (Required), selectedMenu (Required), icon)

## Input Fields
- BarRatingField (value (Required), localValue)
- BasicDropdown (value, items (Required), placeHolder, errors, disable, popUpWidth)
- DateField (value (Required), placeHolder, format, disable)
- PasswordField (value (Required), placeHolder, errors, visiblePassword)
- SearchableInputField (value (Required), items (Required), popUpWidth)

## Date & Time
- DateTimeCalender (value (Required), format)
- DateTimeField (value (Required), placeHolder, format, disable)
- DateTimeView (value (Required), format)
- DateView (value (Required), format)
- TimeField (value (Required), placeHolder, format)
- TimePicker (value (Required), militryTime)
- TimePickerWithInputfield (value (Required), militryTime)
- TimeView (value (Required), format)

## Toggle & Selection
- CardCheckbox (value, label)
- IconCheckbox (value, icon)
- IconToggle (icon, value)
- LabledToggle (label, value)
- StatusToggle (value)
- SwitchToggle (value)
- TextCheckbox (value, text)
- Toggle (value)
- ToggleBase (value)

## Layout & Display
- BasicSideBarView
- Divider
- DoubleView (value)
- IntegerView (value)
- LabelField (label)
- LabelWithDescriptionField (label, description)
- ProgressBar (value, total)
- RatingView (value)
- SearchResultView (items)

## Search & Filter
- SearchComponent (value, onSearch)
- SearchFilter (filters)
- SearchableDropdown (value, items)

## Special Components
- QuantityCounter (value)
- Slider (value, min, max)
- ToolTipWrapper (tooltip)
- VoiceBasedSearch

## Calendar Components
- CalenderView (value (Required))
- DateCell (date (Required), isSelected)
- MonthOrYearCell (value (Required), isSelected)


---

## 1. Widget Rules and Best Practices

- **Every widget must have a build tree**: The `build` block defines the UI for the widget.
- **Widgets are reusable**: They can be used in other widgets or pages.
- **All widgets and pages extend BaseComponent**: Properties from BaseComponent are accessible in any widget.
- **Widget = Component = Form = View**: These terms are used interchangeably; all are UI elements.
- **Split large widgets**: For maintainability, break large build trees into smaller, reusable widgets.
- **Do not declare properties of type Widget or Page**: Use `slots` to accept widgets for composition instead.
- **Properties are of two types**:
  - **External**: Passed in from parent, not marked as `internal true`, cannot be mutated inside the widget.
  - **Internal**: Marked as `internal true`, can be mutated inside the widget, required for two-way binding.
- **To change a property value from within the widget, it must be internal**.
- **All properties referenced in the build tree must be declared in the widget**.
- **No commas in arrays/lists**: D3E does not support commas between items in collections.
- **No comments in D3E code**: Use markdown comments in documentation only.
- **Two-way binding**:
  - Supported by setting `twoWayBinding true` on the widget usage.
  - Allows parent/child widgets to sync property values.
- **Event handlers**:
  - Each event handler maps to one event on one widget node.
  - The `OnInit` event handler is special and runs once on widget render.
  - Arguments to event handlers must match the event's parameter names.
- **Styles**:
  - Define visual characteristics for widgets.
  - Styles are reusable and referenced in the build tree.
- **Widget composition**:
  - Use slots to inject custom widgets or content.
  - Do not use properties of type Widget/Page for composition.
- **Pages are widgets**: Pages are created like widgets but cannot be used inside other widgets or pages, and do not have events.
- **Editor widgets**: If a widget is specified as an editor for a model, it can leverage model validation methods.
- **Node identity in the build tree must not match any property identity in the same widget.**
- **All non-binded properties inside `data` must be strings and parsable to their real type.**

---

## 2. Widget Declaration: Syntax & Anatomy

Every widget starts with a declaration block:

```d3e
Widget {
    // Optional: package 'your.package'
    name 'WidgetName'
    // Optional: category 'UserDefined' | 'System' | ...
    // Optional: description 'A short description of the widget'
    properties [
        // ... property blocks ...
    ]
    build <WidgetTree> { ... }
    // Optional: slots [ ... ]
    // Optional: eventHandlers [ ... ]
    // Optional: events [ ... ]
}
```

**Syntax Rules:**
- **NO COMMAS** between items in arrays/lists.
- **Expressions**: Wrap in backticks: `expression`
- **Code Blocks**: Wrap in triple backticks: `code`
- **Optional Fields**: Properties in brackets [ ] are optional

---

## 3. Widget Properties: Internal vs External

### External Properties
- Used for data passed into the widget from outside (parent widget, page, etc.).
- Declared **without** `internal true`.
- Cannot be mutated from within the widget.
- Used for input, configuration, or data display.
- For model types (e.g., `User`, `Product`), must specify the model name as the `type`:
  ```d3e
  {
      name 'User'
      type User
      required true
  }
  ```
  This ensures full access to all model fields (e.g., `user.firstName`, `user.email`).

### Internal Properties
- Used for widget-local state, computed values, or any property that is mutated within the widget.
- Declared **with** `internal true`.
- Can be changed by the widget (e.g., timers, UI state, form values, etc.).
- Required for two-way binding.

### Computed Properties
- Use `computed true` and a `computation` expression.
- Can be internal or external, but are often internal for derived state.

### Property Declaration Example
```d3e
properties [
    {
        name 'email'
        type String
        required true
    }
    {
        name 'password'
        type String
        required true
    }
    {
        name 'isLoggingIn'
        type Boolean
        internal true
    }
]

> **Note:** Do not use both `required true` and `internal true` on the same property. Use `required true` for user-input fields, and `internal true` for internal state only.
```

---

## 4. Property Binding in the Build Tree

- **Properties are referenced in the build tree using their identity** (the camelCase version of the property name).
- **External properties** are used for display, configuration, or as input to child widgets.
- **Internal properties** are used for local state, UI logic, or as part of computed expressions.
- **All properties referenced in the build tree must be declared in the widget.**
- **Node identity in the build tree must not match any property identity.**

### Example: Referencing Properties in Build
```d3e
build Column {
    children [
        TextView {
            data {
                data `user.firstName`
            }
        }
        CIf {
            condition `isLoading`
            then Loader { }
        }
        TextView {
            data {
                data `status.name`
            }
        }
    ]
}
```

---

## 5. Two-way Binding

- D3E supports two-way binding for properties, especially in form fields.
- Two-way binding is enabled on the widget usage (e.g., `twoWayBinding true`), not on the property itself.
- This allows the child widget to update the parent's property value.

### Example: Two-way Binding
```d3e
properties [
    {
        name 'firstName'
        type String
        internal true
    }
]
build LabelWithInputField {
    data {
        value `firstName`
        placeHolder 'enter firstname'
        label 'First Name'
    }
    twoWayBinding true
}
```

---

## 6. Slots and Widget Composition

- **Do not declare properties of type Widget or Page.**
- Use `slots` to accept widgets as children for composition.
- Slots allow you to inject custom content or widgets into specific places in your widget's build tree.

### Example: Using Slots
```d3e
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
```

---

## 7. Build Tree: UI Structure

The `build` block defines the widget's UI using a tree of components. This is where you compose the visual and interactive structure of your widget.

```d3e
build <WidgetType> {
    name 'NodeName'
    // Optional: styles [ ... ]
    // Optional: data { ... }
    // Optional: children [ ... ]
    // Optional: conditionals [ ... ]
    // Optional: key `expression`
    // Optional: child <WidgetType> { ... }
}
```

- **WidgetType**: Row, Column, TextView, Button, Container, or any custom widget etc.
- **children**: List of child widgets/components.
- **data**: Key-value pairs for widget properties (e.g., text, color, padding).
- **styles**: List of style references.
- **conditionals**: Conditional rendering or property overrides.
- **key**: Unique key for widget instance.

---

## 8. Event Handlers

Widgets can define event handlers for user interactions or lifecycle events:

```d3e
eventHandlers [
    {
        name 'HandlerName'
        type OnEvent // Optional, e.g., OnEvent
        on <WidgetNodeName>
        event <EventName>
        block ```
            // D3E code to execute
        ```
    }
    // ... more handlers ...
]
```

- **on**: The widget node this handler is attached to.
- **event**: The event to listen for (e.g., onPressed, onChanged).
- **block**: D3E code to execute when the event occurs.
- **OnInit** is a special event handler called once on widget render.

---

## 9. Events

Widgets can define custom events to communicate with parent widgets or the app:

```d3e
events [
    {
        name 'EventName'
        params [
            {
                name 'ParamName'
                type DataType
            }
            // ... more params ...
        ]
    }
    // ... more events ...
]
```

---

## 10. Widget Composition & Special Features

- **Composition**: Widgets can include other widgets as children, enabling reuse and modularity.
- **Conditional Rendering**: Use `CIf` blocks for conditional UI.
- **Internal State**: Use `internal true` for widget-local state.
- **Custom Styles**: Reference styles from the Style/ directory.
- **System Widgets**: Built-in widgets like Row, Column, TextView, Button, Container, etc.
- **Composed Widgets**: User-defined widgets that include other widgets as children.
- **Editor Widgets**: If a widget is specified as an editor for a model, it gets validation methods for model properties.

---

## 11. Best Practices

- **Keep widgets focused**: Each widget should have a clear responsibility.
- **Reuse widgets**: Compose complex UIs from smaller, reusable widgets.
- **Use properties for configuration**: Expose only what is necessary.
- **Use proper property types**:
  - For external model objects (e.g., `User`, `Product`), must specify the model name as the type
  - For primitive types (`String`, `Boolean`, `int`, `double`), use the type directly
  - For internal properties (with `internal true`), any type is allowed
- **Leverage event handlers**: For user interaction and communication.
- **Document your widgets**: Use the `description` field for clarity.
- **Follow naming conventions**: Use clear, descriptive names for widgets and properties.
- **Do not use defaultValue for type defaults** (e.g., `defaultValue ''` for String, `defaultValue 0` for Integer).
- **Node identity in the build tree must not match any property identity.**
- **All non-binded properties inside `data` must be strings and parsable to their real type.**

---

## 12. Example: Comprehensive Widget

**Scenario:**  
This widget displays and edits a user's profile. It accepts a `User` model as an external property, manages local form state with internal properties, uses two-way binding for form fields, and exposes slots for custom buttons. It also demonstrates event handling and property binding in the build tree.

```d3e
Widget {
    package 'lead.management'
    name 'UserProfileFormWidget'
    category 'UserDefined'
    description 'A form for viewing and editing user profile information.'
    properties [
        {
            name 'user'
            type User
            required true
        }
        {
            name 'firstName'
            type String
            internal true
        }
        {
            name 'lastName'
            type String
            internal true
        }
        {
            name 'email'
            type String
            internal true
        }
        {
            name 'isSaving'
            type Boolean
            internal true
        }
        {
            name 'fullName'
            type String
            computed true
            computation `firstName + ' ' + lastName`
            internal true
        }
    ]
    build Column {
        data {
            padding '20'
        }
        children [
            TextView {
                data {
                    data 'Edit Profile'
                    fontSize '20'
                    fontWeight 'w600'
                }
            }
            LabelWithInputField {
                data {
                    name 'First Name'
                    value `firstName`
                    placeHolder 'Enter first name'
                }
                twoWayBinding true
            }
            LabelWithInputField {
                data {
                    name 'Last Name'
                    value `lastName`
                    placeHolder 'Enter last name'
                }
                twoWayBinding true
            }
            LabelWithInputField {
                data {
                    name 'Email'
                    value `email`
                    placeHolder 'Enter email address'
                }
                twoWayBinding true
            }
            TextView {
                data {
                    data `fullName.isEmpty ? '' : 'Full Name: ' + fullName`
                    color '@c8'
                    fontSize '14'
                    margin '10 0 0 0'
                }
            }
            CIf {
                condition `isSaving`
                then Loader {
                    data {
                        size '24'
                    }
                }
            }
        ]
        slots [
            {
                slot buttons
                children [
                    Button {
                        name 'SaveButton'
                        styles [Primary]
                        data {
                            tooltip 'Save'
                        }
                        child TextView {
                            data {
                                data 'Save'
                            }
                        }
                    }
                    Button {
                        name 'CancelButton'
                        styles [Secondary]
                        data {
                            tooltip 'Cancel'
                        }
                        child TextView {
                            data {
                                data 'Cancel'
                            }
                        }
                    }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'onInit'
            block ```
                firstName = user.firstName;
                lastName = user.lastName;
                email = user.email;
                isSaving = false;
            ```
        }
        {
            name 'onSaveButtonPressed'
            type OnEvent
            on SaveButton
            event onPressed
            block ```
                isSaving = true;
                user.firstName = firstName;
                user.lastName = lastName;
                user.email = email;
                Result<User> result = user.save().await;
                isSaving = false;
                if(result.status == Success) {
                    EventBus.get().fire(SuccessMessage(message : 'Profile updated successfully'));
                } else {
                    EventBus.get().fire(FailureMessage(message : result.errors.join(', ')));
                }
            ```
        }
        {
            name 'onCancelButtonPressed'
            type OnEvent
            on CancelButton
            event onPressed
            block ```
                firstName = user.firstName;
                lastName = user.lastName;
                email = user.email;
            ```
        }
    ]
}
```

---

## 13. Template for New Widgets

```d3e
Widget {
    name '[WidgetName]'
    // Optional: package 'your.package'
    // Optional: category 'UserDefined' | 'System' | ...
    // Optional: description 'A short description of the widget'
    properties [
        {
            name 'externalProperty'
            type String
            required true
        }
        {
            name 'internalState'
            type Boolean
            internal true
        }
        {
            name 'computedValue'
            type String
            computed true
            computation `someExpression`
            internal true
        }
    ]
    build Column {
        children [
            TextView {
                data {
                    data `externalProperty`
                }
            }
            CIf {
                condition `internalState`
                then Loader { }
            }
            TextView {
                data {
                    data `computedValue`
                }
            }
        ]
        slots [
            {
                slot buttons
                children [
                    Button { ... }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'onInit'
            block ```
                // Initialization logic
            ```
        }
        {
            name 'onButtonPressed'
            type OnEvent
            on Button
            event onPressed
            block ```
                // Button press logic
            ```
        }
    ]
    events [
        {
            name 'onCustomEvent'
            params [
                {
                    name 'param'
                    type String
                }
            ]
        }
    ]
}
```

---
- Represents a unit of user interface.
- Can have properties, children, events, event handlers etc.
- Properties can be computed, or they can have default Value.
- DefaultValue or computation is a expression type. they follow the sytax of d3e-code.
- There is build for every widget that represent UI.
(Widget CollapseView) {
    name 'Collapse View'
    properties [
        {
            name 'Collapse'
            type Boolean
            internal true
            defaultValue `true`
        }
        {
            name 'Title'
            type String
        }
    ]
    build Column {
        name 'Column'
        children [
            Row {
                name 'Row'
                children [
                    TextView {
                        name 'TextView'
                        data {
                            data `title`
                        }
                    }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'onTapRowBehaviourHandler'
            type OnBehaviour
            on row
            behaviour GestureDetector
            event onTap
            block '''
                this.collapse = !collapse;
            '''
        }
    ]
}
- These widgets are reusable items, they can be used in another widget or page.
- They must pass the required external property values and must handle required events.
- Optionally they can pass values for optional external properties as well.
- Eveyr widget and page internally extends BaseComponent. So, all properties in the BaseComponent can be accessed in any widget. Can pass values for the BaseComponent properties while using any widget.
Example of BaseComponent property use
Button {
    name 'LoginButton'
    child TextView {
        name 'LoginButtonText'
        data {
            data 'Login'
        }
    }
}
- Here 'width' property is not defined in the Button, But we can use it as it was there in BaseComponent.
- Width is pecified always in terms of percentage only. So, no need to metion '100%' just mention '100'. Since width takes only number and that will be treated as percentage.
- Some time we call widget as Component, Form, View etc. But basically it is a UI element.
- Best practice of design pattern is, Try to split a widget into multiple reusable widgets. So that, a developer can handle them better.
- Keeping a huge build tree in a single widget is not good to handle. Better to split them in to parts.
Example:
 InvoicePage will have InvoiceDetailsView, InvoiceLineItemView, Customer Address View etc.
 Some time, we can create a widget for any name and input field together, so that e can directly use that widget everytime instead useig two widgets.

## 14. Widget & Page Relationship

- **Widgets** are reusable UI components and can be composed inside pages or other widgets.
- **Pages** are the main navigation targets and cannot be used as children in other widgets or pages.
- Both widgets and pages extend `BaseComponent` and can use its properties (e.g., width, style).
- **Properties**: By default, all are external unless marked `internal true`. Only internal properties can be mutated in event handlers.
- **No property of type Widget or Page**: Use `slots` for widget composition.
- **Build tree**: All nodes must have unique identities not matching any property.

---

## Color and Style Usage Rules

- When specifying colors in widgets or pages, always use existing color codes defined in the current theme (e.g., @c1, @c2, ...). If you need a color not present in the theme, use a direct hex code (e.g., 'ff000000').
- For styles, always use an existing style if it matches the requirement. If no suitable style exists, specify the style properties directly within the component.

## General Widget Properties

All widgets can use the following general properties:
- `height`
- `width`
- `padding`
- `margin`
- `backgroundColor`
- `color`
- ...and other standard properties as seen in existing widget examples.

Refer to the project's existing widgets for best practices and property usage.

---


