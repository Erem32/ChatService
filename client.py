import socket
import threading

PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def talk_to_server(gui, nickname):
    """
    Starts a thread to receive messages from the server and sends the nickname as the first message.
    """
    thread = threading.Thread(target=receive_message, args=(client, gui))
    thread.start()
    send(nickname, nickname)  # Send the nickname as the first message

def send(nickname, msg):
    """
    Sends a message to the server with the nickname as prefix.
    """
    message = f"{nickname}: {msg}"
    message_encoded = message.encode(FORMAT)
    msg_length = len(message_encoded)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Padding to HEADER bytes
    client.send(send_length)
    client.send(message_encoded)

def receive_message(client_socket, gui):
    """
    Receives messages from the server and puts them into the GUI message queue.
    """
    connected = True
    while connected:
        msg_length = client_socket.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = client_socket.recv(msg_length).decode(FORMAT)
            gui.msg_queue.put(msg)
            print(f"{msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False

if __name__ == '__main__':
    # The GUI module handles login and further client communications
    from clientGUI import GUI
    g = GUI()
