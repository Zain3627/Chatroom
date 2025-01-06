import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import PhotoImage

import socket
import threading
import pyaudio
import wave
import subprocess

import keyboard



import main_Client_connection  #the file for the first window
import cv2  # OpenCV library for video recording and processing.


global connection_running   # global flag to check if the connection is running
connection_running = True

global client   # global socket imported from the client_connection file

def on_snd_button_click(): # Method to send a message to the server
    global message_send
    message_send = tf.get() # get the message from the text field
    if message_send != '':    
        tf.delete(0, tk.END) # clear the text field
        update_chat(f"You: {message_send}") # update the log_area with the message
        
        thread2 = threading.Thread(target=send_messages,daemon=True)
        thread2.start()

def on_enter_click(event): # Method to send a message to the server
    global message_send
    message_send = tf.get() # get the message from the text field
    if message_send != '':    
        tf.delete(0, tk.END) # clear the text field
        update_chat(f"You: {message_send}") # update the log_area with the message
        
        thread2 = threading.Thread(target=send_messages,daemon=True)
        thread2.start()


def send_messages(): # method to send message to the server
    client.send(message_send.encode('utf-8')) # send method and turn it from string to bytes


def receive_messages():# function to recieve the m  essages from the server
    while True:
        global connection_running
        try:
            rec_message = client.recv(1024).decode('utf-8') # client can recieve a messiage up to 1024 bytes  # decode method turn from bytes to string
            if rec_message.find("#fi_rn") != -1 :  # code for file
                file_name = rec_message.split('#fi_rn')[-1]


                thread3 = threading.Thread(target=receive_file,args =(file_name,), daemon=True)
                thread3.start()
                thread3.join()
                
            elif rec_message.find("#v1_re") != -1 : # code for termmination of a file
                pass
            else:
                update_chat(rec_message)
        except Exception as e: # if error occurs
            print(e)
            connection_running = False
            client.close() #close the connection
            messagebox.showerror("Error", "You have lost connection")
            on_quit_button_click() # exit the window
            break

def update_chat(message): # Method to update the chat_area with the message
    chat_area.config(state='normal') # allow the user to write in the chat_area
    chat_area.insert(tk.END, message + '\n') # insert the message at the end of the chat_area
    chat_area.see(tk.END) # scroll to the end of the chat_area
    chat_area.config(state='disabled') # prevent the user from writing in the chat_area

def on_quit_button_click(): # Method to quit the window
    global connection_running
    if connection_running:
        client.close() # close the connection
        connection_running = False
    
    root.destroy() # exit the window
    main_Client_connection.main() # return to the connection window

def on_attach_button_click(): 
    global root2
    root2 = tk.Toplevel(root)  # Create a new window named root2
    root2.title("Attach a document")   # Title of the window
    root2.geometry("600x400")    # Size of the window
    root2.configure(bg='lightblue')

    # this configuration is to leave empty cells in the grid for proper alligning of the GUI elements
    root2.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    root2.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
    root2.grid_columnconfigure(2, weight=1)  # Allow column 2 to expand

    root2.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root2.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
    root2.grid_rowconfigure(2, weight=1)  # Allow row 2 to expand

    selected_option = tk.StringVar(value="Choose the file type")  # Default value of the option menu
    options = ["Image","Voice","Video","Upload"] # Write the options in the option menu

    option_menu = tk.OptionMenu(root2, selected_option, *options,command=option_change) # Create the option menu

    option_menu.grid(row=0, column=1,pady=20) # Add the option menu to the window
    option_menu.config(width=30, font=("Arial", 12),bg="#f44336", fg="white")


