# WhatsApp-like Chat Application API Documentation

## Create Chatroom
- Endpoint: `/chatroom/create/`
- Method: POST
- Description: Creates a new chat room.
- Request Body:
    - `name` (string): Name of the chat room.
    - `max_members` (integer): Maximum number of members allowed in the chat room.
- Response:
    - Status Code: 201 CREATED
    - Response Body: `{ 'message': 'Chat room created successfully' }`

## List Chatrooms
- Endpoint: `/chatroom/list/`
- Method: GET
- Description: Retrieves a list of all available chat rooms.
- Response:
    - Status Code: 200 OK
    - Response Body: List of chat rooms with their details.

## Leave Chatroom
- Endpoint: `/chatroom/leave/`
- Method: POST
- Description: Allows a user to leave a chat room.
- Request Body:
    - `user_id` (integer): ID of the user leaving the chat room.
    - `room_id` (integer): ID of the chat room.
- Response:
    - Status Code: 200 OK
    - Response Body: `{ 'message': 'User left the chat room' }`

## Enter Chatroom
- Endpoint: `/chatroom/enter/`
- Method: POST
- Description: Allows a user to enter/join a chat room.
- Request Body:
    - `user_id` (integer): ID of the user joining the chat room.
    - `room_id` (integer): ID of the chat room.
- Response:
    - Status Code: 200 OK
    - Response Body: `{ 'message': 'User joined the chat room' }`

## Send Message
- Endpoint: `/message/send/`
- Method: POST
- Description: Sends a message to a chat room.
- Request Body:
    - `user_id` (integer): ID of the user sending the message.
    - `room_id` (integer): ID of the chat room.
    - `message` (string): Text message content.
    - `attachment` (file): File attachment (optional).
- Response:
    - Status Code: 200 OK
    - Response Body: `{ 'message': 'Message sent successfully' }`

## List Messages
- Endpoint: `/message/list/`
- Method: GET
- Description: Retrieves a list of messages in a specific chat room.
- Request Parameter:
    - `room_id` (integer): ID of the chat room.
- Response:
    - Status Code: 200 OK
    - Response Body: List of messages with details.