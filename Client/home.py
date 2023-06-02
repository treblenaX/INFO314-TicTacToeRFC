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
from tkmacosx import Button
from tkinter import messagebox
from board import Board


LARGEFONT =("Arial", 30)

# # global variables
# CLICKED = True
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


# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')

        # Set everything in the middle of the screen

        # Create widgets
        login_label = tk.Label(self, text='Welcome to TicTacToe Game!', bg='#333333', fg='#AACE8F', font=("Arial", 35))
        player_name = tk.Label(self, text='Please Enter Your Name:', bg='#333333', fg='#AACE8F', font=("Arial", 20))
        self.player_entry = tk.Entry(self, font=("Arial", 20))
        login_button = tk.Button(
            self, text="Start", bg="#BAD0B9", fg="#333333", font=("Arial", 25), highlightbackground='#BAD0B9',
            command = lambda : controller.show_frame("Select")
        )


        login_label.pack(padx=5,  pady=40)
        player_name.pack(padx=5,  pady=15)
        self.player_entry.pack()
        login_button.pack(padx=5,  pady=60)


# Selection Page for Create or Join a Game
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


# show a list of games
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

# class Board(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent, bg='#333333')

#         self.b = [
#             [0,0,0],
#             [0,0,0],
#             [0,0,0]]

#         #text for buttons
#         self.states = [
#             [0,0,0],
#             [0,0,0],
#             [0,0,0]]

#         for i in range(3):
#             for j in range(3):
#                 self.b[i][j] = Button(
#                                 height = 180, width = 200,
#                                 font = ("Arial", 30),
#                                 command = lambda r = i, c = j : self.clicked(r,c))
#                 self.b[i][j].grid(row = i, column = j)


#         # Quit a Game (will make a button disabled)
#         # button1 = Button(self, text ="Quit", bg='#AACE8F', fg='black',
#         #                     command = lambda : controller.show_frame('Select'))

#         # button1.grid(row=3, column=0, columnspan=2, pady=5)
#         # # Back to Selection Page
#         # button2 = Button(self, text ="Back", bg='#AACE8F', fg='black',
#         #                     command = lambda : controller.show_frame('Select'))

#         # button2.grid(row=3, column=1, columnspan=2, pady=5)

#     def clicked(self, r, c):
#         #player
#         global Player1, COUNT
#         # global stop_game

#         if Player1 == "X" and self.states[r][c] == 0 and stop_game == False:
#             self.b[r][c].configure(text = "X")
#             self.states[r][c] = 'X'
#             Player1='O'
#             COUNT += 1
#             self.check_if_win()


#         elif Player1 == 'O' and self.states[r][c] == 0 and stop_game == False:
#             self.b[r][c].configure(text = 'O')
#             self.states[r][c] = "O"
#             Player1 = "X"
#             COUNT += 1
#             self.check_if_win()

#         else:
#             messagebox.showerror("Tic Tac Toe", "Hey! That box has already been selected\nPick Another Box...")


#     # disable button
#     def disableButtons(self):
#         pass
#         # for i in range(3):
#         #     for j in range(3):
#         #         self.b[i][j].config(state=DISABLED)

#     # Check to see if someone win
#     def check_if_win(self):
#         global stop_game
#         # count = 0

#         for i in range(3):
#             if self.states[i][0] == self.states[i][1] == self.states[i][2] !=0:
#                 stop_game = True
#                 self.b[i][0].configure(bg='white')
#                 self.b[i][1].configure(bg='white')
#                 self.b[i][2].configure(bg='white')
#                 winner = messagebox.showinfo("Winner", self.states[i][0] + " Won")
#                 self.disableButtons()
#                 break

#         # for j in range(3):
#             elif self.states [0][i] == self.states[1][i] == self.states[2][i] != 0:
#                 stop_game = True
#                 winner = messagebox.showinfo("Winner", self.states[0][i]+ " Won!")
#                 self.disableButtons()
#                 break

#             elif self.states[0][0] == self.states[1][1] == self.states[2][2] !=0:
#                 stop_game = True
#                 winner = messagebox.showinfo("Winner", self.states[0][0]+ " Won!")
#                 self.disableButtons()
#                 break

#             elif self.states[0][2] == self.states[1][1] == self.states[2][0] !=0:
#                 stop_game = True
#                 winner = messagebox.showinfo("Winner" , self.states[0][2]+ " Won!")
#                 self.disableButtons()
#                 break

#             elif self.states[0][0] and self.states[0][1] and self.states[0][2] and self.states[1][0] and self.states[1][1] and self.states[1][2] and self.states[2][0] and self.states[2][1] and self.states[2][2] != 0:
#                 stop_game = True
#                 winner = messagebox.showinfo("tie", "It's a Tie!")
#                 self.disableButtons()
#                 break


# Driver Code
if __name__ == "__main__":
    app = Windows()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()