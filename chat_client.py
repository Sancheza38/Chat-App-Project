import threading
from tkinter import *
from tkinter import simpledialog
from tkinter import font
from tkinter import ttk

import grpc

import chat_pb2_grpc
import chat_pb2
import time

import sys
#--------global-------
address_port = 'localhost:5000'

class Client:

    def __init__(self, user: str, window):
        #frame to put ui components on
        self.window = window
        self.username = user
        #create a gRPC channel + stub
        channel = grpc.insecure_channel(address_port)
        self.conn = chat_pb2_grpc.ChatServiceStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """
        Will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """

        self.joined = False

        if not self.joined:
                n = chat_pb2.ChatMessage()  # create protobug message (called Note)
                n.time = time.strftime("%H:%M:%S",time.localtime()) # set the time of message
                n.fromUser = "CHAT UPDATE"
                n.msg = self.username + " has entered the chat!"
                print("S[{}] <{}> {}".format(n.time, n.fromUser, n.msg))  # debugging statement
                self.conn.sendMsg(n)  # send the Note to the server
                self.joined= True

        for note in self.conn.receiveMsg(chat_pb2.Empty()):  # this line will wait for new messages from the server!
            
            print("R[{}] <{}> {}".format(note.time, note.fromUser, note.msg))  # debugging statement
            print()
            self.chat_list.insert(END, "[{}] <{}> {}\n".format(note.time, note.fromUser, note.msg))  # add the message to the UI

    def send_message(self, event):
        """
        Called when user enters something into the textbox
        """
        message = self.entry_message.get()  # retrieve message from the UI
        empty = ''
        if message != empty:
            n = chat_pb2.ChatMessage()  # create protobug message (called Note)
            n.time = time.strftime("%H:%M:%S",time.localtime()) # set the time of message
            n.fromUser = self.username  # set the username
            n.msg = message  # set the actual message of the note
            print("S[{}] <{}> {}".format(n.time, n.fromUser, n.msg))  # debugging statement
            self.conn.sendMsg(n)  # send the Note to the server
            self.entry_message.delete(0, END)

    # Creates the GUI for the chatroom using tkinter toolkit.
    def __setup_ui(self):
        # creates the chat list where user messages are displayed
        self.chat_list = Text(self.window, background="black", foreground="white")
        self.chat_list.grid(row=0, column=0, columnspan=5)

        # creates the username label and sets it to the name of the current user.
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.grid(row=1, column=0, columnspan=1, sticky=E)

        # creates the message textbox used by the user to enter a message.
        self.entry_message = Entry(self.window, foreground="black", bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.grid(row=1, column=1, columnspan=4, sticky=EW)

if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.grid()
    root.withdraw()
    username = None
    while username is None:
        # retrieve a username so we can distinguish all the different clients
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    c = Client(username, frame)  # this starts a client and thus a thread which keeps connection to server open
