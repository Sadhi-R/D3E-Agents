# D3E Page Structure

## Introduction

A **Page** in D3E is a top-level screen or route in your application. Pages are the main entry points for navigation and are composed of widgets and UI components. Unlike widgets, pages are not reusable—they are designed for distinct screens such as Login, Dashboard, Team, or Audit Log.

This guide defines the canonical structure, syntax, and best practices for D3E Pages in this project, based on real-world examples and the project’s standards.
- Similar to a standard React page
- Represents a full screen in the application
- Can contain multiple widgets
- Handles routing and navigation concerns
- We never create a page for simple create/update/view. We will create a widget for that. And that widget will be used in a page.

Note:
- If any page contains only one widget, then we can directly create build in page for that. We don't need a separate widget for that.
- Ex: a dashboard contains multiple widgets. But, if a Login Page that contains only one login widget, then we can directly create a build in page for that. And no login widget object.

---

## 1. Page Declaration: Syntax & Anatomy

Every page starts with a `Page { ... }` block. The standard structure is:

```d3e
Page {
    // Optional: package 'your.package'
    name 'Page Name'
    // Optional: category 'UserDefined' | ...
    // Optional: description 'A short description of the page'
    // Optional: properties [
    //     { ... }
    // ]
    build <WidgetType> {
        // ... UI tree ...
    }
    // Optional: eventHandlers [
    //     { ... }
    // ]
}
```

**Key Points:**
- **No commas** between items in arrays/lists.
- **No comments** inside D3E code blocks.
- **All properties referenced in the build tree must be declared in the page.**
- The `build` block is always required and defines the UI.
- The root widget in `build` is usually `Column`, but can be any widget.
- Node identity in the build tree must not match any property identity in the same page.

---

## 2. Properties

Properties are used for page state, data, or configuration. Declare them in a `properties [ ... ]` array.

- `internal true`: For local state (e.g., loading flags, input fields)
- `computed true`: For derived or query-backed values
- `collection true`: For lists/arrays

**Property Type Rules:**
- For external model objects (e.g., `User`, `Product`), must specify the model name as the type:
  ```d3e
  {
      name 'User'
      type User
      required true
  }
  ```
  This ensures full access to all model fields (e.g., `user.firstName`, `user.email`).
- For primitive types (`String`, `Boolean`, `int`, `double`), use the type directly
- For internal properties (marked with `internal true`), any type is allowed

**Example of Multiple Properties:**
```d3e
properties [
    {
        name 'User'
        type User
        required true
    }
    {
        name 'Email'
        type String
        internal true
    }
    {
        name 'Loading'
        type Boolean
        internal true
    }
]
```
Properties are optional—some pages may not declare any.

---

## 3. Build Tree: UI Composition

The `build` block defines the visual structure of the page using widgets. Use `children` to compose multiple widgets, and `data` for widget configuration.

**Example:**
```d3e
build Column {
    name 'MainColumn'
    children [
        Row {
            name 'HeaderRow'
            children [
                TextView {
                    name 'Title'
                    data {
                        data 'Welcome!'
                    }
                }
            ]
        }
        // ... more widgets ...
    ]
}
```
- All non-binded properties inside `data` must be strings and parsable to their real type (including enums/option sets).
- Node identity should not match any property identity.

---

## 4. Event Handlers

Pages can declare `eventHandlers [ ... ]` for lifecycle and UI events. Common events include `OnInit` (runs when the page loads) and handlers for user actions (e.g., button presses).

**Example:**
```d3e
eventHandlers [
    {
        name 'OnInit'
        block ```
            // Initialization logic
        ```
    }
    {
        name 'onLoginButtonHandler'
        type OnEvent
        on loginButton
        event onPressed
        block ```
            // Handle login
        ```
    }
]
```
- Each event handler maps to one event on one widget node.
- The `OnInit` event handler is special and runs once on page render.

---

## 5. Creating a New Page: Step-by-Step

1. **Define the purpose and main UI of the page.**
2. **Declare required properties** (e.g., user, data objects, state flags).
3. **Compose the UI in the `build` block** using widgets, rows, columns, and control widgets (`CIf`, `CFor`).
4. **Add event handlers** for initialization and user actions.
5. **Test and refactor**: Move repeated or complex UI into widgets.

