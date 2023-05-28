import socket

msgFromClient = ""

# To start the game
# Please note if we create a version 2 of our game, we need to change this to add functionality
def startGame(name):
    return "HELO 1 "+name

# To get a List of games
def gameList(filter):
    if filter == "ALL":
        return "LIST ALL"
    return "LIST CURR"

# Create a game
def createGame(name):
    return "CREA "+name

# Quit the game
def quitGame():
    return "GDBY"

# Join a Game
def joinGame(gameID):
    return "JOIN "+gameID

# To make a move
def move(name, location)
    return "MOVE "+name+" "+location

# To abandon the game without terminating the session
def abandonGame():
    return "QUIT"

# To ask for the status of a game
def status(game):
    return "STAT "+game

bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 8000)
bufferSize          = 1024


# Create a UDP socket at client side
# SOCK_DGRAM for UDP packets
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)


msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
