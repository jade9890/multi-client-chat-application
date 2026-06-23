# multi-client-chat-application


##requirements:

support multiple clients concurrently
python threading 
ask for a unique username
server should notify others
leaves with quit 

##how it works

the client: 

Connects to the server on localhost:5000
Uses threading for sending and receiving
Handles server disconnection with quit


the server:
Listens on port 5000
Handles multiple client connections
Broadcasts messages to connected clients
Manages client disconnections 

##error handling
messages for common errors
handles random disconnections