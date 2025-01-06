import main_Client_connection
import Server
import tkinter as tk

def join():
    root.destroy()
    main_Client_connection.main()

def host():
    root.destroy()
    Server.main()

    
global root
root = tk.Tk()  # Create a window named root
root.title("WhatsApp")   # Title of the window
root.geometry("550x400")    # Size of the window
root.configure(bg='lightblue')

# this configuration is to leave empty cells in the grid for proper alligning of the GUI elements
root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand
root.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand
root.grid_columnconfigure(2, weight=1)  # Allow column 1 to expand
root.grid_columnconfigure(3, weight=1)  # Allow column 1 to expand

root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
root.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
root.grid_rowconfigure(2, weight=1)  # Allow row 1 to expand

label = tk.Label(root, text = "Welcome", font=("Arial", 24,'bold')) 
label.grid(row=0, column=1,columnspan=2, padx=30,pady=20)
label.configure(bg='lightblue')

button1 = tk.Button(root, text="Host room", command=host, width=10, height=2, font=("Arial", 14,'bold'), bd=2, relief="raised", bg="#4CAF50", fg="white") # **Styled button with font, border, background color, and text color**
button1.grid(row=1, column=1) #columnspan to make the button span 2 columns

button2 = tk.Button(root, text="Join room", command=join, width=10, height=2, font=("Arial", 14,'bold'), bd=2, relief="raised", bg="#4CAF50", fg="white") # **Styled button with font, border, background color, and text color**
button2.grid(row=1, column=2) #columnspan to make the button span 2 columns


root.mainloop() # Run the main loop for the gui of the window

