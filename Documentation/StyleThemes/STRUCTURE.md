# D3E Theme Structure

## Introduction

In D3E Studio, **themes** define the global look and feel of your application.  
A theme specifies the color palette, typography, and default colors for widgets, ensuring visual consistency and easy customization across your project.  
Themes work in tandem with styles, which define reusable visual rules for specific widgets or UI elements.

---

## 1. Theme Declaration: Syntax & Anatomy

Declare a theme using the `StyleTheme` block:

```d3e
StyleTheme {
    name 'ThemeName'
    // Optional: description 'A short description of the theme'
    color 'FFFFFFFF' // Default background color
    font 'Nunito Sans' // Default font family
    fontSize 14.0 // Default font size
    colors [
        {
            color '@c1'
            hexCode 'FFC20F2F'
            description 'Primary color'
        }
        {
            color '@c2'
            hexCode 'FF00B894'
            description 'Accent color'
        }
        {
            color '@c3'
            hexCode 'FF1976D2'
            description 'Info Blue'
        }
        {
            color '@c4'
            hexCode 'FF757575'
            description 'Neutral Gray'
        }
        {
            color '@c5'
            hexCode 'FFFFFFFF'
            description 'White'
        }
        {
            color '@c6'
            hexCode 'FF000000'
            description 'Black'
        }
    ]
    textColor '@c6' // Default text color
    tooltipBackgroundColor '@c2' // Default tooltip background color
    tooltipTextColor '@c5' // Default tooltip text color
}
```

**Syntax Rules:**
- **NO COMMAS** between items in arrays/lists.
- **No comments** inside D3E code blocks.
- **Expressions**: Wrap in backticks: `expression`
- **Optional Fields**: Properties in brackets [ ] are optional.

---

## 2. Theme Properties & Features

- **name:** Unique identifier for the theme.
- **description:** (Optional) Explains the theme’s purpose or style.
- **color:** Default background color (hex string, e.g., 'FFFFFFFF').
- **font:** Default font family for the app.
- **fontSize:** Default font size for text.
- **colors:** Custom color palette, referenced throughout the project (e.g., '@c1').
- **textColor:** Default text color.
- **tooltipBackgroundColor:** Default background for tooltips.
- **tooltipTextColor:** Default text color for tooltips.

---

## 3. Theme Colors: Management & Usage

- **Define colors** with a unique code (e.g., '@c1'), hex value, and description.
- **Reference colors** in styles, widgets, and pages using their code (e.g., `color '@c1'`).
- **Document** each color’s purpose for clarity.
- **Remove unused colors** to keep the palette clean.

### Example: Defining Theme Colors

```d3e
StyleTheme {
    name 'EdgeTheme'
    color 'FFFFFFFF'
    font 'Nunito Sans'
    fontSize 14.0
    colors [
        {
            color '@c1'
            hexCode 'FFC20F2F'
            description 'Primary color'
        }
        {
            color '@c2'
            hexCode 'FF00B894'
            description 'Accent color'
        }
        {
            color '@c3'
            hexCode 'FF1976D2'
            description 'Info Blue'
        }
        {
            color '@c4'
            hexCode 'FF757575'
            description 'Neutral Gray'
        }
        {
            color '@c5'
            hexCode 'FFFFFFFF'
            description 'White'
        }
        {
            color '@c6'
            hexCode 'FF000000'
            description 'Black'
        }
    ]
    textColor '@c6'
    tooltipBackgroundColor '@c2'
    tooltipTextColor '@c5'
}
```

---

## 4. Best Practices

- **Consistency:** Use themes and styles to ensure a unified look across the app.
- **Reusability:** Define colors once and reference them throughout the project.
- **Documentation:** Use the `description` field for clarity and collaboration.
- **No comments or commas** in D3E code blocks.
- **Naming:** Use clear, descriptive names for themes and colors.
- **Color Management:** Regularly review and clean up unused colors.

---

## 5. Template: New Theme

```d3e
StyleTheme {
    name '[ThemeName]'
    description '[Short description of the theme]'
    color '[DefaultBackgroundColor]'
    font '[FontFamily]'
    fontSize [FontSize]
    colors [
        {
            color '@c1'
            hexCode '[HexCode]'
            description '[Primary color]'
        }
        // ... more colors ...
    ]
    textColor '@c1'
    tooltipBackgroundColor '@c2'
    tooltipTextColor '@c3'
}
```

---

## 6. Real-World Example: Modern Theme

```d3e
StyleTheme {
    name 'ModernAppTheme'
    description 'A modern, clean theme for the application.'
    color 'FFFFFFFF'
    font 'Nunito Sans'
    fontSize 16.0
    colors [
        {
            color '@c1'
            hexCode 'FF1976D2'
            description 'Primary Blue'
        }
        {
            color '@c2'
            hexCode 'FF43A047'
            description 'Success Green'
        }
        {
            color '@c3'
            hexCode 'FFE53935'
            description 'Error Red'
        }
        {
            color '@c4'
            hexCode 'FF757575'
            description 'Neutral Gray'
        }
        {
            color '@c5'
            hexCode 'FFFFFFFF'
            description 'White'
        }
        {
            color '@c6'
            hexCode 'FF000000'
            description 'Black'
        }
    ]
    textColor '@c6'
    tooltipBackgroundColor '@c2'
    tooltipTextColor '@c5'
}
```

---

## 7. Prompt for Creating a New Theme

When creating a new theme, use a prompt that follows the model-with-child-properties structure. This ensures clarity and completeness.

### Example Prompt Structure

```prompt
Create a new D3E theme with the following properties:
- Name: [ThemeName]
- Description: [Short description]
- Color: [Default background color hex]
- Font: [Font family]
- FontSize: [Default font size]
- Colors:
    - color: [@c1], hexCode: [HexCode], description: [Primary color]
    - color: [@c2], hexCode: [HexCode], description: [Accent color]
    - ...more colors...
- textColor: [@c7]
- tooltipBackgroundColor: [@c8]
- tooltipTextColor: [@c9]
```

---

## 8. Example Prompts

### Example 1: Modern Theme

```prompt
Create a new D3E theme with the following properties:
- Name: ModernAppTheme
- Description: A modern, clean theme for the application.
- Color: FFFFFFFF
- Font: Nunito Sans
- FontSize: 16.0
- Colors:
    - color: @c1, hexCode: FF1976D2, description: Primary Blue
    - color: @c2, hexCode: FF43A047, description: Success Green
    - color: @c3, hexCode: FFE53935, description: Error Red
    - color: @c4, hexCode: FF757575, description: Neutral Gray
    - color: @c5, hexCode: FFFFFFFF, description: White
    - color: @c6, hexCode: FF000000, description: Black
- textColor: @c6
- tooltipBackgroundColor: @c2
- tooltipTextColor: @c5
```

### Example 2: Minimal Theme

```prompt
Create a new D3E theme with the following properties:
- Name: MinimalTheme
- Description: Minimal, light theme for dashboards.
- Color: FFFFFFFF
- Font: Roboto
- FontSize: 14.0
- Colors:
    - color: @c1, hexCode: FF212121, description: Primary Black
    - color: @c2, hexCode: FF90CAF9, description: Accent Blue
    - color: @c3, hexCode: FFFBC02D, description: Warning Yellow
    - color: @c4, hexCode: FFEEEEEE, description: Light Gray
    - color: @c5, hexCode: FFFFFFFF, description: White
- textColor: @c1
- tooltipBackgroundColor: @c2
- tooltipTextColor: @c5
```

---
