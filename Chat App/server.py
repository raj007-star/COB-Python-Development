import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)

print("Server is listening...")

clients = []

def handle_client(client_socket):
    username = f"user {len(clients) + 1}"
    clients.append(client_socket)

    # Broadcast a message to inform all clients about the new user
    broadcast(f"{username} has joined the chat.")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                clients.remove(client_socket)
                client_socket.close()
                broadcast(f"{username} has left the chat.")
                break
            broadcast(f"{username}: {message}")
        except:
            pass

def broadcast(message):
    for client in clients:
        client.send(message.encode())

while True:
    client_socket, addr = server_socket.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
