import tkinter as tk
from tkinter import *
from tkmacosx import Button
from tkinter import messagebox

LARGEFONT =("Arial", 30)


# global variables
CLICKED = True
COUNT = 0

class Board(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#333333')

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
        button2 = Button(self, text ="Back", bg='#AACE8F',
                            command = lambda : controller.show_frame('Select'))

        button2.grid(row=3, column=1, columnspan=2, pady=5)

    def b_click(self, b):
        global CLICKED, COUNT
        if b['text'] == " " and CLICKED == True:
            b['text'] = "X"
            CLICKED = False
            COUNT += 1
            self.checkWin()
        elif b['text'] == " " and CLICKED == False:
            b['text'] = "O"
            CLICKED = True
            COUNT += 1
            self.checkWin()
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

    # Check to see if someone win
    def checkWin(self):
        global winner
        winner = False

        # check X win
        if (self.b1["text"] == "X" and self.b2["text"] == "X" and self.b3["text"] == "X") or (
            self.b1["text"] == "O" and self.b2["text"] == "O" and self.b3["text"] == "O"
        ):
            self.b1.config(bg='red')
            self.b2.config(bg='red')
            self.b3.config(bg='red')
            print(self.b1['text']) # test
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b4["text"] == "X" and self.b5["text"] == "X" and self.b6["text"] == "X") or (
            self.b4["text"] == "O" and self.b5["text"] == "O" and self.b6["text"] == "O"
        ):
            self.b4.config(bg='red')
            self.b5.config(bg='red')
            self.b6.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b7["text"] == "X" and self.b8["text"] == "X" and self.b9["text"] == "X") or (
            self.b7["text"] == "O" and self.b8["text"] == "O" and self.b9["text"] == "O"
        ):
            self.b7.config(bg='red')
            self.b8.config(bg='red')
            self.b9.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b1["text"] == "X" and self.b4["text"] == "X" and self.b7["text"] == "X") or (
            self.b1["text"] == "O" and self.b4["text"] == "O" and self.b7["text"] == "O"
        ):
            self.b1.config(bg='red')
            self.b4.config(bg='red')
            self.b7.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b2["text"] == "X" and self.b5["text"] == "X" and self.b8["text"] == "X") or (
            self.b2["text"] == "O" and self.b5["text"] == "O" and self.b8["text"] == "O"
        ):
            self.b2.config(bg='red')
            self.b5.config(bg='red')
            self.b8.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b3["text"] == "X" and self.b6["text"] == "X" and self.b9["text"] == "X") or (
            self.b3["text"] == "O" and self.b6["text"] == "O" and self.b9["text"] == "O"
        ):
            self.b3.config(bg='red')
            self.b6.config(bg='red')
            self.b9.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b1["text"] == "X" and self.b5["text"] == "X" and self.b9["text"] == "X") or (
            self.b1["text"] == "O" and self.b5["text"] == "O" and self.b9["text"] == "O"
        ):
            self.b1.config(bg='red')
            self.b5.config(bg='red')
            self.b9.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()
        elif (self.b3["text"] == "X" and self.b5["text"] == "X" and self.b7["text"] == "X") or (
            self.b3["text"] == "O" and self.b5["text"] == "O" and self.b7["text"] == "O"
        ):
            self.b3.config(bg='red')
            self.b5.config(bg='red')
            self.b7.config(bg='red')
            winner = True
            messagebox.showinfo("Tic Tac Toe", "Congratulations! You Win!")
            self.disableButtons()

        # check if tie
        if COUNT == 9 and winner == False:
            messagebox.showinfo("Tic Tac Toe", "It's a Tie!\n Nobody Wins!")
            self.disableButtons()