def option_change(*args):    #   Method to be done upon selecting an item from the option menu
    global root2
    # Clear existing widgets in root2
    for widget in root2.winfo_children():
        widget.destroy()

    # Recreate the option menu
    selected_option = tk.StringVar(value=args[0])
    options = ["Image","Voice","Video","Upload"]
    option_menu = tk.OptionMenu(root2, selected_option, *options, command=option_change)
    option_menu.grid(row=0, column=1, pady=20)
    option_menu.config(width=30, font=("Arial", 12), bg="#f44336", fg="white")

    if args[0] == "Video":
        rec_button = tk.Button(root2, text="Record", command=record_video, width=10, height=3, font=("Arial", 12, "bold"), bd=2, relief="raised", bg="#4CAF50", fg="white")
        rec_button.grid(row=2, column=1)
        label = tk.Label(root2, text="After starting the record press 'q' to stop it or 'esc' to cancel it", font=("Arial", 12, "italic"), fg="red")
        label.grid(row=1, column=1)

    elif args[0] == "Image":
        label = tk.Label(root2, text="press 'q' to capture the image", font=("Arial", 12, "italic"), fg="red")
        label.grid(row=1, column=1)
        capture_button = tk.Button(root2, text="Open camera", command=capture_image, width=10, height=3, font=("Arial", 12, "bold"), bd=2, relief="raised", bg="#4CAF50", fg="white")
        capture_button.grid(row=2, column=1)

    elif args[0] == "Voice":
        label = tk.Label(root2, text="After starting the record press 'q' to stop it or 'esc' to cancel it", font=("Arial", 12, "italic"), fg="red")
        label.grid(row=1, column=1)
        rec_button = tk.Button(root2, text="Record", command=record_voice, width=10, height=3, font=("Arial", 12, "bold"), bd=2, relief="raised", bg="#4CAF50", fg="white")
        rec_button.grid(row=2, column=1)


    elif args[0] == "Upload":
        label = tk.Label(root2, text="Path: ", font=("Arial", 12, "italic"), fg="red")
        label.grid(row=1, column=0,padx=10)

        global file_path_entry
        file_path_entry = tk.Entry(root2, width=40, font=("Arial", 12), bd=2, relief="solid")
        file_path_entry.grid(row=1, column=1, pady=20)

        upload_button = tk.Button(root2, text="Upload", command=on_upload_button_click, width=10, height=3, font=("Arial", 12, "bold"), bd=2, relief="raised", bg="#4CAF50", fg="white")
        upload_button.grid(row=2, column=1)


def record_voice(output_filename="output.wav", chunk=1024, channels=1, rate=44100):

    is_recording = True
    is_bad_recording = False

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []

    while is_recording:
 
        data = stream.read(chunk)
        frames.append(data)
        if keyboard.is_pressed('q'):
            is_recording = False
        if keyboard.is_pressed('esc'):
            is_recording = False
            is_bad_recording = True

    stream.stop_stream()
    stream.close()
    p.terminate()

    if is_bad_recording:
        return

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))    

    root2.destroy()  # close the current window

    global message_send
    message_send = "#fi_rn"  # Send this code to tell the server to receive a file and a name method
    
    thread2 = threading.Thread(target=send_messages,daemon=True)
    thread2.start()
    thread2.join()  # wait for the type of the file to be sent

    message_send = "1"+ output_filename
    thread2 = threading.Thread(target=send_messages,daemon=True)
    thread2.start() #send the file name
    thread2.join() 

    thread2= threading.Thread(target=send_file, args=(output_filename,),daemon=True)
    thread2.start()


def on_upload_button_click():
        global file_path_entry
        file_path = file_path_entry.get().split('\\')[-1]  # Extract only the file name from the full path
        full_path = file_path_entry.get()

        global message_send
        message_send = "#fi_rn"  # Send this code to tell the server to receive a file and a name method
    
        thread2 = threading.Thread(target=send_messages,daemon=True)
        thread2.start()
        thread2.join()  # wait for the type of the file to be sent

        message_send = file_path
        thread2 = threading.Thread(target=send_messages,daemon=True)
        thread2.start() #send the file name
        thread2.join() 

        thread2= threading.Thread(target=send_file, args=(full_path,),daemon=True)
        thread2.start()

        root2.destroy()

