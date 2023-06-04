import socket
import threading
import time

bufferSize = 1024

class UDP_Client(threading.Thread):

    def __init__(self, server_ip, server_port, client_id):
        threading.Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_id = client_id
        self.session_id = ""
        self.game_id = ""
        self.game_list = []
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.isWinner = False
        self.isLoser = False

        print("Client is running!")
        self.client_socket.sendto(f"HELO 1 {self.name}".encode(), (self.server_ip, self.server_port))
        msgFromServer = self.client_socket.recvfrom(bufferSize)
        msg1 = msgFromServer[0].decode()
        print(msg1)
    '''def listen_to_server(self):
        while True:
            try:
                response, _ = self.client_socket.recvfrom(1024)
                decoded_response = response.decode('utf-8')
                print(f"Received: {decoded_response}")
                self.handle_server_response(decoded_response)
            except Exception as e:
                print(f"Error occurred while listening for responses: {e}")
                break'''
    

    def run(self):
        def receive():
            print("Receiver start")
            while True:
                try:
                    message,  = self.client_socket.recvfrom(bufferSize)
                    decoded_response = message.decode()
                    print("Server:", decoded_response)
                    self.handle_server_response(decoded_response)
                except:
                    pass

        t = threading.Thread(target=receive)
        t.start()
        # time.sleep(1)

        # LIST or Create
        while True:
            input_msg = input("Enter a message to send: ")
            if input_msg == "quit":
                exit()
            # print(input_msg)
            else:
                self.client_socket.sendto(input_msg.encode(), (self.server_ip, self.server_port))

            time.sleep(2)


    def send(self, command):
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))
        
    # To start the game
    # This might change later
    def startGame(self):
        self.isLoser = False
        self.isWinner = False
        command = 'HELO 1 {self.client_id}'
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

    # Create a game
    def createGame(self):
        command = 'CREA {self.client_id}'
        self.client_socket.sendto(command.encode(), (self.server_ip, self.server_port))
    
    # Join a Game
    def joinGame(self, gameID):
        command = "JOIN "+gameID
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

    # To make a move
    def move(self):
        location = input()
        command = "MOVE "+self.client_id+" "+location
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

    # To get a List of games
    def gameList(self, filter):
        if filter == "ALL":
            command = "LIST ALL"
            self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))
        else:
            command = "LIST CURR"
            self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))
    
    # Quit the game
    def quit(self):
        command = "QUIT "+self.game_id
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

    # To abandon the game without terminating the session
    def goodbye(self):
        command = "GDBY"
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

    # To ask for the status of a game
    def status(self, game):
        command = "STAT "+game
        self.client_socket.sendto(command.encode('utf-8'), (self.server_ip, self.server_port))

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
        self.session_id = response[2]
        print(self.session_id)
    
    def handle_jond(self, response):
        self.game_id = response[2]
    
    def handle_gdby(self, response):
        self.session_id = ""
        self.game_id = ""
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def handle_bord(self, response):
        board = response.split()[-1]
        if board != self.client_id:
            gameboard = [p for p in board.split("|") if p]
            self.game_board = [gameboard[i:i+3] for i in range(0, len(gameboard), 3)]

    def handle_gams(self, response):
        self.game_list.clear()
        games = response.split()
        if len(games) > 0:
            for i in range(1, len(games)):
                self.game_list.append(games[i])

    def handle_yrmv(self, response):
        next_move = response[2]
        if next_move == self.client_id:
            self.move()
    
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
    thread = UDP_Client('localhost', 3116, 'Kathy')
    thread.start()