---

## 6. Real-World Example: Login Page

```d3e
Page {
    package 'lead.management'
    name 'Login Page'
    category 'UserDefined'
    properties [
        {
            name 'Email'
            type String
            internal true
        }
        {
            name 'Password'
            type String
            internal true
        }
        {
            name 'Loading'
            type Boolean
            internal true
        }
    ]
    build Column {
        name 'Column'
        children [
            TextView {
                name 'Title'
                data {
                    data 'Login'
                }
            }
            LabelField {
                name 'Email Field'
                data {
                    name 'Email'
                    value `email`
                }
                twoWayBinding true
            }
            LabelField {
                name 'Password Field'
                data {
                    name 'Password'
                    value `password`
                    obscureText 'true'
                }
                twoWayBinding true
            }
            Button {
                name 'Login Button'
                child TextView {
                    data {
                        data 'Login'
                    }
                }
            }
        ]
    }
    eventHandlers [
        {
            name 'OnInit'
            block ```
                // Initialization logic
            ```
        }
        {
            name 'onLoginButtonHandler'
            type OnEvent
            on loginButton
            event onPressed
            block ```
                // Handle login
            ```
        }
    ]
}
```

---

## 7. Minimal Example: Team Page

```d3e
Page {
    package 'lead.management'
    name 'Team Page'
    category 'UserDefined'
    build Column {
        name 'Column'
        children [
            Row {
                name 'Row'
                children [
                    TeamWidget {
                        name 'TeamWidget'
                        data {
                            expand 'true'
                            user `null`
                        }
                    }
                ]
            }
        ]
    }
}
```

---

## 8. Best Practices

- **No commas** in arrays/lists.
- **No comments** inside D3E code blocks (use markdown for documentation).
- **All properties referenced in the build tree must be declared.**
- **Use `internal true` for local state.**
- **Use `computed true` for derived/query-backed properties.**
- **Use clear, descriptive names for pages and properties.**
- **Keep page logic focused on layout and navigation; use widgets for reusable UI logic.**
- **Event handlers**: Use for lifecycle and UI events only.
- **Pages are not reusable**—use widgets for reusable components.
- **Node identity in the build tree must not match any property identity.**
- **All non-binded properties inside `data` must be strings and parsable to their real type.**
- **Pages cannot be used inside other pages or widgets.**
- **Pages extend BaseComponent and can use its properties.**

---

## 9. D3E Page & Widget Relationship

- **Pages** are the main navigation targets and cannot be used as children in other widgets or pages.
- **Widgets** are reusable UI components and can be composed inside pages or other widgets.
- Both pages and widgets extend `BaseComponent` and can use its properties (e.g., width, style).
- **Properties**: By default, all are external unless marked `internal true`. Only internal properties can be mutated in event handlers.
- **No property of type Widget or Page**: Use `slots` for widget composition.
- **Build tree**: All nodes must have unique identities not matching any property.

---

## 10. Advanced Example: Login Page

