import json

# Test the generated content
test_content = '''[
    {
        "name": "LoginPage",
        "category": "UserDefined",
        "properties": [
            {
                "name": "email",
                "type": "String",
                "internal": true
            }
        ]
    }
]'''

try:
    parsed = json.loads(test_content)
    print("JSON is valid!")
    print(f"Component name: {parsed[0]['name']}")
    print(f"Category: {parsed[0]['category']}")
    
    # Check if this is a widget
    if 'buildTree' in parsed[0] or 'properties' in parsed[0]:
        print("This looks like a widget component")
    
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
