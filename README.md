# Chatroom

This is a Python-based client-server chatroom application with support for text messaging, file sharing, and audio/video recording. The application provides a graphical user interface (GUI) for both server and client functionalities.

---

## Features
Real-time Chat: Live messaging between clients connected to the server.
File Sharing: Send and receive various file types such as images, videos, and documents.
Audio/Video Recording: Record audio or video directly from the app and share it in the chatroom.
User-Friendly GUI: Intuitive interface for ease of use.

---


## Technologies Used
Programming Language: Python
Libraries:
tkinter: For building the GUI.
socket: For enabling network communication.
threading: For handling multiple connections.
pyaudio and wave: For audio recording and playback.
opencv-python: For video recording.
keyboard and subprocess: For handling keyboard inputs and subprocess commands.

---


## Prerequisites
Please make sure that there are no import errors and all additional libraries are downloaded.
ffmpeg is used and must be added to the system variables path

---

## File Structure
main.py: it is the driving file that controls the application.
Server.py: Manages client connections, messages, and file broadcasting.
Client_chatroom.py: Handles client-side messaging, file sharing, and multimedia functionalities.
main_Client_connection.py: Sets up the client connection to the server and launches the chatroom.
