import socket
import threading
import time
import os

bufferSize = 1024

class Client(threading.Thread):
    def __init__(self, server_ip, server_port, name, version):
        threading.Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port = server_port

        # check the version
        self.version = version
        if self.version == 'UDP':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif self.version == 'TCP':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server_ip, self.server_port))

        self.name = name
        self.room = None
        self.board = None

        # Create a session
        self.client.sendto(f"HELO 1 {self.name}".encode(), (self.server_ip, self.server_port))
        msgFromServer = self.client.recvfrom(bufferSize)
        msg1 = msgFromServer[0].decode()


        # Creat Game or Check List
        self.start_page()
        # come to game page

    # run the thread, when calling thread.sart()
    def run(self):
        # show initial board
        self.show_board("xxx")
        # a thread to receive message from server
        def receive():
            # print("Receiver start")
            while True:
                try:
                    message, addr = self.client.recvfrom(bufferSize)
                    # self.messages.put((message, add))
                    # check messages
                    message = message.decode().strip()
                    tokens = message.split(' ')
                    if tokens[0] == 'YRMV':
                        player = tokens[2]
                        # print(player)
                        self.show_turn(player)
                        # self.show_board(board)
                    elif tokens[0] == 'BORD' and len(tokens) > 3:
                        board = tokens[5]
                        self.board = board
                        # print(board)
                        self.show_board(board)
                    elif tokens[0] == 'TERM' and len(tokens) >= 4:
                        winner = tokens[2]
                        print("Winner is " + winner + "!")
                        print("Do you want to start a second game? (y/n)")
                        reply = input()
                        if reply == 'y':
                            self.clear_console()
                            self.start_page()
                        else:
                            # TODO I have no idea for this
                            pass
                    else:
                        # TODO other cases like JOND, QUIT ?
                        print("Server: ", message)
                except:
                    pass

        t = threading.Thread(target=receive)
        t.start()

        # start the game
        while True:
            # while not self.messages.empty():
            #     message, addr = self.messages.get()
            #     print("Receive from Server: ", message.decode())
            input_msg = input()
            if input_msg == "quit":
                exit()
            else:
                self.client.sendto(input_msg.encode(), (self.server_ip, self.server_port))

            time.sleep(3)


    # clear the console
    def clear_console(self):
        command = 'clear'
        os.system(command)


    # send CREA to server
    def create_game(self):
        self.client.sendto(f"CREA {self.name}".encode(), (self.server_ip, self.server_port))
        msgFromServer = self.client.recvfrom(bufferSize)
        msg2 = msgFromServer[0].decode()
        # print(msg2)
        self.clear_console()
        room = msg2.split(' ')[2]
        self.room = room
        print("You: " + self.name)
        print("Your room is: " + room)
        print("Please wait for other player join in!")



    # show which player should played now
    def show_turn(self, name):
        print("Now is " + name + "'s Turn!")


    # show the current game boad
    def show_board(self, board):
        board = board.split('|')[1:10]
        if self.board == None:
            new_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        else:
            new_board = [[board[0], board[1], board[2]],
                        [board[3], board[4], board[5]],
                        [board[6], board[7], board[8]]]
            self.board = 'UPDATE'
        for row in new_board:
            for item in row:
                print(item, end="    ")
            print()


    # Start Page shows Create or List a Game
    def start_page(self):
        # Creat Game or Check List
        print("Give me your choice!(1 or 2)\n1. Create a New Game\n2. Check current open games\n3. Check all Games")
        response = input("")
        print(response)
        # check valid input
        while response != '1' and response != '2' and response != '3':
            response = input("Please enter 1 or 2 or 3:")
        # check the response
        if response == '1':
            self.clear_console()
            self.create_game()
        elif response == '2':
            self.clear_console()

            self.client.sendto(f"LIST ".encode(), (self.server_ip, self.server_port))
            msgFromServer = self.client.recvfrom(bufferSize)
            msg2 = msgFromServer[0].decode()
            # print(msg2) # test the response from server for LIST command
            # print(len(msg2))
            if len(msg2) < 6:
                print("Sorry, no game is openning now\nDo you want to create a new Game!(y or n)")
                res = input()
                print(res)

                # create a game
                self.create_game()
            else:
                # TODO check STAT
                tokens = msg2.split(' ')

                rooms = []
                for room in tokens[1:]:
                    print("Game Room: " + room)
                    rooms.append(room[:4])
                print("rooms: ",rooms)

                room_join = input("Please choose a room to join: ")
                print("room_join: ", room_join)
                print(len(room_join))

                while room_join not in rooms or len(room_join) != 4:
                    room_join = input("Please input a valid room name: ")

                self.room = room_join
                # print(room_join)
                self.client.sendto(f"JOIN {room_join}".encode(), (self.server_ip, self.server_port))
                msgFromServer = self.client.recvfrom(bufferSize)
                msg = msgFromServer[0].decode()
                print(msg)
                self.clear_console()
                print("You: " + self.name)
                print("Your room is: " + self.room)
        elif response == '3':
            self.clear_console()
            # TODO show the game status

            self.client.sendto(f"LIST ALL".encode(), (self.server_ip, self.server_port))
            msgFromServer = self.client.recvfrom(bufferSize)
            msg2 = msgFromServer[0].decode()
            print(msg2)
            # TODO check STAT

if __name__ == "__main__":
    thread = Client('localhost', 3116, 'Sophie')
    thread.start()