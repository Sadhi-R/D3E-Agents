# Basic Widget

## What is a Basic Widget?
A **Basic Widget** is a standard, reusable UI component in D3E. It encapsulates a specific piece of functionality or display logic and is the foundation for building more complex widgets. Basic widgets have their own properties and a build tree, and may include event handlers, but do not use advanced composition features like slots.

## Prompt Template
"Create a basic widget that [describe the functionality, e.g., displays a counter and an increment button]."

## Example Prompts
- Create a basic widget that shows a number and a button to increment it.
- Build a simple label widget that displays a string property.
- Make a widget with a boolean property and a toggle button.

## D3E Example
```d3e
Widget {
    package 'agentcanvas.com'
    name 'Basic Login Widget'
    category 'UserDefined'
    build Column {
        name 'Column'
        data {
            mainAxisAlignment 'center'
        }
        children [
            TextView {
                name 'TextView'
                data {
                    data 'Login '
                    fontSize '25'
                    fontWeight 'w800'
                }
            }
            LabelField {
                name 'Email Field'
                data {
                    label 'Email'
                    isRequired 'true'
                    placeHolder 'Enter your email'
                    width '250'
                }
            }
            LabelField {
                name 'Password Field'
                data {
                    label 'Password'
                    isRequired 'true'
                    placeHolder 'Enter your password'
                    width '250'
                    margin '10 0'
                    obscureText 'true'
                }
            }
            Button {
                name 'Button'
                data {
                    width '250'
                    decoration {
                        color '@c8'
                    }
                }
                child TextView {
                    name 'ButtonText'
                    data {
                        data 'Login'
                    }
                }
            }
        ]
    }
    eventHandlers [
        {
            name 'onPressedButtonHandler'
            type OnEvent
            on button
            event onPressed
            block ```
                
                /* Your code here. */
            ```
        }
    ]
}
```
# Example 2

```d3e
Widget {
    package 'agentcanvas.com'
    name 'Basic Signup Widget'
    category 'UserDefined'
    build Column {
        name 'Column'
        data {
            mainAxisAlignment 'center'
        }
        children [
            TextView {
                name 'TextView'
                data {
                    data 'Sign up'
                    fontSize '25'
                    fontWeight 'w900'
                }
            }
            LabelField {
                name 'Name Field'
                data {
                    label 'Name'
                    isRequired 'true'
                    placeHolder 'Please enter your name...'
                    width '250'
                }
            }
            LabelField {
                name 'Email Field'
                data {
                    label 'Email'
                    isRequired 'true'
                    placeHolder 'Please Enter your email'
                    width '250'
                }
            }
            LabelField {
                name 'Phone Field'
                data {
                    label 'Phone Number'
                    isRequired 'true'
                    placeHolder 'Plese enter your phone'
                    width '250'
                }
            }
            LabelField {
                name 'Address Field'
                data {
                    label 'Address'
                    isRequired 'true'
                    placeHolder 'Enter your address'
                    width '250'
                }
            }
            Button {
                name 'Button'
                data {
                    width '250'
                    margin '15 0'
                    decoration {
                        color '@c18'
                    }
                }
                child TextView {
                    name 'ButtonText'
                    data {
                        data 'Varify'
                    }
                }
            }
        ]
    }
    eventHandlers [
        {
            name 'onPressedButtonHandler'
            type OnEvent
            on button
            event onPressed
            block ```
                
                /* Your code here. */
            ```
        }
    ]
}
```
