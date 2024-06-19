import socket
from threading import Thread
from tkinter import *
from tkinter import ttk

clients = []

def broadcast_draw(message, current_client=None):
    for client in clients:
        if client != current_client:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def broadcast(message, current_client=None):
    for client in clients:
        if client != current_client:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            if message.startswith(b"DRAW"):
                broadcast_draw(message, client_socket)
            else:
                broadcast(message, client_socket)
            chat = Label(chatFrame, text=message.decode('utf-8'), fg='red', anchor='w')
            chat.pack(anchor='w', fill=X, pady=5, padx=10)
        except ConnectionResetError:
            break
    client_socket.close()

def start_server():
    global chatFrame
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    port = 55555

    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server IP Address: {host}")
    print("Server is listening...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Got a connection from {addr}")

        client_thread = Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def main():
    global Text_Entry, chatFrame

    root = Tk()
    root.title("Server")
    root.geometry("400x500")

    chatFrame = Frame(root)
    chatFrame.pack(fill=BOTH, expand=True)

    Text_Entry = Entry(root)
    Text_Entry.pack(fill=X, pady=10)

    root.mainloop()

server_thread = Thread(target=start_server)
server_thread.start()
main()
