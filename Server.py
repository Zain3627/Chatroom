import tkinter as tk
from tkinter import scrolledtext

import socket
import threading
import traceback
import time

messages = ''
current_person = ''

files_received = []
files_count = 1 # counter for the received files

def get_prv_messages():
    global messages
    return messages

def handle_client(client_socket): # Method to receive messages from that client and then broadcast them to all other clients
    
    broadcast2(client_socket) # send previous messages to the new client
    time.sleep(1)

    for file in files_received: #send all previous files to the new client
        
        thread = threading.Thread(target=broadcast_past_files, args=(client_socket, file), daemon=True)
        thread.start()
        thread.join()

    
    global messages
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8') # client will send up to 1024 bytes of data. # decode converts the  bytes into a string
            if message == "#fi_rn":  # code for receive of file with name method
                global file_name
                file_name = client_socket.recv(1024).decode('utf-8')                
                file_name = file_name.split('.')[-1]    # get the file extension
                file_name = f"{files_count}.{file_name}"    #append the counter to the extension
                
                receive_file(client_socket, file_name)
                files_received.append(file_name)    #put the file name in the received files

            elif message == "#v1_re":  # code for the end of a file
                pass
            else:
                update_log(f"Received message: {message} from {clients[client_socket]}")
                message = clients[client_socket] + ": " + message # add the nickname of the client to the message
                broadcast(message, client_socket) # method to send the message to all clients.
                messages += message + '\n'
        except: # if an error happens.
            #print(traceback.format_exc())
            update_log(f"Lost connection from {clients[client_socket]}") 
            broadcast(f"{clients[client_socket]} has left the chatroom", client_socket) # send a message to all clients that a client has left the chatroom
            messages += f"{clients[client_socket]} has left the chatroom" + '\n'
            del clients[client_socket] # remove client from the List
            client_socket.close() # End connection with client
            break

def receive_file(client_socket, filename): 
    global files_count
    files_count += 1
    with open(filename, 'wb') as f:  # creates a file to save the received data.
        while True:
            data = client_socket.recv(1024) # can receive up to 1024 bytes
            datacasted = str(data)
            if datacasted.find("#v1_re") != -1:
                data = data.replace(b"#v1_re", b"")
                f.write(data)
                break
            f.write(data) # Writes the received data (1024 bytes at a time) to the file filename="received_output.mp4" which is created in beginning of method.
            
    update_log(f"File '{filename}' received from {clients[client_socket]}.")
    global messages
    messages += f"File '{filename}' received from {clients[client_socket]}.\n"
    broadcast_file(client_socket,filename)

def broadcast_file(client_socket,file_path):
    broadcast(f'{clients[client_socket]} is sending file {file_path}', client_socket) # send a message to all clients that a client has sent a file
    for client in clients:
        if client != client_socket: # To not send the file to the client who is sending the file.
            start_signal = "#fi_rn"+file_path 
            client.send(start_signal.encode('utf-8')) # code for initiating sending a file
            time.sleep(0.5)            
            # client.send("#fi_En".encode('utf-8')) # code for ending name of a file
            with open(file_path, 'rb') as f: # Open the specified file in read-binary mode
                while chunk := f.read(1024):# Continuously read the file in segements of 1024 bytes  # Read and send file in segements(chunks).
                    client.sendall(chunk)  # Send each segement(chunk) to the server
            client.send("#v1_re".encode('utf-8'))
            # client.send(file_path.encode('utf-8')) # send the file name to the client

def broadcast2(sender_socket):  # Method to send previous messages to the new client
    global messages
    global current_person
    messages += current_person + " has joined to the chatroom"
    sender_socket.send(messages.encode('utf-8'))
    messages += '\n'

def broadcast_past_files(sender_socket,file):  # Method to send previous files to the new client
    
        start_signal = "#fi_rn"+file
        sender_socket.send(start_signal.encode('utf-8')) # code for initiating sending a file
        time.sleep(0.5)            
        with open(file, 'rb') as f: # Open the specified file in read-binary mode
            while chunk := f.read(1024):# Continuously read the file in segements of 1024 bytes  # Read and send file in segements(chunks).
                sender_socket.sendall(chunk)  # Send each segement(chunk) to the server
        sender_socket.send("#v1_re".encode('utf-8'))

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket: # To not send the messege to the client who is sending the message.
            client.send(message.encode('utf-8')) # convert the messege from string to bytes by encode method.

def update_log(message): # Method to update the log_area with the message
    log_area.config(state='normal') # allow the user to write in the log_area
    log_area.insert(tk.END, message + '\n') # insert the message at the end of the log_area
    log_area.see(tk.END) # scroll to the end of the log_area
    log_area.config(state='disabled') # prevent the user from writing in the log_area

def accept_connections():   # Accept new connections and create a new thread to handle each connection
    global current_person
    while True:
        client_socket, client_address = server.accept() # wait for incoming connection and accept it.
        nickname = client_socket.recv(1024).decode('utf-8') # recieve the nickname from the client\

        update_log(f"New connection from {nickname}")
        current_person = nickname

        # thread = threading.Thread(target=broadcast2, args=(client_socket,), daemon=True) # create a thread to send previous messages to the new client
        # thread.start()
        
        
        broadcast(f"{nickname} has joined the chatroom", client_socket) # send a message to all clients that a new client has joined the chatroom
        clients[client_socket] = nickname # Add the client socket to the Clients list.
        thread = threading.Thread(target=handle_client, args=(client_socket,),daemon=True)  # daemon=True to end the thread when the main thread ends
        thread.start()


def main():

    host_name = socket.gethostname() # Get the hostname of the server
    server_host = socket.gethostbyname(host_name) # Get the IP address of the server from the name

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:  #creates temp sockets and see whether it is closed or not
        temp_socket.bind(('0.0.0.0', 0))  # Bind to any available port
        _, server_port = temp_socket.getsockname()  # Get the assigned port number and leave the ip returned unsigned


    root = tk.Tk()  # Create a window named root
    root.title("Chatroom Server")   # Title of the window
    root.geometry("550x400")    # Size of the window
    root.configure(bg='lightblue')


    global log_area
    log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=70, font=("Arial", 10), bd=2, relief="sunken")    # Create a vertical text widget # wrap=tk.WORD to wrap the text by words into new lines # bd is the border width # relief is the type of the border
    log_area.pack(padx=20, pady=20)  # Add padding to the log area
    log_area.config(state='disabled')   # Prevents user from writting in the log_area

    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 1st parameter for client Address    # 2nd parameter for type of transport (TCP)
    server.bind((server_host, server_port)) # Bind Server Port to Server Socket
    server.listen(20) # server listen for TCP connection requests from the client     # Maximum 20 clients in queue.
    global clients
    clients = {}    # map to store the client sockets and nicknames


    update_log(f"Server running on IP: {server_host} with port:{server_port}")

    thread = threading.Thread(target=accept_connections,daemon=True)    # Additional thread for accepting connections in order not to block the gui mainloop
    thread.start()

    root.mainloop() # Run the main loop for the gui of the window