```d3e
Page {
    package 'lead.management'
    name 'Login Page'
    category 'UserDefined'
    properties [
        {
            name 'Email'
            type String
            internal true
        }
        {
            name 'Password'
            type String
            internal true
        }
        {
            name 'Email Info'
            type Boolean
            internal true
        }
        {
            name 'Password Info'
            type Boolean
            internal true
        }
        {
            name 'Error Messages'
            type String
            internal true
        }
        {
            name 'Show Error'
            type Boolean
            internal true
        }
        {
            name 'Loading'
            type Boolean
            internal true
        }
        {
            name 'isRememberMe'
            type Boolean
            internal true
        }
        {
            name 'Device Token'
            type String
            internal true
        }
        {
            name 'Invalid Error Message'
            type String
            internal true
        }
    ]
    build Column {
        name 'Column'
        styles [
            ScreenBgColor
        ]
        data {
            mainAxisAlignment 'center'
            crossAxisAlignment 'center'
        }
        children [
            Column {
                styles [
                    BaseViewStyle
                ]
                data {
                    mainAxisAlignment 'center'
                    crossAxisAlignment 'start'
                    width '550'
                    mainAxisSize 'min'
                    padding '30'
                }
                children [
                    TextView {
                        name 'TextView'
                        styles [
                            HeadlineTwo
                        ]
                        data {
                            data 'Lead Management'
                            margin '0 5 20 5'
                            color '@c1'
                        }
                    }
                    CIf {
                        name 'ImageView Condition'
                        condition `false`    
                        then ImageView {
                            name 'ImageView'
                            data {
                                imageType 'Asset'
                                imageUrl 'images/app_icon.png'
                                width '180'
                                height '180'
                            }
                        }
                    }
                    TextView {
                        name 'TextView'
                        styles [
                            HeadlineThree
                        ]
                        data {
                            data 'Login'
                            margin '0 5 10 5'
                        }
                    }
                    LabelField {
                        name 'Email Field'
                        data {
                            name 'Email'
                            placeHolder 'Enter Email Address'
                            value `email`
                            errors `emailInfo ? ['Please Enter Email Address'] : []`
                            isRequired 'true'
                            textStyle {
                                color 'ff000000'
                            }
                        }
                        twoWayBinding true
                    }
                    LabelField {
                        name 'PasswordField'
                        data {
                            name 'Password'
                            placeHolder 'Enter Password'
                            value `password`
                            errors `passwordInfo ? ['Please Enter Password'] : []`
                            margin '10 0 0'
                            obscureText 'true'
                            isRequired 'true'
                        }
                        twoWayBinding true
                    }
                    Row {
                        name 'Forgot Password Row'
                        data {
                            mainAxisAlignment 'end'
                            margin '10 5'
                            padding '0'
                        }
                        children [
                            Button {
                                name 'Forgot Password Button'
                                styles [
                                    LinkButton
                                ]
                                child TextView {
                                    name 'Forgot Password Text'
                                    data {
                                        data 'Forgot Password ?'
                                        fontSize '14'
                                    }
                                }
                            }
                        ]
                    }
                    CIf {
                        name 'Error Message Condition'
                        condition `showError`
                        then TextView {
                            name 'Error Message'
                            styles [
                                ErrorText   
                            ]
                            data {
                                data 'Invalid authentication details. Please Enter valid details.'
                                fontSize '14'
                                margin '5 0 0'
                            }
                            conditionals [
                                {
                                    condition `invalidErrorMessage != null && invalidErrorMessage.isNotEmpty`
                                    values {
                                        data `invalidErrorMessage`
                                    }
                                }
                            ]
                        }
                    }
                    Row {
                        name 'Row'
                        data {
                            margin '20 5'
                        }
                        children [
                            Button {
                                name 'Login Button'
                                styles [
                                    Primary
                                ]
                                data {
                                    expand 'true'
                                }
                                child Row {
                                    name 'Row'
                                    data {
                                        mainAxisAlignment 'center'
                                    }
                                    children [
                                        CIf {
                                            name 'Loading Condition'
                                            condition `loading`
                                            then Loader {
                                                name 'CircularProgressIndicator'
                                                data {
                                                    backgroundColor '@c14'
                                                    valueColor '@c1'
                                                }
                                            }
                                        }
                                        TextView {
                                            name 'ButtonText'
                                            data {
                                                data 'Login'
                                                padding '0 10'
                                            }
                                        }
                                    ]
                                } 
                            }
                        ]
                    }
                    Row {
                        name 'Row'
                        data {
                            mainAxisAlignment 'center'
                            margin '10 5'
                        }
                        children [
                            TextView {
                                name 'TextView'
                                data {
                                    data `'Version '+ Env.get().buildVersion`
                                    fontSize '14'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'OnInit'
            block ```
                
            ``` 
        }
        {
            name 'onTapEmailFiledHandler'
            type OnEvent
            on emailField
            event onTap
            block ```
                emailInfo = false;
            ```
        }
        {
            name 'onTapPasswordFiledHandler'
            type OnEvent
            on passwordField
            event onTap
            block ```
                passwordInfo = false;
            ```
        }
        
        {
            name 'AuthenticatingUser'
            block ```
                this.invalidErrorMessage = '';
                if(email.isEmpty) {
                    emailInfo = true;
                }
                if(password.isEmpty) {
                    passwordInfo = true;
                }
                loading = true;
                deviceToken = FirebaseUtil.getToken().await;
                LoginResult result = 
                Query.loginManagerUserWithEmailAndPassword(
                    email: this.email.toLowerCase(),
                    password: password,
                    deviceToken: this.deviceToken
                ).await;
                
                if(result.success) {
                    User user = result.userObject as User;
                    if (user.status) {
                        user.isRememberMe = isRememberMe;
                        Result<User> userResult = user.save().await;
                        AuditLogUtils.loginedUser = user;
                        navigator.pushRoutePage(user: user);
                    } else {
                       user.isRememberMe = false;
                        this.showError = true;
                       this.invalidErrorMessage =  'Your Account is Disabled';
                    }
                    
                }else {
                    this.errorMessages = result.failureMessage;
                    if (this.errorMessages == result.failureMessage) {
                        this.showError = true;
                    }
                }
                loading = false;
            ```
        }
        {
            name 'onLoginButtonHandler'
            type OnEvent
            on loginButton
            event onPressed
            block ```
                authenticatingUser();
            ```
        }
        {
            name 'onSubmitHandler'
            type OnEvent
            on passwordField
            event onSubmitted   
            block ```
                authenticatingUser();
            ```
        }
        {
            name 'forgotPasswordHandler'
            type OnEvent
            on forgotPasswordButton
            event onPressed
            block ```
                //Test bundle upload
                navigator.pushForgotPasswordPage();
            ```
        }
    ]
}
```

 **Requirement:** Login and create a Customer record

    **Flow:**
    1.  User accesses login page
    2.  User fills credentials and clicks login button
    3.  Upon successful login, user navigates to Home page
    4.  User opens new customer form
    5.  User fills details and clicks save button

    **Actions:**
    -   On login click: A login request is sent to the server through an RPCService
    -   On successful authentication: User information is retrieved and stored in session
    -   On customer save click: Customer model is instantiated, populated with form data, and saved to the database

    ##  Your Responsibilities

    When presented with functional requirements, you will:

    1.  Analyze the provided functional requirements thoroughly
    2.  Create a high-level architecture document that outlines:

        ### Backend Plan
        -   For each individual point in the specification, specify how different D3E features/data models will be used to implement that task
        -   Include:
            -   Model definitions required
            -   Lifecycle hooks to utilize
            -   Data Queries needed
            -   RPCServices to implement
            -   Channels for real-time features
        -   Example:
            -   Requirement: "On signup, user should get welcome email"
            -   Solution: "We will create a 'User' model for each signup. On creation of a User model (using the 'On Create' lifecycle hook), we will create an EmailNotification object with the welcome content and save it. An RPCService will handle the actual email delivery."

        ### Frontend Plan
        -   For each individual point in the specification, specify the user flow
        -   Include:
            -   Pages required
            -   Widgets needed on each page
            -   Navigation paths between pages
            -   User interactions and their outcomes
            -   Data display and form strategies
        -   Example:
            -   Requirement: "Users should be able to view their profile"
            -   Solution: "Create a UserProfilePage with UserInfoWidget, UserStatsWidget, and UserPreferencesWidget. Navigation to this page will be available from the main menu. The page will use a UserDataQuery to fetch profile information using the current user's ID."
---

## Color and Style Usage Rules

- When specifying colors in pages or widgets, always use existing color codes defined in the current theme (e.g., @c1, @c2, ...). If you need a color not present in the theme, use a direct hex code (e.g., 'ff000000').
- For styles, always use an existing style if it matches the requirement. If no suitable style exists, specify the style properties directly within the component.

## General Widget Properties

All widgets used in pages can use the following general properties:
- `height`
- `width`
- `padding`
- `margin`
- `backgroundColor`
- `color`
- ...and other standard properties as seen in existing widget examples.

Refer to the project's existing widgets and styles for best practices and property usage.
