
# D3E Classes COMPREHENSIVE REFERENCE

## Introduction

In D3E Studio, **Classes** are the fundamental building blocks for organizing and structuring application logic. With thousands of classes in large-scale applications, understanding their structure, patterns, and best practices becomes crucial for maintaining code quality, reusability, and system architecture. Classes serve as blueprints that encapsulate data and behavior, enabling developers to create modular, maintainable, and scalable applications.

Classes in D3E can be deployed across different tiers (client, server, shared) and serve various purposes from utility functions to complex business logic, data processing, and service integration.

---

## Class Architecture Overview

### Tier-Based Classification

**Client Classes (`client class`)**
- Execute on client-side (mobile apps, web browsers)
- Handle UI logic, user interactions, client-side data processing
- Cannot directly access server resources or databases
- Examples: UI utilities, client-side validation, data formatting

**Server Classes (`server class`)**
- Execute on server-side infrastructure
- Handle business logic, database operations, external service integration
- Have access to server resources, databases, and third-party APIs
- Examples: Data access layers, business services, authentication

**Shared Classes (no tier annotation)**
- Can execute on both client and server
- Contain common utilities, data models, and shared logic
- Must be platform-agnostic and not depend on tier-specific resources
- Examples: Data models, mathematical utilities, common algorithms

---

## Class Syntax and Structure

### Basic Class Definition

```d3e
[tier] class ClassName {
    static Type staticProperty = defaultValue;
    Type instanceProperty;
    ClassName([parameters]);
    static ReturnType staticMethod([parameters]) {
        // implementation
    }
    ReturnType instanceMethod([parameters]) {
        // implementation
    }
}
````

### Syntax Rules and Conventions

* **No Commas**: Never use commas between class members or in parameter lists
* **Type Safety**: Always specify types for properties, parameters, and return values
* **Naming**: PascalCase for classes, camelCase for methods/properties
* **Access Modifiers**: Use underscore prefix (\_) for private members
* **Static vs Instance**: Choose based on whether state is needed

---

## Class Categories and Patterns

### 1. Utility Classes (Static-Only)

```d3e
client class LeadUtils {
    static List<String> filterRanges = [...];
    static List<String> leadStatuses = [...];

    static String toGMTFromDateTime(DateTime dateTime, {String format = 'd MMMM y hh:mm aaa'}) { ... }

    static List<Lead> getLeadsByStatus(List<Lead> leads, String status) { ... }

    static DateTime getToDateFilter(String filterByRange) { ... }

    static List<String> colorPalette = [...];

    static String getColorForFirstLetter(String name) { ... }
}
```

### 2. Service Classes (Server-Side)

```d3e
server class TwilioService {
    static TwilioService get();
    String getAccessToken(User user, {Boolean isMobile = false});
    String getRecordingUrl(String recordingSid);
    ...
}
```

### 3. Client Integration Classes

```d3e
client class TwilioClient {
    String accessToken;
    String callSid;
    CallData data;
    Boolean isMuted;

    TwilioClient(this.accessToken);
    void setAccessToken(String token);
    Future<Boolean> checkMicPermission();
    ...
}
```

### 4. Data Processing Classes

```d3e
client class ChartDataUtils {
    static Future<List<DataSet>> getStatusBasedChartData(List<LeadAssignment> leadAssignments) async { ... }

    static String getCount(List<DataSet> dataSets) { ... }
}
```

### 5. Stateful Management Classes

```d3e
client class CallDurationUtils {
    Timer _timer;
    Duration _duration = Duration(minutes: 0, seconds: 0);

    CallDurationUtils();

    void startCallDuration(DateTime startTime, {Consumer<String> onUpdate}) { ... }

    String _formatDuration(Duration duration) { ... }

    static String formatDateTime(DateTime dateTime) { ... }
}
```

### 6. Time and Timezone Management Classes

```d3e
client class TimeZoneUtil {
    static List<String> allTimeZones() {
        List<String> inputs = [
            'UTC(GMT+00:00) Default',
            ...
            'Australia/Sydney(GMT+10:00)'
        ];
        return inputs;
    }

    static String chatMessageTimestamp(DateTime last) {
        DateTime currentDate = DateTime.now();
        ...
        return message;
    }
}
```

---

## Class Annotations and External Integration

### Platform-Specific Implementations

```d3e
@Dart('classes/ApolloClient.dart#ApolloClient')
@TypeScript('classes.ApolloClient')
client class ApolloClient {
    ApolloClient();
    Future<List<Lead>> searchLeads(SearchCriteria criteria);
}

@Java('classes.TwilioService')
server class TwilioService {
    static TwilioService get();
    // ... method implementations
}

@Java('rest.MicrosoftOAuth')
server class MicrosoftOAuth {
    static MicrosoftOAuth get();
    Boolean readEmailsFromLead(MicroSoftAcc acc, Lead lead);
    String createLink(Object context);
    Boolean refreshAccessToken(MicroSoftAcc acc);
}
```

```