def record_video(output_filename="output.mp4", fps=20.0): 

    cam = cv2.VideoCapture(0) #open the deafult camera,   0=> refer to deafult camera If you have multiple cameras you can specify other cameras (0,1,2) to select different cameras.

    # Get the default frame width and height it adjust on camera height and width.
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # make format of video mp4v and # * to unpack mp4v into 'm' 'p; 'v' '4' as function works like this.
    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height)) # create the output video file object video recorded.

    #initializing recording audio
    p = pyaudio.PyAudio()
    audio_filename = "audio.wav"
    audio_stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    def rec_audio_only_without_sending():
        frames = []
        while is_recording:
            data = audio_stream.read(1024)
            frames.append(data)
        with wave.open(audio_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))

    global is_recording 
    is_recording = True
    audio_thread = threading.Thread(target=rec_audio_only_without_sending)
    audio_thread.start()    # start separate thread for recording audio

    try:
        while True:
            recorded = False    # flag to check if the video is recorded

            ret, frame = cam.read()  # camera takes two thing ret and frame. ret => Boolean to know if camera captured the frame or not it returns true and false 
            if not ret:  # If frame capture fails, break
                break

            # Write the frame to the output file
            out.write(frame)

            # Display the captured frame
            cv2.imshow('Camera', frame)

            

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                is_recording = False
                recorded = True
                break

            if cv2.waitKey(1) & 0xFF == 27:    #ASCII code for exc button
                is_recording = False
                break

            elif cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1: # close camera if window is closed
                is_recording = False
                break

    finally:
        is_recording = False
        audio_thread.join()
        # Release resources
        cam.release()
        out.release()
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        cv2.destroyAllWindows()

    merged_name = f"merged{output_filename}"
    merge_command = f"ffmpeg -y -i {output_filename} -i {audio_filename} -c:v libx264 -c:a aac {merged_name}"
    subprocess.run(merge_command, shell=True)

    if not recorded:
        return  # stop executing if the video isn't recorded
    
    root2.destroy()  # close the current window
    
    global message_send
    message_send = "#fi_rn"  # Send this code to tell the server to receive a file
    
    thread2 = threading.Thread(target=send_messages,daemon=True)
    thread2.start()
    thread2.join()  # wait for the type of the file to be sent

    message_send = merged_name
    thread2 = threading.Thread(target=send_messages,daemon=True)
    thread2.start() #send the file name
    thread2.join() 


    thread2= threading.Thread(target=send_file, args=(merged_name,),daemon=True)
    thread2.start()

def capture_image(output_filename="image.png"):
    captured = False # flag to check if the image is captured
    cam = cv2.VideoCapture(0)   # open the default camera

    while True:
        ret, frame = cam.read() # captures a frame
        if not ret:
            break
        
        cv2.imshow("Camera", frame) # display the live frame

        if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to capture the image and exit the loop
            cv2.imwrite(output_filename, frame)
            captured = True
            break
        elif cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1: # close camera if window is closed
            break

    # release all sources
    cam.release()
    cv2.destroyAllWindows()

    root2.destroy()  # close the current window
    if not captured:
        return # stop executing if the image isn't captured
    
    global message_send
    message_send = "#fi_rn"  # Send this code to tell the server to receive a file    

    thread2 = threading.Thread(target=send_messages, daemon=True)
    thread2.start()
    thread2.join()  # wait for the type of the file to be sent

    message_send = output_filename
    thread2 = threading.Thread(target=send_messages,daemon=True)
    thread2.start() #send the file name
    thread2.join() 

    thread2 = threading.Thread(target=send_file, args=(output_filename,), daemon=True)
    thread2.start()






