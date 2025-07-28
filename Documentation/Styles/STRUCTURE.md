# 🎨 D3E Style Reference Guide

## 🧭 Introduction

In **D3E Studio**, styles define reusable visual rules for widgets and UI components.
They ensure **consistency**, ease of **maintenance**, and rapid **customization** of UI appearance.

This guide covers:

* Style declaration syntax
* Style application
* Real-world examples
* Best practices
* Advanced style selectors & combinators

---

## 1. 🔧 Style Declaration: Syntax & Anatomy

Each style starts with a `Style` block:

```d3e
Style {
    name 'StyleName'
    component WidgetType
    // Optional: description 'A short description of the style'
    values {
        // style properties
    }
}
```

### 🔤 Syntax Rules

* **No commas** between items in arrays/lists.
* **No comments** inside D3E code blocks.
* **Expressions**: Use backticks: `expression`
* **Optional fields** are wrapped in \[ ].

---

## 2. 🎨 Style Properties

| Property      | Description                                                                                              |
| ------------- | -------------------------------------------------------------------------------------------------------- |
| `name`        | Unique style identifier                                                                                  |
| `component`   | Target widget type (e.g., `Button`, `InputField`)                                                        |
| `description` | (Optional) Purpose of the style                                                                          |
| `values`      | Visual properties: `backgroundColor`, `color`, `fontSize`, `fontWeight`, `borderRadius`, `padding`, etc. |

* Use theme color codes (`@c1`, `@c2`, ...) or direct hex values (`'ff000000'`).
* Font weights: `'w400'`, `'w500'`, `'w600'`, etc.

---

## 3. 🚀 Applying a Style

Apply a style using the `style` or `styles` property in a widget:

```d3e
Button {
    name 'SaveBtn'
    styles [PrimaryButton]
    child TextView {
        data {
            data 'Save'
        }
    }
}
```

---

## 4. 📦 Real-World Style Examples

### ✅ Primary Button

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

### 🟨 Secondary Button

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

### 📝 Input Field

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

---

## 5. 🌟 Best Practices

* ✅ **Consistency**: Use styles across the UI.
* 🔀 **Reusability**: Declare once, reuse often.
* 🧪 **Override**: Component props can override style values.
* 📝 **Document**: Use `description` field.
* 🚫 **Avoid comments/commas** in D3E code blocks.
* 🏷 **Naming**: Be descriptive and meaningful.
* 🎨 **Color management**: Prefer theme color codes (`@c1`, `@c2`...) over hex codes.

---

## 6. 🧱 New Style Template

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

## 7. 💬 Style Creation Prompt Template

```prompt
Create a new D3E style for a [WidgetType] with the following properties:
- Name: [StyleName]
- Description: [Short description]
- Values:
    - backgroundColor: [color code]
    - color: [color code]
    - fontSize: [number]
    - fontWeight: [weight string]
    - borderRadius: [number]
    - padding: [string]
```

---

## 8. 🤩 Supported Tags (Bootstrap-like)

You can use Bootstrap-style **semantic tags** in `tags [ ]` or as **selectors** in styles:

Examples:
`h1`, `textcenter`, `lead`, `warning`, `disabled`, `bgprimary`, `tableDark`, `roundedOutline`, `bold`, `InputField`, `DropDown`, etc.

### Tag Usage Example

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

## 9. 🔎 D3E Style Selector Specification

### ✅ Widget Selector

Selects all elements of a widget type.

```d3e
selector 'Button'
```

---

### ✅ Tag Selector

Selects widgets with a specific tag.

```d3e
selector '.error'
```

---

### ✅ Descendant Combinator (`A B`)

Matches `B` inside `A` (at any level):

```d3e
selector 'Row TextView'
```

---

### ✅ Child Combinator (`A > B`)

Matches `B` as **direct child** of `A`:

```d3e
selector 'Row > TextView'
```

---

### ✅ Adjacent Sibling Combinator (`A + B`)

Matches `B` that is **immediately after** `A`:

```d3e
selector 'Row + TextView'
```

---

### ✅ General Sibling Combinator (`A ~ B`)

Matches **all `B` siblings** that follow `A`:

```d3e
selector 'Row ~ TextView'
```

---

### ✅ Column Selector (`A || B`)

Matches elements in the **same column**:

```d3e
selector '.Name || TextView'
```

---

### ✅ Pseudo Classes

| Pseudo   | Description  |
| -------- | ------------ |
| `:hover` | Mouse over   |
| `:focus` | When focused |

---

### 🔧 Advanced Style Structure with Selectors

```d3e
Style {
    name 'InputFieldError'
    component InputField
    items [
        {
            selector '.error'
            values {
              activeColor '@c11'
              inActiveColor '@c11'
            }
        }
    ]
}
```

```d3e
Style {
    name 'TextViewInRow'
    component TextView  
    items [
        {
            selector 'Row > TextView'
            values {
              fontSize '15.0'
              color '@c6'
              fontWeight 'w600'
            }
        }
    ]
}
```

---
