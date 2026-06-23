# server.py
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

#bind and listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT)) #bind these 2 together
server.listen()

clients = {}  # socket -> username
lock = threading.Lock() #don't mess up

#broadcast function to notify others when a user leaves
def broadcast(message, exclude_client=None):
    with lock:
        dead_clients = [] 
        for client in clients:
            if client != exclude_client:
                try:
                    client.send(message.encode())
                except:
                    dead_clients.append(client)

        for client in dead_clients:
            remove_client(client) 

#function for removing client that types quit
def remove_client(client):
    username = clients.get(client)
    if username:
        try:
            del clients[client]
        except:
            pass
        try:
            client.close()
        except:
            pass

#get client username
def get_username(client):
    while True:
        client.send("USERNAME".encode())
        username = client.recv(1024).decode().strip()
        if not username:
            continue
        with lock:
            if username not in clients.values():
                clients[client] = username
                return username
        client.send("USERNAME_TAKEN".encode())


def handle_client(client):
    try:
        username = get_username(client) #receive the username
        print(f"{username} joined the chat") 
        broadcast(f"[SERVER] {username} has joined the chat.", exclude_client=client) #tells everyone a client has joined
        client.send(f"[SERVER] Welcome, {username}! Type QUIT to leave.".encode()) #welcome message

        while True:
            msg = client.recv(1024)
            if not msg: #in case client disconnects
                break

            text = msg.decode().strip()
            if text.upper() == "QUIT": #if client types quit
                break

            broadcast(f"{username}: {text}", exclude_client=client) 

    except:
        pass
    finally:
        with lock:
            username = clients.get(client, "Unknown")
        remove_client(client)
        print(f"{username} left the chat")
        broadcast(f"[SERVER] {username} has left the chat.")

#make sure to always accept / listen for new clients
def accept_clients():
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        print(f"Connected from {addr}")
        thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
        thread.start()


if __name__ == "__main__":
    accept_clients()