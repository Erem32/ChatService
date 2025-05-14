from tkinter import *
import queue

BLACK = "#000000"
WHITE = "#FFFFFF"
GREEN = "#4CAF50"
DARK_GRAY = "#2E2E2E"
VERY_DARK_GRAY = "#1E1E1E"
MEDIUM_GRAY = "#323232"
ENTRY_GRAY = "#2C2C2C"

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.geometry("400x300")
        self.login_screen()  # Login screen
        self.msg_queue = queue.Queue()
        self.last_sent = None  # Store last sent message to filter echo from the server
        self.Window.after(100, self.poll_queue)
        self.Window.mainloop()

    def login_screen(self):
        self.Window.title("Login")
        self.Window.configure(bg=DARK_GRAY)
        
        # Frame for the login screen
        login_frame = Frame(self.Window, bg=DARK_GRAY)
        login_frame.place(relwidth=1, relheight=1)
        
        Label(login_frame, 
              text="Please login to continue", 
              font="Helvetica 16 bold", 
              bg=DARK_GRAY, 
              fg=WHITE).pack(pady=(20, 10))
        
        Label(login_frame, 
              text="Name:", 
              font="Helvetica 14", 
              bg=DARK_GRAY, 
              fg=WHITE).pack(pady=(10, 5))
        
        self.entryName = Entry(login_frame, 
                               font="Helvetica 14", 
                               bg=WHITE, 
                               fg=BLACK)
        self.entryName.pack(pady=(0, 10), ipadx=50, ipady=5)
        self.entryName.focus()

        Button(login_frame, 
               text="CONTINUE", 
               font="Helvetica 14 bold", 
               bg=GREEN, 
               fg=WHITE, 
               relief=FLAT, 
               bd=0, 
               cursor="hand2", 
               command=lambda: self.goAhead(self.entryName.get())).pack(pady=(20, 10), ipadx=10, ipady=5)

    def goAhead(self, name):
        # Remove login screen widgets
        for widget in self.Window.winfo_children():
            widget.destroy()
        self.chat_layout(name)
        from client import talk_to_server
        talk_to_server(self, name)  # Pass the nickname to the server

    def poll_queue(self):
        """
        Updates the GUI when new messages appear in the queue.
        """
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            # Filter out echo of our own message from the server
            if self.last_sent is not None and msg == self.last_sent:
                self.last_sent = None
            else:
                self.appendMessageToChat(msg)
        self.Window.after(100, self.poll_queue)

    def chat_layout(self, name):
        self.name = name
        self.Window.title("CHATROOM")
        self.Window.geometry("470x550")
        self.Window.resizable(True, True)
        self.Window.configure(bg=VERY_DARK_GRAY)

        # Header frame displaying nickname
        header_frame = Frame(self.Window, bg=VERY_DARK_GRAY)
        header_frame.pack(fill=X)
        Label(header_frame, 
              text=self.name, 
              bg=VERY_DARK_GRAY, 
              fg=WHITE, 
              font="Helvetica 14 bold").pack(pady=10)

        # Separator line
        line = Frame(self.Window, bg=GREEN, height=2)
        line.pack(fill=X, padx=10)

        # Frame for chat messages and scrollbar
        chat_frame = Frame(self.Window, bg=VERY_DARK_GRAY)
        chat_frame.pack(padx=10, pady=(5, 0), fill=BOTH, expand=True)

        # Text area for displaying messages
        self.textCons = Text(chat_frame, 
                             bg=VERY_DARK_GRAY, 
                             fg=WHITE, 
                             font="Helvetica 14", 
                             padx=10, pady=10, 
                             bd=0)
        self.textCons.pack(side=LEFT, fill=BOTH, expand=True)
        self.textCons.config(state=DISABLED)

        # Scrollbar for the chat text area
        scrollbar = Scrollbar(chat_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textCons.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.textCons.yview)

        # Bottom frame for message input
        bottom_frame = Frame(self.Window, bg=MEDIUM_GRAY, height=80)
        bottom_frame.pack(fill=X, side=BOTTOM)

        self.entryMsg = Entry(bottom_frame, 
                              bg=ENTRY_GRAY, 
                              fg=WHITE, 
                              font="Helvetica 13", 
                              bd=0)
        self.entryMsg.pack(side=LEFT, padx=10, pady=10, ipady=7, fill=X, expand=True)
        self.entryMsg.focus()

        # Bind Enter key to send message
        self.entryMsg.bind("<Return>", lambda event: self.sendMessage())

        self.buttonMsg = Button(bottom_frame, 
                                text="Send", 
                                font="Helvetica 12 bold", 
                                bg=GREEN, 
                                fg=WHITE, 
                                relief=FLAT, 
                                bd=0, 
                                cursor="hand2", 
                                command=self.sendMessage)
        self.buttonMsg.pack(side=RIGHT, padx=10, pady=10, ipadx=10, ipady=7)

    def sendMessage(self, event=None):
        from client import send
        message = self.entryMsg.get()
        if message:
            full_message = f"{self.name}: {message}"
            send(self.name, message)
            self.entryMsg.delete(0, END)
            # Save sent message to filter the echo from server
            self.last_sent = full_message
            # Immediately display the message locally
            self.appendMessageToChat(full_message)

    def appendMessageToChat(self, msg):
        if msg:
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, f"{msg}\n")
            self.textCons.config(state=DISABLED)
            self.textCons.yview(END)
