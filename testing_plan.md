# Testing Plan

## Overview
This testing plan focuses on **automated testing** of the critical functionalities of the **DjangoChatroom** application to ensure reliability, performance, and security.

## Critical Functionalities to Test

### 1. User Registration and Authentication
- **Register New User**
  - **Test Case:** Register with valid credentials.
  - **Expected Outcome:** User is successfully registered, receives a confirmation message, and can log in with the provided credentials.
  - **Tools:** Django Test Framework, Postman.

- **Register New User with Invalid Credentials**
  - **Test Case:** Attempt to register with missing or invalid fields (e.g., invalid email format).
  - **Expected Outcome:** Registration fails with appropriate error messages indicating the invalid fields.
  - **Tools:** Django Test Framework, Postman.

- **Register New User with Valid Name and Invalid Password**
  - **Test Case:** Register using a valid username but an invalid password (e.g., too short, no special characters).
  - **Expected Outcome:** Registration fails with error messages specifying password requirements.
  - **Tools:** Django Test Framework, Postman.

- **Login User**
  - **Test Case:** Login with correct and incorrect credentials.
  - **Expected Outcome:** 
    - With correct credentials: User is authenticated and redirected to the chatroom list.
    - With incorrect credentials: Login fails with an authentication error message.
  - **Tools:** Django Test Framework, Postman.

- **Logout Functionality**
  - **Test Case:** Ensure users can logout successfully.
  - **Expected Outcome:** User session is terminated, and the user is redirected to the login page.
  - **Tools:** Django Test Framework.

### 2. Chatroom Management
- **Create Chatroom**
  - **Test Case:** Create a chatroom with a unique name.
  - **Expected Outcome:** Chatroom is successfully created, appears in the chatroom list, and the creator is added as a member.
  - **Tools:** Django Test Framework, Jest (Frontend).

- **Create Chatroom with Invalid Details**
  - **Test Case:** Attempt to create a chatroom with invalid details (e.g., empty name, name exceeding character limit).
  - **Expected Outcome:** Chatroom creation fails with appropriate error messages.
  - **Tools:** Django Test Framework, Jest (Frontend).

- **View Chatrooms**
  - **Test Case:** Retrieve and display a list of existing chatrooms.
  - **Expected Outcome:** All existing chatrooms are listed with correct details visible to the user.
  - **Tools:** Django Test Framework, Jest (Frontend).

- **Join Chatroom**
  - **Test Case:** Join an existing chatroom.
  - **Expected Outcome:** User is successfully added to the chatroom's member list and can participate in messaging.
  - **Tools:** Django Test Framework

- **View Only Joined Chatrooms**
  - **Test Case:** Ensure that only chatrooms the user is a member of are displayed or accessible.
  - **Expected Outcome:** User can only see and access chatrooms they have joined; other chatrooms are hidden or inaccessible.
  - **Tools:** Django Test Framework, Jest (Frontend).

### 3. User Invitations
- **Send Invitation**
  - **Test Case:** Invite another user to a chatroom.
  - **Expected Outcome:** Invitation is sent successfully, and the recipient receives a notification.
  - **Tools:** Django Test Framework, Postman.

- **Send Invitation to Yourself**
  - **Test Case:** Attempt to invite oneself to a chatroom.
  - **Expected Outcome:** Invitation fails with an error message indicating that a user cannot invite themselves.
  - **Tools:** Django Test Framework, Postman.

- **Send Invitation to Someone Already in the Chatroom**
  - **Test Case:** Invite a user who is already a member of the chatroom.
  - **Expected Outcome:** Invitation fails with an error message stating that the user is already a member.
  - **Tools:** Django Test Framework, Postman.

- **Send Invitation to a Non-Existent User**
  - **Test Case:** Invite a user that does not exist in the system.
  - **Expected Outcome:** Invitation fails with an error message indicating that the user does not exist.
  - **Tools:** Django Test Framework, Postman.

- **Accept Invitation**
  - **Test Case:** Accept an invitation and join the chatroom.
  - **Expected Outcome:** Invitation status updates to accepted, and the user is added to the chatroom's member list.
  - **Tools:** Django Test Framework, Cypress (End-to-End).

- **Decline Invitation**
  - **Test Case:** Decline an invitation.
  - **Expected Outcome:** Invitation status updates to declined, and the user is not added to the chatroom.
  - **Tools:** Django Test Framework, Cypress (End-to-End).

### 4. Real-Time Messaging
- **Send Message**
  - **Test Case:** Send a text message within a chatroom.
  - **Expected Outcome:** Message is sent successfully, appears in the chat interface immediately, and is visible to all chatroom members.
  - **Tools:** Django Channels Tests, Jest (Frontend), Cypress (End-to-End).

- **Receive Message**
  - **Test Case:** Receive messages in real-time without page refresh.
  - **Expected Outcome:** Incoming messages appear instantly in the chat interface without the need to refresh the page.
  - **Tools:** Django Channels Tests, Jest (Frontend), Cypress (End-to-End).

### 5. Members List
- **View Members**
  - **Test Case:** Display the list of members in a chatroom.
  - **Expected Outcome:** All current members of the chatroom are listed accurately and update in real-time as members join or leave.
  - **Tools:** Django Test Framework, Jest (Frontend).

## Automated Testing Tools

### Backend
- **Django Test Framework**
  - **Usage:** Unit and integration tests for models, views, and APIs.


### Frontend
- **Jest**
  - **Usage:** Unit testing for React components.

### Real-Time Communication
- **Django Channels Tests**
  - **Usage:** Test WebSocket connections and real-time message broadcasting.

# Testing commands
- **Run Django Backend Tests:**
```
python manage.py test
```
