import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import socket
import threading
import traceback

import Client_chatroom  #the file for the second window

def on_button_click(): # Method to send the nickname to the server
    try:
        # get the three fields
        global name
        name = tf.get() # get the nickname from the text field

        global server_host
        global server_port
        server_host = tf2.get()
        temp = tf3.get()
        server_port = int(temp) 

        if name == '' or server_host == '': # check if the nickname or host ip is empty
            raise ValueError
    except ValueError as e: 
        messagebox.showerror("Error", "Please enter valid values") # show a warning message
    else:
        try:
            client.connect((server_host, server_port)) # connect client to Server
            client.send(name.encode('utf-8')) # send the nickname to the server
            root.destroy() # close the current window
            Client_chatroom.chat() # open the second window
        except:
            # print(traceback.format_exc())
            messagebox.showerror("Error", "Could not connect to the server")


def on_enter_click(event): # Method to send the nickname to the server
    try:
        # get the three fields
        global name
        name = tf.get() # get the nickname from the text field

        global server_host
        global server_port
        server_host = tf2.get()
        temp = tf3.get()
        server_port = int(temp) 

        if name == '' or server_host == '': # check if the nickname or host ip is empty
            raise ValueError
    except ValueError as e: 
        messagebox.showerror("Error", "Please enter valid values") # show a warning message
    else:
        try:
            client.connect((server_host, server_port)) # connect client to Server
            client.send(name.encode('utf-8')) # send the nickname to the server
            root.destroy() # close the current window
            Client_chatroom.chat() # open the second window
        except:
            # print(traceback.format_exc())
            messagebox.showerror("Error", "Could not connect to the server")



def main(): # Method to create the first window
    global root
    root = tk.Tk()  # Create a window named root
    root.title("WhatsApp")   # Title of the window
    root.geometry("650x550")    # Size of the window
    root.configure(bg='lightblue')

    # this configuration is to leave empty cells in the grid for proper alligning of the GUI elements
    root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    root.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
    root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
    root.grid_rowconfigure(2, weight=1)  # Allow row 2 to expand
    root.grid_rowconfigure(3, weight=1)  # Allow row 3 to expand



    # server_host = '192.168.1.6'
    # server_port = 60253

    global client   # global variable for the client socket to be accessed from the other methods
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 1st parameter for Server Address family (IPv4)   # 2nd parameter for type of transport (TCP)
    Client_chatroom.client = client

    # row for nickname
    label = tk.Label(root, text = "Nickname: ", font=("Arial", 12)) 
    label.grid(row=0, column=0, padx=50, pady=30, sticky="Nw") # sticky w to align the label to the left
    label.configure(bg='lightblue')
    
    global tf
    tf = tk.Entry(root, width=30, font=("Arial", 12), bd=2, relief="solid") 
    tf.grid(row=0, column=1, padx=0, pady=30, sticky="Nw") # sticky w to align the text field to the left
    tf.focus_set()  # Set the keyboard cursor to be initialized in the entry

    # row for server IP
    label2 = tk.Label(root, text = "Server IP address: ", font=("Arial", 12)) 
    label2.grid(row=1, column=0, padx=50, pady=0, sticky="Nw") # sticky w to align the label to the left
    label2.configure(bg='lightblue')
    
    global tf2
    tf2 = tk.Entry(root, width=30, font=("Arial", 12), bd=2, relief="solid") 
    tf2.grid(row=1, column=1, padx=0, pady=0, sticky="Nw") # sticky w to align the text field to the left

    # row for server port number
    label3 = tk.Label(root, text = "Port number: ", font=("Arial", 12)) 
    label3.grid(row=2, column=0, padx=50, pady=0, sticky="Nw") # sticky w to align the label to the left
    label3.configure(bg='lightblue')
    
    global tf3
    tf3 = tk.Entry(root, width=30, font=("Arial", 12), bd=2, relief="solid") 
    tf3.grid(row=2, column=1, padx=0, pady=0, sticky="Nw") # sticky w to align the text field to the left


    button = tk.Button(root, text="Connect", command=on_button_click, width=25, height=2, font=("Arial", 14,'bold'), bd=2, relief="raised", bg="#4CAF50", fg="white") # **Styled button with font, border, background color, and text color**
    button.grid(row=3, column=0,columnspan=2,sticky ="N") #columnspan to make the button span 2 columns

    root.bind('<Return>', on_enter_click)


    root.mainloop() # Run the main loop for the gui of the window
