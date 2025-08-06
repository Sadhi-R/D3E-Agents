# D3E UserTypes STRUCTURE

## Introduction

User Types in D3E Studio define the roles, permissions, and authentication mechanisms for users within your application. They are foundational for managing access, shaping user interactions, and ensuring security. Each user type is associated with a user model and specific login settings, enabling tailored user experiences and robust permission control.

---

## Types of Users

D3E applications commonly involve several user types, each with distinct roles and privileges:

| User Type      | Description                                      |
|--------------- |--------------------------------------------------|
| Regular User   | Standard users with basic access and features.   |
| Admin User     | Users with administrative privileges.            |
| Developer User | Users involved in application development.       |
| Anonymous      | Unauthenticated users (public access).           |

---

## UserType Structure

A UserType in D3E is defined by several key properties:

- **name**: Unique identifier for the user type.
- **userModel**: The model representing this user type (must extend `BaseUser`).
- **loginSettings**: Configuration for authentication fields (email, phone, username, password, etc.).
- **roleAccessType**: How roles are assigned (Fixed, Dynamic, None).
- **permissions**: Model, data query, and object list permissions.
- **sessionModel**: (Optional) Model representing session data.

### Example Syntax

```d3e
UserType {
    name 'DeveloperUserType'
    userModel Developer
    loginSettings {
        emailField email
        passwordField password
    }
}
```

---

## Login Settings

Login settings determine how users authenticate. The following fields can be configured:

- **emailField**: Property in userModel for email (must be unique).
- **phoneField**: Property for phone number (must be unique).
- **usernameField**: Property for username (must be unique).
- **passwordField**: Property for password.
- **emailOtpSubject/body**: For OTP-based flows.
- **phoneOtpSubject**: For phone OTP flows.
- **needDemoUser**: Enable/disable demo user feature.

> **Note:** At least one of email, phone, or username must be unique in the user model.

---

## Permissions and Roles

- **Role Access Type**:
    - *Fixed*: Predefined roles assigned to users.
    - *Dynamic*: Roles assigned based on conditions.
    - *None*: No roles assigned.
- **Model Access Permissions**: Define create, update, delete rights for each model.
- **Data Query Permissions**: Specify which queries are allowed.
- **Object List Permissions**: Control access to object lists.

---

## Creating a UserType: Step-by-Step

1. **Define User Model**: Extend `BaseUser` in your model.
2. **Create UserType**: Specify name, userModel, and loginSettings.
3. **Configure Session Model** (optional): Assign a session model if needed.
4. **Set Role Access Type**: Choose Fixed, Dynamic, or None.
5. **Set Permissions**: Define model, query, and object list permissions.
6. **Configure Login Settings**: Map fields for email, phone, username, and password.
7. **Enable Features**: (Optional) Configure OTP and demo user settings.
8. **Save and Review**: Ensure all settings are correct.

---

## Example: UserType and Login API

Given a UserType:

```d3e
UserType {
    name 'DeveloperUserType'
    userModel Developer
    loginSettings {
        emailField email
        passwordField password
    }
}
```

A login API is automatically generated:

```dart
LoginResult result = Query.loginDeveloperUserTypeWithEmailAndPassword(
    email: this.email.toLowerCase(),
    password: this.password
).await;
```

**LoginResult** contains:
- `success`: Boolean
- `userObject`: BaseUser
- `token`: String
- `failureMessage`: String

---

## Best Practices & Notes

- Always ensure unique constraints on login fields (email, phone, username).
- Use descriptive names for user types.
- Document each UserType for collaboration and clarity.
- Review permissions and access settings for security.

---

## Conclusion

User Types are central to defining access and permissions in D3E Studio applications. By following the structure and steps outlined above, you can create robust, secure, and flexible user management systems tailored to your application's needs.