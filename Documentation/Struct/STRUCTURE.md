
# Struct

## Introduction

In D3E Studio, **structs** define a structure for holding data, similar to models, but with key differences. Structs are lightweight, temporary data containers that **cannot be stored in the database**. They are used for passing and managing data within the application, especially for:

- **Server to Client Communication:** Organize and send data from server to client.
- **Widget to Widget Communication:** Pass structured data between widgets.
- **Temporary Data Holding:** Hold or manipulate data temporarily in classes or methods, without persistent storage.

---

## Key Components of Structs

- **Name:**
  - Uniquely identifies the struct within a project.
- **Description:**
  - Provides additional information to help understand or explain the struct.
- **Properties:**
  - Define the attributes or fields of the struct, specifying their names, types, and characteristics.
- **Documentation:**
  - Allows users to add notes, explanations, or guidelines related to the struct for collaboration and clarity.

---

## Key Components of Properties

- **Name:**
  - The unique identifier for the property within the struct.
- **Type:**
  - Specifies the kind of data the property holds. Types can be primitive (e.g., String, Integer), another model, or an option set.
  - Example from `FailureMessage` struct:
    ```d3e
    Struct {
        name 'FailureMessage'
        properties [
            {
                name 'Message'
                type String
            }
        ]
    }
    ```
- **Collection:**
  - Indicates if the property can hold multiple values (list/array).
  - Example from `SubjectData` struct:
    ```d3e
    (Struct SubjectData) {
        properties [
            {
                name 'chapters'
                type SubjectChapterData
                collection true
            }
            {
                name 'topics'
                type ChapterTopicData
                collection true
            }
        ]
    }
    ```
- **Description:**
  - Additional explanation or representation of the property.
- **Computed:**
  - A property whose value is derived from computations or aggregations on other struct members.
- **Internal:**
  - A property or struct kept private within a module, not exposed externally.

---

## Creating a Struct

1. Select **Struct** in the "Create New" menu.
2. Enter a unique name for the struct.
3. (Optional) Add a description for the struct.
4. Add properties:
    - Enter a unique property name.
    - Select a data type.
    - Enable the collection option if the property should hold multiple values.
    - (Optional) Add a description for the property.
    - Enable **Computed** for computed values and provide computation logic.
    - Enable **Internal** if the struct/property should be private.
5. Click **Save**. The struct will appear in the structs list in the Explore tree.

---

## Managing Structs

- **Properties:**
  - To duplicate, edit, or delete a property, use the options in the struct editor.
  - Locate the property and select the desired action.

---

## Common Use Cases in D3E Studio

Based on the LEADMANAGEMENT project, here are some common use cases for structs:

1. **Message Handling:**
   - `FailureMessage`: Used for error handling and displaying failure notifications
   - `SuccessMessage`: Used for success notifications and confirmations
   - `InfoMessage`: Used for general information messages to users

2. **Data Organization:**
   - `SubjectData`: Organizes hierarchical data with collections of chapters and topics
   - `SemesterSubject`: Groups semester-specific subject information
   - `SubjectChapterData`: Structures chapter-specific data within subjects

These examples demonstrate how structs can be used for:
- User feedback and messaging systems
- Organizing hierarchical data structures
- Temporary data storage during user interactions
- Passing complex data between different parts of the application

## Summary

Structs in D3E Studio provide a flexible and efficient way to structure and pass data between different parts of an application without persistent storage. They are ideal for scenarios requiring temporary data management or communication between components and layers of the application. As seen in the LEADMANAGEMENT project, structs are particularly useful for message handling, data organization, and managing hierarchical information structures.
