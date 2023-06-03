import socket
import uuid
import threading

# states = [
# 
# ]



class UDP_Client:

    def __init__(self, server_ip, server_port, client_id):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_id = client_id
        self.listen_thread = threading.Thread(target=self.listen_for_responses, daemon=True)
        self.listen_thread.start()
        self.session_id = ""
        self.game_id = ""
        self.game_list = []
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.isWinner = False
        self.isLoser = False

    def send(self, command):
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))
        response, _ = self.client_socket.recvfrom(1024)
        return response.decode('utf-8')

    def listen_for_responses(self):
        while(True):
            response, _ = self.client_socket.recvfrom(1024)
            self.handle_server_response(response.decode('utf-8'))

    # To start the game
    # This might change later
    def startGame(self):
        self.isLoser = False
        self.isWinner = False
        return self.send(f'HELO 1 {self.client_id}')

    # Create a game
    def createGame(self):
        return self.send(f'CREA {self.client_id}')
    
    # Join a Game
    def joinGame(self, gameID):
        return self.send("JOIN "+gameID)

    # To make a move
    def move(self):
        location = input()
        return self.send("MOVE "+self.client_id+" "+location)

    # To get a List of games
    def gameList(self, filter):
        if filter == "ALL":
            return self.send("LIST ALL")
        return self.send("LIST CURR")
    
    # Quit the game
    def quit(self):
        return self.send("QUIT "+self.game_id)

    # To abandon the game without terminating the session
    def goodbye(self):
        return self.send("GDBY")

    # To ask for the status of a game
    def status(self, game):
        return self.send("STAT "+game)

    def handle_server_response(self, response):
        response = response.split()
        command = response[0]
        if command == 'BORD':
            self.handle_bord(response)
        elif command == 'GAMS':
            self.handle_gams(response)
        elif command == 'GDBY':
            self.handle_gdby(response)
        elif command == 'JOND':
            self.handle_jond(response)
        elif command == 'SESS':
            self.handle_sess(response)
        elif command == 'TERM':
            self.handle_term(response)
        elif command == 'YRMV':
            self.handle_yrmv(response)
    
    def handle_sess(self, response):
        self.session_id = response[1]
    
    def handle_jond(self, response):
        self.game_id = response[2]
    
    def handle_gdby(self, response):
        self.session_id = ""
        self.game_id = ""

    def handle_bord(self, response):
        board = response.split()[-1]
        if board != self.client_id:
            self.game_board = [p for p in board.split("|") if p]

    def handle_gams(self, response):
        self.game_list.clear()
        games = response.split()
        if len(games) > 0:
            for i in range(1, len(games)):
                self.game_list.append(games[i])

    def handle_yrmv(self, response):
        next_move = response[2]
        if next_move == self.client_id:
            self.move
    
    def handle_term(self, response):
        if response[1] == self.game_id:
            if len(response) > 3:
                winner_id = response[2]
                if winner_id == self.client_id:
                    self.isWinner = True
                else:
                    self.isLoser = False
            self.goodbye()
    




if __name__ == "__main__":
    client = UDP_Client('localhost', 3116, 'shivansh')

    response = client.hello()
    print(f"Server Response: {response}")
'''bytesToSend         = str.encode(msgFromClient)
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
'''
