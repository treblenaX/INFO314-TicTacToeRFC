"""
GDBY:
    Client -> Server (QUIT, not terminate the Session)
    Server -> Client (Finished the Session)
STAT? (Client -> Server)(Which the page should the get the response.)

1st Page:
  -HELO: Initiate a Session with the Server (Client -> Server)
  --SESS: Indicate the server has officially created a unique session.(Server -> Client)

2nd Page:
  -LIST: See a play game list. (Client -> Server, Server response GAMES)
  1. -CREA: Create a new game. (Client -> Server, Server response JOIN)
  2. -JOIN: Join the existed opening game. (Client -> Server)
  -JOND: Join the game successfully. (Server -> Client)

3rd Page (Game Page):
  -YRMV: Tells us which player's move is currently accepted. (Server -> Client)
  -MOVE: client makes a move(Client -> Server)
  -QUIT: client abandon the game without terminating the session. (Client -> Server)
"""

import tkinter as tk
from tkinter import *
from tkmacosx import Button
from tkinter import messagebox
# from board_test import Board


LARGEFONT =("Arial", 30)

# global variables
CLICKED = True
# COUNT = 0

class Windows(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("TicTacToe Game")
        self.geometry('600x600')

        # creating a frame and assigning it to container
        container = tk.Frame(self)
        # specifying the region where the frame is packed in root
        container.pack(side = "top", fill = "both", expand = True)
        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # create a dictionary of frames
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Select, Board, List):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# 1st Frame: Startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')

        # Create widgets
        login_label = tk.Label(self, text='Welcome to TicTacToe Game!', bg='#333333', fg='#AACE8F', font=("Arial", 35))
        player = tk.Label(self, text='Please Enter Your Name:', bg='#333333', fg='#AACE8F', font=("Arial", 20))

        name = tk.StringVar()
        self.player_entry = tk.Entry(self, font=("Arial", 20), textvariable=name)

        # get player's name
        def get_player():
            player_name = name.get()
            print(player_name) # test
            controller.show_frame("Select")

        login_button = tk.Button(
            self, text="Start", bg="#BAD0B9", fg="#333333", font=("Arial", 25), highlightbackground='#BAD0B9',
            command = get_player
        )


        login_label.pack(padx=5,  pady=40)
        player.pack(padx=5,  pady=15)
        self.player_entry.pack()
        login_button.pack(padx=5,  pady=60)


# 2nd Frame: Selection Page for Create or Join a Game
class Select(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg='#333333')

        label = tk.Label(self, text ="Welcome to TicTacToe Game!", bg='#333333', fg='#AACE8F', font = LARGEFONT)
        # label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.pack(padx=5,  pady=40)

        # create multiple rooms
        button1 = tk.Button(self, text ="Create A Game", bg="#AACE8F",
                            command = lambda : controller.show_frame("Board"))
        button1.pack(padx=5,  pady=15)

        button2 = tk.Button(self, text ="Join A Game", bg="#AACE8F",
                            command = lambda : controller.show_frame("List"))
        button2.pack(padx=5,  pady=15)


# Frame: show a list of games
class List(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.configure(bg='#333333')

        label = tk.Label(self, text ="Select a Game Room", bg='#333333', fg='#AACE8F', font = LARGEFONT)
        # label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.pack(padx=5,  pady=40)

        # create multiple rooms
        button1 = tk.Button(self, text ="Room 1: Player A", bg="#AACE8F",
                            command = lambda : controller.show_frame('Board'))
        button1.pack(padx=5,  pady=15)

        button2 = tk.Button(self, text ="Room 2: Player B", bg="#AACE8F",
                            command = lambda : controller.show_frame('Board'))
        button2.pack(padx=5,  pady=15)

        backButton = tk.Button(self, text ="Back", bg="#AACE8F", fg='#333333',
                            command = lambda : controller.show_frame('Select'))
        backButton.pack(padx=5,  pady=15)

# Frame: Game Board
class Board(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')
        self.controller = controller

        self.b1 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b1))
        self.b2 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b2))
        self.b3 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b3))

        self.b4 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b4))
        self.b5 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b5))
        self.b6 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b6))

        self.b7 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b7))
        self.b8 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b8))
        self.b9 = Button(self, text=' ', font=("Arial", 80), height=180, width=200, bg='#333333',fg='#AACE8F', borderless=1, command=lambda: self.b_click(self.b9))

        self.b1.grid(row=0, column=0)
        self.b2.grid(row=0, column=1)
        self.b3.grid(row=0, column=2)

        self.b4.grid(row=1, column=0)
        self.b5.grid(row=1, column=1)
        self.b6.grid(row=1, column=2)

        self.b7.grid(row=2, column=0)
        self.b8.grid(row=2, column=1)
        self.b9.grid(row=2, column=2)
        # self.buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9]

        # Quit a Game (will make a button disabled)
        button1 = Button(self, text ="Quit", bg='#AACE8F',
                            command = self.disableButtons)

        button1.grid(row=3, column=0, columnspan=2, pady=5)
        # Back to Selection Page
        # referesh the board! (not work!)
        # button2 = Button(self, text ="Back", bg='#AACE8F',
        #                     command = lambda : controller.show_frame('Select'))
        button2 = Button(self, text ="Back", bg='#AACE8F',
                            command = self.refresh)

        button2.grid(row=3, column=1, columnspan=2, pady=5)

    def refresh(self):
        global CLICKED
        self.enableButtons()
        self.b1.config(text=' ', bg='#333333')
        self.b2.config(text=' ', bg='#333333')
        self.b3.config(text=' ', bg='#333333')
        self.b4.config(text=' ', bg='#333333')
        self.b5.config(text=' ', bg='#333333')
        self.b6.config(text=' ', bg='#333333')
        self.b7.config(text=' ', bg='#333333')
        self.b8.config(text=' ', bg='#333333')
        self.b9.config(text=' ', bg='#333333')
        CLICKED = True
        self.controller.show_frame('Select')

    def b_click(self, b):
        global CLICKED
        if b['text'] == " " and CLICKED == True:
            b['text'] = "X"
            CLICKED = False

        elif b['text'] == " " and CLICKED == False:
            b['text'] = "O"
            CLICKED = True
        else:
            messagebox.showerror("Tic Tac Toe", "Hey! That box has already been selected\nPick Another Box...")


    # disable button
    def disableButtons(self):
        self.b1.config(state=DISABLED)
        self.b2.config(state=DISABLED)
        self.b3.config(state=DISABLED)
        self.b4.config(state=DISABLED)
        self.b5.config(state=DISABLED)
        self.b6.config(state=DISABLED)
        self.b7.config(state=DISABLED)
        self.b8.config(state=DISABLED)
        self.b9.config(state=DISABLED)

    # disable button
    def enableButtons(self):
        self.b1.config(state=ACTIVE)
        self.b2.config(state=ACTIVE)
        self.b3.config(state=ACTIVE)
        self.b4.config(state=ACTIVE)
        self.b5.config(state=ACTIVE)
        self.b6.config(state=ACTIVE)
        self.b7.config(state=ACTIVE)
        self.b8.config(state=ACTIVE)
        self.b9.config(state=ACTIVE)



# Driver Code
if __name__ == "__main__":
    app = Windows()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()