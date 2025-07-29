import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "Enter your name: ":
                # Avoid printing the name prompt twice
                print(message, end='', flush=True)
            else:
                print(message)
        except:
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    # Start the thread to listen for messages from the server
    threading.Thread(target=receive_messages, args=(client,)).start()

    # Input for the name
    name = input()  # This handles the user input without extra print
    client.send(name.encode('utf-8'))

    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client.send(message.encode('utf-8'))
    
    client.close()

if __name__ == "__main__":
    start_client()
