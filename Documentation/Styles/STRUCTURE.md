# D3E Style Structure

## Introduction

In D3E Studio, **styles** define the reusable visual rules for widgets and UI elements.  
Styles promote consistency, simplify maintenance, and allow you to quickly update the look of your application.  
This guide explains the D3E style syntax, best practices, and provides real-world examples based on actual styles in this project.

---

## 1. Style Declaration: Syntax & Anatomy

Every style is declared using a `Style` block:

```d3e
Style {
    name 'StyleName'
    component WidgetType
    // Optional: description 'A short description of the style'
    values {
        // ... style properties ...
    }
}
```

**Syntax Rules:**
- **NO COMMAS** between items in arrays/lists.
- **No comments** inside D3E code blocks.
- **Expressions**: Wrap in backticks: `expression`
- **Optional Fields**: Properties in brackets [ ] are optional.

---

## 2. Style Properties

- **name:** Unique identifier for the style.
- **component:** The widget type this style targets (e.g., Button, TextView, InputField).
- **description:** (Optional) Explains the style’s purpose.
- **values:** Key-value pairs for visual properties (color, font, spacing, etc.).
    - **backgroundColor, color, fontSize, fontWeight, borderRadius, padding, margin, border, etc.**
    - Values can reference theme color codes (e.g., `@c1`), numbers, or strings.

---

## 3. How to Create and Apply a Style

1. **Create a new style** using the `Style` block.
2. **Provide a name** and (optionally) a description.
3. **Specify the component** (widget type).
4. **Define the values** for the style.
5. **Apply the style** to widgets via the `style` or `styles` property in the widget's build tree.

### Example: Applying a Style

```d3e
Button {
    name 'SaveBtn'
    style PrimaryButton
    child TextView {
        data {
            data 'Save'
        }
    }
}
```

---

## 4. Real-World Examples: Existing Styles

### Primary Button Style

```d3e
Style {
    name 'PrimaryButton'
    component Button
    description 'Primary style for main action buttons.'
    values {
        backgroundColor '@c1'
        color '@c5'
        fontSize 16.0
        fontWeight 'w600'
        borderRadius 8.0
        padding '12 24'
    }
}
```

### Secondary Button Style

```d3e
Style {
    name 'SecondaryButton'
    component Button
    description 'Secondary style for less prominent actions.'
    values {
        backgroundColor '@c4'
        color '@c1'
        fontSize 16.0
        fontWeight 'w500'
        borderRadius 8.0
        padding '12 24'
    }
}
```

### Input Field Default Style

```d3e
Style {
    name 'InputFieldDefault'
    component InputField
    description 'Default style for input fields.'
    values {
        backgroundColor '@c5'
        color '@c4'
        fontSize 14.0
        borderRadius 4.0
        padding '8 12'
    }
}
```

### TextView Body Style

```d3e
Style {
    name 'BodyText'
    component TextView
    description 'Default body text style.'
    values {
        color '@c4'
        fontSize 14.0
        fontWeight 'w400'
    }
}
```

---

## 5. Best Practices

- **Consistency:** Use styles to ensure a unified look across widgets.
- **Reusability:** Define styles once and apply them throughout the project.
- **Override:** Widget-level properties can override style defaults for special cases.
- **Documentation:** Use the `description` field for clarity and collaboration.
- **No comments or commas** in D3E code blocks.
- **Naming:** Use clear, descriptive names for styles.
- **Color Management:** Reference theme color codes for maintainability.

---

## 6. Template: New Style

```d3e
Style {
    name '[StyleName]'
    component [WidgetType]
    description '[Short description of the style]'
    values {
        backgroundColor '@c1'
        color '@c5'
        fontSize 16.0
        fontWeight 'w600'
        borderRadius 8.0
        padding '12 24'
    }
}
```

---

## 7. Prompt for Creating a New Style

When creating a new style, use a prompt that follows the model-with-child-properties structure. This ensures clarity and completeness.

### Example Prompt Structure

```prompt
Create a new D3E style for a [WidgetType] with the following properties:
- Name: [StyleName]
- Description: [Short description]
- Values:
    - backgroundColor: [color code or value]
    - color: [color code or value]
    - fontSize: [number]
    - fontWeight: [weight string]
    - borderRadius: [number]
    - padding: [string]
```

---

## 8. Example Prompts

### Example 1: Primary Button

```prompt
Create a new D3E style for a Button with the following properties:
- Name: PrimaryButton
- Description: Primary style for main action buttons.
- Values:
    - backgroundColor: @c1
    - color: @c5
    - fontSize: 16.0
    - fontWeight: w600
    - borderRadius: 8.0
    - padding: 12 24
```

### Example 2: Input Field

```prompt
Create a new D3E style for an InputField with the following properties:
- Name: InputFieldDefault
- Description: Default style for input fields.
- Values:
    - backgroundColor: @c5
    - color: @c4
    - fontSize: 14.0
    - borderRadius: 4.0
    - padding: 8 12
```

---

## Supported Tags (Bootstrap Style)

Styles in D3E can be applied using a wide range of tags for styling and semantics, similar to Bootstrap. These tags can be used in the build tree of widgets and pages to apply consistent visual rules. Example tags include:

h1, h2, h3, h4, h5, h6, headingOne, headingTwo, headingThree, headingFour, headingFive, headingSix, dh1, dh2, dh3, dh4, lead, small, delete, strike, insert, underline, strong, em, textleft, textcenter, textright, textjustify, abbr, blockquote, muted, primary, success, info, warning, danger, Column, profile, Row, ListView, CollapsibleSideMenu, TextView, IconView, Button, rounded, roundedOutline, default, primary, success, info, warning, danger, primaryOutline, successOutline, infoOutline, warningOutline, dangerOutline, large, link, small, xsmall, block, nav, SideMenuButton, Checkbox, IconView, disabled, focus, IconCheckbox, Container, TextCheckbox, CardCheckbox, Toggle, outer, body, IconToggle, StatusToggle, roundedBox, CheckboxWithText, TextWithCheckbox, ToggleBase, Table, TableRow, TableCell, tableDark, darkRow, lightRow, tableHover, tableSmall, bordered, roundedborders, bold, headerborder, headercaption, tableActive, tableDefault, tablePrimary, tableSecondary, tableSuccess, tableDanger, tableWarning, tableInfo, tableDark, tableLight, tableStriped, InputField, large, disable, searchablePopup, resultPopup, DropDown, DropDownPopup, DurationField, SearchFilter, PasswordField, bg, CalenderView, datePopup, timePickerPopup, MonthOrYearCell, DateCell, DateField, active, DateTimeField, DateAndTimeCalendar, IconButton, small, large, Column, SatisfactionSurveyGrid, bgprimary, bgsuccess, bginfo, bgwarning, bgdanger, borderColor, MouseHoverView, mousePointer, PopupWrapperView, SearchableDropdown, SearchResultView, PopupHeader, AttachmentDownloadView, Badge, ProfileWithStatus, ProfileWithEditIcon, indicator, CarouselDot, ImageView, Container

**Example:**

```d3e
TextView {
    name 'Message'
    tags [
        'h1'
        'error'
    ]
    data {
        data 'Message'
    }
}
```

---

## Color and Style Usage Rules

- When specifying colors in styles, widgets, or pages, always use existing color codes defined in the current theme (e.g., @c1, @c2, ...). If you need a color not present in the theme, use a direct hex code (e.g., 'ff000000').
- For styles, always use an existing style if it matches the requirement. If no suitable style exists, specify the style properties directly within the component.

---

