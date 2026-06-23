# client.py
import socket
import threading

#create tcp connection
HOST = "127.0.0.1"
PORT = 5000

#connect to the same host and port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

#function for getting messages
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode() #input message

            #input username
            if message == "USERNAME":
                username = input("Enter username: ").strip()
                client.send(username.encode())
                

            #rejected username
            elif message == "USERNAME_TAKEN":
                print("Username already exists. Try another one.")
            
            #display normal message
            else:
                print(message)
        #in case of failure, close client connection
        except:
            print("Disconnected from server.")
            client.close()
            break

#function for sending messages to the server
def send_messages():
    while True: #run forever

        try:
            message = input()
            client.send(message.encode()) #send the message to server
            if message.strip().upper() == "QUIT": #if you type quit, close client connection
                client.close()
                break
        except:
            break

#threads to send and receive
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

send_thread = threading.Thread(target=send_messages, daemon=True)
send_thread.start()

send_thread.join() #keep program running 