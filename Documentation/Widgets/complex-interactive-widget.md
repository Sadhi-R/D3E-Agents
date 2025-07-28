# Complex Interactive Widget

## What is a Complex Interactive Widget?
A **Complex Interactive Widget** combines multiple features: internal state, events, slots, styles, and data binding, to create rich, interactive UI components. These widgets are used for advanced scenarios where multiple interactive features are required.

## Prompt Template
"Create a complex interactive widget that [describe the features, e.g., has a text input, a send button, and shows a loading state]."

## Example Prompts
- Create a chat input widget with a message field, send button, and loading indicator.
- Build a form widget with multiple fields, validation, and submit/cancel actions.
- Make a dashboard widget that combines charts, filters, and actions.

## D3E Example
```d3e
Widget {
    package 'lead.management'
    name 'AddUserView'
    category 'UserDefined'
    properties [
        {
            name 'User'
            type User
            required true
        }
        {
            name 'Errors'
            collection true
            type String
            internal true
        }
        {
            name 'isAdmin'
            type Boolean
            required true
        }
    ]
    build PopupWrapperView {
        name 'popupWrapper'
        data {
            title 'Add New User'
        }
        slots [
            {
                slot content
                child Column {
                    name 'Column'
                    children [
                        Container {
                            name 'Container'
                            data {
                                width '100'
                                height '100'
                                decoration {
                                    border {
                                        color 'ff000000'
                                        width '1'
                                    }
                                    borderRadius '50'
                                }
                                alignment 'center'
                                margin '10 0'
                                cursor 'click'
                            }
                            child CIf {
                                name 'CIf3'
                                condition `user.profile == null || user.profile.downloadUrl == null`
                                then ImageView {
                                    name 'ImageView3'
                                    data {
                                        imageType 'Asset'
                                        imageUrl 'images/profile1.png'
                                        width '100'
                                        height '100'
                                        cornerRadius '50'
                                        fit 'fill'
                                    }
                                }
                                else ImageView {
                                    name 'ProviderImage2'
                                    data {
                                        imageType 'Network'
                                        imageUrl `user.profile.downloadUrl + '?width=100&height=100&inline=true'`
                                        width '100'
                                        height '100'
                                        cornerRadius '50'
                                        fit 'fill'
                                    }
                                }
                            }
                            behaviours [
                                GestureDetector
                            ]
                        }
                        LabelField {
                            name 'LabelField'
                            data {
                                name 'First Name'
                                placeHolder 'Enter First Name'
                                value `user.firstName`
                                errors `firstNameErrors`
                                isRequired 'true'
                            }
                            twoWayBinding true
                        }
                        LabelField {
                            name 'LabelField1'
                            data {
                                name 'Last Name'
                                placeHolder 'Enter Last Name'
                                value `user.lastName`
                                errors `lastNameErrors`
                                isRequired 'true'
                            }
                            twoWayBinding true
                        }
                        LabelDropdown {
                            name 'LabelDropdown'
                            type UserRole
                            data {
                                name 'Role'
                                placeHolder 'Select Role'
                                value `user.role`
                                items `isAdmin? UserRole.values : UserRole.values.where((e) => e != UserRole.Admin).toList()`
                                errors `roleErrors`
                                width '500'
                            }
                            builder TextView {
                                name 'TextView1'
                                data {
                                    data `item.name`
                                }
                            }
                            twoWayBinding true
                        }
                        LabelField {
                            name 'LabelField2'
                            data {
                                name 'Email Address'
                                placeHolder 'Enter Email Address'
                                value `user.email`
                                errors `emailErrors`
                                isRequired 'true'
                            }
                            twoWayBinding true
                        }
                        LabelField {
                            name 'LabelField4'
                            data {
                                name 'Password'
                                placeHolder 'Enter Password'
                                value `user.password`
                                errors `passwordErrors`
                                obscureText 'true'
                                isRequired 'true'
                            }
                            twoWayBinding true
                        }
                        LabelField {
                            name 'LabelField3'
                            data {
                                name 'Phone Number ( Enter with country code )'
                                placeHolder 'Enter Phone Number'
                                value `user.phoneNumber`
                            }
                            twoWayBinding true
                        }
                        CFor {
                            name 'CFor'
                            var 'error'
                            items `errors`
                            type String
                            item Column {
                                name 'Column'
                                data {
                                    crossAxisAlignment 'start'
                                    margin '5 0 0 0'
                                }
                                children [
                                    TextView {
                                        styles [
                                            ErrorText
                                        ]
                                        name 'TextView'
                                        data {
                                            data `error`
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
            {
                slot buttons
                children [
                    Button {
                        name 'CancelButton'
                        styles [
                            Secondary
                        ]
                        data {
                        }
                        child TextView {
                            name 'ButtonText2'
                            data {
                                data 'Cancel'
                            }
                        }
                    }
                    Button {
                        name 'UserButton'
                        styles [
                            Primary
                        ]
                        child TextView {
                            name 'ButtonText'
                            data {
                                data 'Add New User'
                            }
                        }
                    }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'onPressedProfileButtonHandler'
            type OnBehaviour
            on container
            behaviour GestureDetector
            event onTap
            block ```
                FileToUpload fileToUpload = Browser.selectFile(['jpg', 'jpeg', 'png'], (){}).await;
                if(fileToUpload != null) {
                    FileUploadResult res = PlatformClient.upload(fileToUpload).await;
                    if(res.success){
                        user.profile = res.file; 
                    }
                }
            ```
        }
        {
            name 'cancelButtonHandler'
            type OnEvent
            on cancelButton
            event onPressed
            block ```
                user.restore();
                navigator.close();
            ```
        }
        {
            name 'onAddUserHandler'
            type OnEvent
            on userButton
            event onPressed
            block ```
                errors = [];
                if(user.phoneNumber != null) {
                    user.phoneNumber = TwilioClient.getPurifiedPhoneNumber(user.phoneNumber);
                }
                if(validate().isEmpty){
                    user.email = user.email.replaceAll(' ', '');
                    user.email = user.email.toLowerCase();
                    Result<User> result = user.save().await;
                    if(result.status == Success) {
                    MicroSoftAcc acc = MicroSoftAcc(
                        user: user,
                    );
                    Result<MicroSoftAcc> accResult = acc.save().await;
                    if(accResult.status == Success) {
                        EventBus.get().fire(SuccessMessage(message : 'Successfully Saved'));
                        navigator.close();
                    } else {
                        errors = accResult.errors;
                    }
                    } else {
                        errors = result.errors;
                    }
                }  
            ```
        }
    ]
    editorFor User
    editorInput user
}
```

