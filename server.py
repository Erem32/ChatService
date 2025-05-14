import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_sockets = []
chat_history = []

# Locks for synchronizing access to shared resources
client_sockets_lock = threading.Lock()
chat_history_lock = threading.Lock()

def receive_message(client_socket, addr):
    """Handles messages from a connected client."""
    print(f"[NEW CONNECTION] {addr} connected.")

    # The first message from client is taken as the nickname
    msg_length = client_socket.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        nickname = client_socket.recv(msg_length).decode(FORMAT)
    
    print(f"[NICKNAME] {addr} is now known as {nickname}.")

    # Send existing chat history to the newly connected client
    with chat_history_lock:
        for hist_msg in chat_history:
            message = hist_msg.encode(FORMAT)
            message_length = len(message)
            send_length = str(message_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client_socket.send(send_length)
            client_socket.send(message)

    connected = True
    while connected:
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length)
            msg = client_socket.recv(msg_length).decode(FORMAT)
            print(f"[{nickname} {addr}]: {msg}")
            
            # If not a disconnect message, add to chat history
            if msg != DISCONNECT_MESSAGE:
                with chat_history_lock:
                    chat_history.append(msg)
            
            send_messages_to_clients(msg)

            if msg == DISCONNECT_MESSAGE:
                connected = False
        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False

    # Remove client from the list under lock and close the socket
    with client_sockets_lock:
        if client_socket in client_sockets:
            client_sockets.remove(client_socket)
    client_socket.close()

def send_messages_to_clients(msg):
    """Broadcasts the message to all connected clients."""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # Copy the client list under lock
    with client_sockets_lock:
        clients_copy = client_sockets.copy()
    for client_socket in clients_copy:
        try:
            client_socket.send(send_length)
            client_socket.send(message)
        except Exception as e:
            print(f"[SEND ERROR] {e}")
            with client_sockets_lock:
                if client_socket in client_sockets:
                    client_sockets.remove(client_socket)

def start():
    """Starts the server and listens for incoming connections."""
    print("[SERVER IS STARTING]")
    server.listen()
    while True:
        client_socket, addr = server.accept()
        # Add new client to the list with synchronization
        with client_sockets_lock:
            client_sockets.append(client_socket)
        thread = threading.Thread(target=receive_message, args=(client_socket, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == '__main__':
    start()
