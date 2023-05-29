import tkinter as tk
from board import Board, Finish
# from selection import Select
# from tkinter import ttk

LARGEFONT =("Arial", 30)

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
        for F in (StartPage, Select, Board, Finish):
            frame = F(container, self)
            # initializing frame of that object from startpage, Select, Board, Finish
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage)

    # Display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # raises the current frame to the top


# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set background color for current frame
        self.configure(bg='#333333')
        # Set everything in the middle of the screen

        # Create widgets
        login_label = tk.Label(self, text='Welcome to TicTacToe Game!', bg='#333333', fg='#AACE8F', font=("Arial", 35))
        player_name = tk.Label(self, text='Please Enter Your Name:', bg='#333333', fg='#AACE8F', font=("Arial", 20))
        self.player_entry = tk.Entry(self, font=("Arial", 20))
        login_button = tk.Button(
            self, text="Start", bg="#BAD0B9", fg="#333333", font=("Arial", 25), highlightbackground='#BAD0B9',
            command = lambda : controller.show_frame(Select)
        )


        login_label.pack(padx=5,  pady=40)
        player_name.pack(padx=5,  pady=15)
        self.player_entry.pack()
        login_button.pack(padx=5,  pady=60)

    def getName(self):
        name =self.player_entry.get()
        return name

# second window frame page1
class Select(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.configure(bg='#333333')

        label = tk.Label(self, text ="Select a Game Room", bg='#333333', fg='#AACE8F', font = LARGEFONT)
        # label.grid(row = 0, column = 4, padx = 10, pady = 10)
        label.pack(padx=5,  pady=40)

        # create multiple rooms
        button1 = tk.Button(self, text ="Room 1: Player A", bg="#AACE8F",
                            command = lambda : controller.show_frame(Board))
        button1.pack(padx=5,  pady=15)

        button2 = tk.Button(self, text ="Room 2: Player B", bg="#AACE8F",
                            command = lambda : controller.show_frame(Board))
        button2.pack(padx=5,  pady=15)

        button3 = tk.Button(self, text ="Room 3", bg="#AACE8F", fg='#333333',
                            command = lambda : controller.show_frame(Board))
        button3.pack(padx=5,  pady=15)


# Driver Code
if __name__ == "__main__":
    app = Windows()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()