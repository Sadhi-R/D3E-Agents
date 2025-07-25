# DATAQUERY STRUCTURE

A **DataQuery** in D3E is used to retrieve specific information from the database, often with dynamic inputs. DataQueries are reusable, can be accessed from both server and client, and support input parameters for filtering and pagination.
- Defines database queries with parameterized inputs
- Used to retrieve data based on supplied inputs
- Connects the UI with the data layer

## General Structure

```d3e
DataQuery {
    name '<Display Name>'
    query `<D3E Query Expression>`
    enableSync <true|false>   // Optional, enables real-time sync if true
    needCount <true|false>    // Optional, returns total count if true
    inputs [
        {
            name '<Input Name>'
            type <Type>
            required <true|false> // Optional
        }
        // ... more input definitions ...
    ]
}
```

---

## Real Examples

### 1. LeadsList.d3e
```d3e
DataQuery {
    name 'LeadsList'
    query `Lead.all
     .where((l) => inputs.user == null || l.leadAssignment.assignedTo == inputs.user || (inputs.user.subordinates != null && inputs.user.subordinates.contains(l.leadAssignment.assignedTo)))
     .where((l) => inputs.applyStatus == false || inputs.status == l.status)
     .where((l) => inputs.fromDate == null || l.createdDate >= inputs.fromDate)
     .where((l) => inputs.toDate == null || l.createdDate <= inputs.toDate)
     .orderBy(e => switch(inputs.orderBy) {
         case 'name' : e.name
         case 'phone' : e.phone
         case 'email' : e.email
         case 'status' : e.status
         case 'createdDate' : e.createdDate  
         default : e.createdDate
     }, asc : inputs.ascending)
     .slice(inputs.offset, inputs.pageSize)
`
    inputs [
        { name 'Status' type LeadStatus }
        { name 'ApplyStatus' type Boolean }
        { name 'User' type User }
        { name 'Page Size' type Integer }
        { name 'Offset' type Integer }
        { name 'orderBy' type String }
        { name 'ascending' type Boolean }
        { name 'ToDate' type DateTime }
        { name 'FromDate' type DateTime }
    ]
    needCount true
}
```

---

### 2. UserByEmail.d3e
```d3e
DataQuery {
    name 'UserByEmail'
    query `User.all
    .where((u) => u.email == inputs.email)`
    inputs [
        { name 'Email' type String }
    ]
}
```

---

### 3. MailBox.d3e
```d3e
DataQuery {
    name 'MailBox'
    query `MailMessage.all
    .where((u) => (inputs.searchMail == null || 
    inputs.searchMail.isEmpty || 
    u.senderEmail.toLowerCase().contains(inputs.searchMail.toLowerCase()) || 
    u.recipientEmail.toLowerCase().contains(inputs.searchMail.toLowerCase())))
    .orderBy(e => e.createdDate, asc : false)
    .slice(inputs.offset, inputs.pageSize)`
    inputs [
        { name 'SearchMail' type String }
        { name 'Page Size' type Integer }
        { name 'Offset' type Integer }
    ]
    enableSync true
}
```
- Retrieves specific information from database.
- Can have inputs for dynamic querying.
```d3e
DataQuery {
    name 'Taxes'
    query `TaxRate.all.where((c) => inputs.country == null || inputs.country.isEmpty || c.country == inputs.country)`
    enableSync true
    inputs [
        {
            name 'country'
            type String
            required true
        }
    ]
}
```
- Every Model will have a `all` field that gives a List of that Object. and the rest is just a List api.
---

## Best Practices
- Use clear, descriptive names for both the DataQuery and its inputs.
- The `query` field should be a valid D3E expression, typically filtering a model’s `.all` property.
- Mark inputs as `required` only if they must be provided for the query to work.
- Use `enableSync true` if you want the query to update in real-time when the underlying data changes.
- Use `needCount true` if you need the total count of results for pagination.
