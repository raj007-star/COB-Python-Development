import tkinter as tk
from tkinter import ttk
import socket
import threading

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            messages_list.insert(tk.END, message)
        except:
            break

# Function to send messages to the server
def send_message(event=None):
    message = message_entry.get()
    client_socket.send(message.encode())
    messages_list.insert(tk.END, "You: " + message)
    message_entry.delete(0, tk.END)

# Create the main application window
root = tk.Tk()
root.title("Chat Application")

# Create a styled frame
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a colorful, styled listbox for messages
messages_list = tk.Listbox(
    frame,
    height=15,
    width=50,
    bg='lightgrey',
    font=('Helvetica', 12),
    selectbackground='yellow',
)
messages_list.pack(side=tk.LEFT, padx=10, pady=10)

# Add a scrollbar to the listbox
scrollbar = ttk.Scrollbar(frame, command=messages_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
messages_list.config(yscrollcommand=scrollbar.set)

# Create an input field for typing messages
message_entry = tk.Entry(frame, width=50, font=('Helvetica', 12))
message_entry.bind("<Return>", send_message)
message_entry.pack(pady=10)

# Create a colorful and styled send button
send_button = ttk.Button(
    frame,
    text="Send",
    command=send_message,
    style="TButton",
)
send_button.pack()

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))  # Replace with your server's IP and port

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Configure the appearance of the send button
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), foreground="blue", background="lightblue")

# Configure the appearance of the frame
frame.configure(style="TFrame")
style.configure("TFrame", background="grey")

root.protocol("WM_DELETE_WINDOW", lambda: client_socket.close())
root.mainloop()