# Example 2

```d3e
Widget {
    package 'lead.management'
    name 'CallProgressView'
    properties [
        {
            name 'client'
            type TwilioClient
        }
        {
            name 'callInteraction'
            type CallInteraction
            synchronise true
        }
        {
            name 'Interaction'
            type Interaction
            required true
            fetchData true
            synchronise true
        }
        {
            name 'isMute'
            type Boolean
            defaultValue `false`
            internal true
        }
        {
            name 'callDuration'
            type String
            internal true
        }
        {
            name 'data'
            type CallData
            computed true
            computation `callInteraction.data`
            internal true
        }
        {
            name 'status'
            type CallStatus
            computed true
            computation `callInteraction.data.callStatus`
            internal true
            onChange onChangeCallId
        }
        {
            name 'duration Start'
            type Boolean
            internal true
        }
        {
            name 'User'
            type User
            required true
            fetchData true
            synchronise true
        }
    ]
    build Column {
        name 'Column'
        data {
            decoration {
                color '@c2'
                border {
                    color '@c2'
                }
                borderRadius '15'
            }
        }
        children [
            Row {
                name 'Row'
                data {
                    mainAxisAlignment 'spaceBetween'
                    padding '15 15 0 15'
                }
                children [
                    Row {
                        name 'Row'
                        data {
                            margin '10 0 0 0'
                        }                        
                        children [
                            TextView {
                                name 'TextView'
                                conditionals [
                                        {
                                            condition `interaction.isConference`
                                            values {
                                                data 'Conference Call'
                                            }
                                        }
                                        {
                                            condition `callInteraction.lead == null`
                                            values {
                                                data 'Unknown Caller'
                                            }
                                        }
                                    ]
                                data {
                                    data `callInteraction.lead.name`
                                    fontSize '16'
                                    color '@c14'
                                    fontWeight 'bold'
                                }
                               
                            }
                            TextView {
                                name 'TextView6'
                                data {
                                    data `callDuration`
                                    fontWeight 'w400'
                                    color '@c14'
                                    margin '0 0 0 10'
                                }
                            }
                            CIf {
                                name 'AssignToLeadRef'
                                condition `callInteraction.lead == null`
                                then Button {
                                    name 'AssignToLeadButton'
                                    styles [
                                        LinkButton
                                    ]
                                    data {
                                        margin '0 0 0 5'
                                    }
                                    child TextView {
                                        name 'TextView'
                                        data {
                                            data 'Assign to Lead'
                                            color '@c1'
                                        }
                                    }
                                }
                            }
                        ]
                    }
                    Container {
                        data {
                            width '80'
                        }
                    }
                    IconButton {
                        name 'addParticipant'
                        data {
                            icon 'MaterialIcons.group_add'
                            color '@c14'
                        }
                    }
                    IconButton {
                        name 'Minimize'
                        data {
                            icon 'MaterialIcons.minimize'
                            color '@c14'
                        }
                    }
                ]
            }
            Row {
                name 'Row'
                children [
                    Container {
                        name 'Container'
                        data {
                            height '1'
                            decoration {
                                color '@c19'
                            }
                            margin '10 0'
                            expand 'true'
                        }
                    }
                ]
            }
            Column {
                name 'Column2'
                data {
                    height '150'
                    mainAxisAlignment 'center'
                    expand 'true'
                }
                children [
                    Container {
                        name 'Container'
                        data {
                            width '80'
                            height '80'
                            alignment 'center'
                            decoration {
                                borderRadius '50'
                                border {
                                    color 'ff4caca4'
                                    width '2'
                                }
                            }
                            padding '3'
                        }
                        child Container {
                            name 'Container'
                            data {
                                width '76'
                                height '76'
                                alignment 'center'
                                decoration {
                                    color '@c14'
                                    borderRadius '50'
                                    border {
                                        color '@c14'
                                        width '2'
                                    }
                                }
                            }
                            child Center {
                                name 'Center'
                                child TextView {
                                    name 'TextView2'
                                    conditionals [
                                        {
                                            condition `callInteraction.lead == null || callInteraction.lead.name == null || (callInteraction.lead.name.trim().length < 1)`
                                            values {
                                                data 'UN'
                                            }
                                        }
                                    ]
                                    data {
                                        data `callInteraction.lead.name[0] + callInteraction.lead.name[1]`
                                        color 'ff4caca4'
                                        fontWeight 'bold'
                                        fontSize '35'
                                        textAlign 'center'
                                    }
                                }
                            }
                        }
                    }
                    TextView {
                        name 'TextView'
                        data {
                            data `interaction.callStatus.name`
                            color '@c14'
                        }
                        conditionals [
                            {

                                condition `interaction == null`
                                values {
                                    data 'Initiating...'
                                    color '@c1'
                                }
                            }
                            {
                                condition `interaction.callStatus == Unanswered`
                                values {
                                    data 'Incoming Call'
                                }
                            }
                        ]
                    }
                    Row {
                        name 'Row'
                        data {
                            mainAxisAlignment 'center'
                            margin '15'
                        }
                        children [
                            Container {
                                name 'Mutecall'
                                data {
                                    width '40'
                                    height '40'
                                    decoration {
                                        color 'ff5c5cc4'
                                        borderRadius '20'
                                    }
                                    alignment 'center'
                                    cursor 'click'
                                }
                                child IconView {
                                    name 'muteButton'
                                    data {
                                        icon 'MaterialIcons.mic'
                                        tooltip 'Mute'
                                        color '@c14'
                                    }
                                    conditionals [
                                        {
                                            condition `client.isMuted`
                                            values {
                                                icon 'MaterialIcons.mic_off'
                                                tooltip 'Unmute'
                                            }
                                        }
                                    ]
                                }
                                behaviours [
                                    GestureDetector
                                ]
                            }
                            Container {
                                name 'Container'
                                 data {
                                    width '10'
                                }
                            }
                            Container {
                                name 'EndCall'
                                data {
                                    width '40'
                                    height '40'
                                    decoration {
                                        color 'fff0465c'
                                        borderRadius '20'
                                    }
                                    alignment 'center'
                                    cursor 'click'
                                }
                                child IconView {
                                    name 'icon2'
                                    data {
                                        icon 'MaterialIcons.call_end'
                                        tooltip 'Hangup'
                                        color '@c14'
                                    }
                                }
                                behaviours [
                                    GestureDetector
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    eventHandlers [
        {
            name 'On Init'
            block ```
                callDuration = '';
                durationStart = false;
            ```
        }
        {
            name 'OnVoiceMutePressed'
            type OnBehaviour
            on mutecall
            behaviour GestureDetector
            event onTap
            block ```
               if(client.isMuted){
                    Boolean unmute = client.unmuteCall(onSuccess: (e) {
                        isMute = false;
                    }, onFailure: (e, s) {
                        EventBus.get().fire(FailureMessage(message : e));
                    }).await;
                }else{
                    Boolean mute = client.muteCall(onSuccess: (e) {
                        isMute = true;
                    }, onFailure: (e, s) {
                        EventBus.get().fire(FailureMessage(message : e));
                    }).await;
                }
            ```
        }
        {
            name 'onDisconnectPressed'
            type OnBehaviour
            on endCall
            behaviour GestureDetector
            event onTap
            block ```
               Boolean disconnect = client.disconnectCall(onFailure: (e) {
                     onCallDisconnectError(e);
                 }).await;
                onCloseView();
            ```
        }
        {
            name 'onChangeCallId'
            block ```
                if(data != null && (data.callSid == null || data.callSid.isEmpty)){
                    onCloseView();
                }
                if (data != null && data.callStatus == InProgress && !durationStart) {
                    durationStart = true;
                    if (callInteraction.interaction.startTime == null) {
                        callInteraction.interaction.startTime = DateTime.now();
                    }
                    DateTime startTime = callInteraction.interaction.startTime;
                    Timer tmr = Timer.periodic(Duration(seconds: 1), (timer) {
                        // Calculate the duration
                        Duration duration = DateTime.now().difference(startTime);

                        Double totalInSeconds = duration.inSeconds.toDouble();
                        // Calculate hours, minutes, and seconds
                        Double hours = (totalInSeconds / 3600);
                        hours = hours.floorToDouble();

                        Double minutes = (totalInSeconds / 60);
                        minutes = minutes.floorToDouble();

                        Double seconds = totalInSeconds % 60;

                        // Convert minutes and seconds to strings
                        String minutesStr = minutes.toStringAsFixed(0);
                        String secondsStr = seconds.toStringAsFixed(0);

                        // Manually add leading zero if needed
                        if (minutesStr.length == 1) {
                            minutesStr = '0' + minutesStr;
                        }
                        if (secondsStr.length == 1) {
                            secondsStr = '0' + secondsStr;
                        }
                        // Format the call duration string
                        if (hours >= 1.0) {
                            // Show hours if the duration is 1 hour or more
                            callDuration = hours.toString() + ':' + minutesStr + ':' + secondsStr;
                        } else {
                            // Show only minutes and seconds
                            callDuration = minutesStr + ':' + secondsStr;
                        }
                    });
                }
            ```
        }
        {
            name 'onCallDisconnectError'
            params [
                {
                    name 'error'
                    type String
                }
            ]
            block ```
                EventBus.get().fire(FailureMessage(message : error));
            ```
        }
        {
            name 'onMinimizePressed'
            type OnEvent
            on minimize
            event onPressed
            block ```
                onMinimizeView();
            ```
        }
        {
            name 'OnAssignToLeadPressed'
            type OnEvent
            on assignToLeadButton
            event onPressed
            block ```
               showLeadAssignPopup();
            ```

        }
        {
            name 'onAddParticipantPressed'
            type OnEvent
            popup contactsView
            event onAddButtonPressed
            block ```
                String enteredNumber = TwilioClient.getPurifiedPhoneNumber(number);
                hideContactsView();
                if(interaction != null && !interaction.isConference){
                    Boolean isConference = RPCServices.getCallService().convertToConference(data.callSid, interaction.fromNumber, interaction.toNumber, enteredNumber).await;
                    if(isConference){
                       interaction.isConference = true;
                       interaction.participants.add(interaction.toNumber);
                       interaction.participants.add(enteredNumber);
                       EventBus.get().fire(SuccessMessage(message : 'Participant Added'));
                    }
                } else{
                    Boolean add = RPCServices.getCallService().addParticipant(interaction.fromNumber, interaction.toNumber, enteredNumber, (interaction.isIncoming ?  interaction.toNumber : interaction.fromNumber)).await;
                    if(add){
                        interaction.participants.add(enteredNumber);
                        EventBus.get().fire(SuccessMessage(message : 'Participant Added'));
                    }
                }
            ```
        }
        {
            name 'onConferenceCallPressed'
            type OnEvent
            on addParticipant
            event onPressed
            block ```
                showContactsView();
            ```
        }
    ]
    events [
        {
            name 'onCloseView'
            required true
        }
        {
            name 'onMinimizeView'
        }
    ]
    popups [
       {
            name 'LeadAssignPopup'
            component LeadAssignPopupView 
            data {
                interaction `callInteraction.interaction`
            }
        }
        {
            name 'ContactsView'
            component ContactsView
            target addParticipant
            side Top
            data {
                width '320'
                reportingManager `user.reportingManager`
            }
        }
    ]
}

```

## Structure
- Uses internal/external/computed properties
- Has event handlers and custom events
- May use slots and styles
- Supports two-way binding

## When to Use
- For widgets that require multiple interactive features and rich UI logic. 