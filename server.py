import socket
import threading

# Dictionary to store clients' sockets and their corresponding names
clients = {}

# Log file to store the chat history
chat_log_file = 'chat_history.txt'

# Function to broadcast a message to all clients except the one specified
def broadcast(message, exclude_client=None):
    # Append the message to the chat history file
    with open(chat_log_file, 'a') as log_file:
        log_file.write(message + '\n')

    # Send the message to all clients except the excluded client
    for client, name in clients.items():
        if client != exclude_client:
            try:
                client.send(message.encode('utf-8'))
            except:
                # If there is an error sending the message, close the connection and remove the client from the list
                client.close()
                del clients[client]

# Function to handle each client connection
def handle_client(client_socket, client_address):
    # Prompt the client to enter their name
    client_socket.send("Enter your name: ".encode('utf-8'))
    name = client_socket.recv(1024).decode('utf-8')  # Receive the client's name
    welcome_message = f"{name} has joined the chat!"  # Message to broadcast when a client joins
    print(welcome_message)
    broadcast(welcome_message)  # Broadcast the welcome message

    # Store the client socket and name in the clients dictionary
    clients[client_socket] = name

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Receive a message from the client
            if not message:
                break  # If no message is received, break out of the loop
            full_message = f"{name}: {message}"  # Format the message with the client's name
            print(full_message)
            broadcast(full_message, client_socket)  # Broadcast the message to all other clients
        except:
            break  # In case of an error, break out of the loop

    # Message to broadcast when the client leaves
    goodbye_message = f"{name} has left the chat."
    print(goodbye_message)
    broadcast(goodbye_message)  # Broadcast the goodbye message
    client_socket.close()  # Close the client's connection
    del clients[client_socket]  # Remove the client from the clients dictionary

# Function to start the server
def start_server():
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the server to all interfaces on port 5555
    server.bind(('0.0.0.0', 5555))
    # Start listening for incoming connections
    server.listen(5)
    print("Server listening on port 5555")

    while True:
        # Accept incoming client connections
        client_socket, client_address = server.accept()
        # Start a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# Entry point to start the server when the script is executed
if __name__ == "__main__":
    start_server()
