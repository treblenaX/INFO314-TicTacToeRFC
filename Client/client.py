"""
Pages:
Welcome Page: Enter to the Game
Selection Page: Join Game
Game Page: Start Game
"""
import board
import selection

def main(name):
  # TODO
  # create a UI Page for welcome page

  # Welcome Page
  print("Welcome to the game! " + name)
  val = input("Enter if start the game (y / n): ")
  print(val)
    # if user enters 1: enter to the
  if val.lower() == "y":
    # TODO
    # Create a UI Page for selection page
    print("Go to the Selection Page")

    # Call Server
    # Request a message from the server for the opening games
    msg = "GAMS AAAA BBBB CCCC"


    # Selection Page
    # Now: 1. Just show all opening games
    #        - Ask server for a list
    #        - Get the current players name in each game
    #      2. Create a Game
    #        - Send resquest to the server for start a game
    #        - Wait response for the server if someone join the game
    selection.Selection(msg)

    # start game: show board
    # board.Board()
  else:
     print("Close the game")


if __name__ == "__main__":
    name = "Mary"
    main(name)