def send_file(file_path):

    with open(file_path, 'rb') as f: # Open the specified file in read-binary mode
        while chunk := f.read(1024):# Continuously read the file in segements of 1024 bytes  # Read and send file in segements(chunks).
            client.sendall(chunk)  # Send each segment(chunk) to the server

    global message_send
    message_send = "#v1_re"  # Send this code to tell the server that the file has been sent 
    send_messages()
    
    # Update the chat window to notify the user that the file has been sent
    update_chat(f"Sent file '{file_path}'")  # Notify user in chat.

def receive_file(file_name):
   
    
    with open(file_name, 'wb') as f:  # creates a file to save the received data.
        while True:
            data = client.recv(1024) # can receive up to 1024 bytes
            datacasted = str(data)
            if datacasted.find("#v1_re") != -1:
                data = data.replace(b"#v1_re", b"")
                f.write(data)
                break
            f.write(data) # Writes the received data (1024 bytes at a time) to the file filename="received_output.mp4" which is created in beginning of method.

    update_chat(f"Received file '{file_name}'")  # Notify user in chat.


def chat(): # Method to create the chatroom window
    global root
    global connection_running
    global greated
    connection_running = True   # set the connection to running

    root = tk.Tk()  # Create a window named root
    root.title(f"{main_Client_connection.name} Chatroom")   # Title of the window
    root.geometry("700x700")    # Size of the window
    root.configure(bg='lightblue')

    # this configuration is to leave empty cells in the grid for proper alligning of the GUI elements
    root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
    root.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
    root.grid_columnconfigure(2, weight=1)  # Allow column 2 to expand
    root.grid_columnconfigure(3, weight=1)  # Allow column 3 to expand
    root.grid_columnconfigure(4, weight=1)  # Allow column 4 to expand



    root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
    root.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
    root.grid_rowconfigure(2, weight=100)  # Allow row 2 to expand
    root.grid_rowconfigure(3, weight=100)  # Allow row 3 to expand


    global chat_area
    chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80,font=("Arial", 10), bd=2, relief="solid")   # Create a vertical text widget # wrap=tk.WORD to wrap the text by words into new lines
    chat_area.grid(row=1, column=0,columnspan=5,padx=10,sticky="EW")  
    chat_area.config(state='disabled')   # Prevents user from writting in the chat_area


    global tf
    tf = tk.Entry(root, width=40, font=("Arial", 12), bd=2, relief="solid") # Text field to enter the message
    tf.grid(row=2, column=1,columnspan=3,sticky="W") # Add the text field to the window
    tf.focus_set()  # Set the keyboard cursor to be initialized in the entry

    label1 = tk.Label(root, text = "Write a message: ",font=("Arial", 12, "bold")) # Label to ask the user to enter their nickname
    label1.grid(row=2, column=0,sticky="W",padx=10) # Add the label to the window
    label1.configure(bg='lightblue')

    snd_button = tk.Button(root, text="Send",command=on_snd_button_click, width=30,height=3,font=("Arial", 12, "bold"), bd=2, relief="raised", bg="#4CAF50", fg="white") # Button to send a message
    snd_button.grid(row=3,column=1, sticky="W") # Add the button to the window

    leave_icon = tk.PhotoImage(file = "leave_icon_mirror-transformed.png")
    quit_button = tk.Button(root, image=leave_icon,command=on_quit_button_click, width=50, height=50, font=("Arial", 12, "bold"), bd=2, relief="raised") # Button to quit the window
    quit_button.grid(row=0,column=0,sticky="W",padx=10) # Add the button to the window


    attach_icon = PhotoImage(file="attach.png") # create an object of the PhotoImage class and pass the its path
    attach_button = tk.Button(root, image=attach_icon,command=on_attach_button_click,width=30,height=30, bd=2, relief="raised",bg="#FFFFFF") # Button to attach an image
    attach_button.grid(row=2,column=3,sticky="E",padx=10 ) # Add the button to the window    

    root.bind('<Return>', on_enter_click)
    
    thread1 = threading.Thread(target=receive_messages,daemon=True) # daemon=True to end the thread when the main thread ends
    thread1.start()


    root.mainloop() # Run the main loop for the gui of the window
