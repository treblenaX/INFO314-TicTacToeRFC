import os
import socket
import threading
import time
import logging

BUFFER_SIZE = 1024

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def clear_console():
	command = 'clear'
	os.system(command)


class Game():
	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

		self.room = None
		self.board = None
		self.state = "PROTO"
		self.games = None

		self.event = threading.Event()

		self.update()

	# call this whenever you want the UI to change or to do something
	def update(self):
		# load data switch case
		if self.state == "LOAD SERVER CONNECTION":
			# boot up the listening thread
			listen_thread = threading.Thread(target=listen, args=(self,))
			listen_thread.start()
			self.event.wait()

			send(self, f"HELO 1 {self.name}")
		elif self.state == "LOAD CREATE":
			send(self, f"CREA {self.name}")
		elif self.state == "LOAD LIST":
			send(self, "LIST CURR")
		elif self.state == "LOAD LIST ALL":
			send(self, "LIST ALL")
		elif self.state == "LOAD GAME JOIN":
			send(self, f"JOIN {self.room}")
			send(self)

		# change UI switch case 
		if self.state == "PROTO":
			self.proto()
		elif self.state == "NAME":
			self.name()
		elif self.state == "MENU":
			self.menu()
		elif self.state == "GAME":
			self.game()
		elif self.state == "LIST":
			self.list()
		elif self.state == "WAITING ROOM":
			self.waiting_room()
		# else:
		# 	print("No State")  # test

	def list(self):	# @TODO Shivansh
		clear_console()

		print("Check these games out!")
		print()
		for game in self.games:
			print(game)
			# @TODO Shivansh print game information for each of these
		print()
		print("To join a game, type the game code - ex: AAAA")
		print("To leave, type leave().")
		print()
		list_input = input('>').strip()

		if (list_input == "leave()"):
			self.state = "MENU"
		else: 
			self.room = list_input
			self.state = "LOAD GAME JOIN"
		self.update()
		
	def waiting_room(self):
		dot_count = 1

		# OPEN - game hasn't started yet
		while not self.is_game_started:
			clear_console()

			print("You: " + self.name)
			print("Room: " + self.room)
			print()
			if (dot_count == 3):
				dot_count = 1
			else:
				dot_count += 1
			
			dots = ""
				
			for i in range(0, dot_count):
				dots += "."
			print("Waiting for another player to join" + dots)

			time.sleep(1)

		# init board
		self.board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
	
	def game(self):
		# IN_PLAY - game has started
		while not self.is_game_finished:
			clear_console()

			print("P1: " + self.player_1)
			print("P2: " + self.player_2)
			print("Room: " + self.room)
			print()
			print("GAME ON!!!")
			print()
			print("  " + self.board[0] + " | " + self.board[1] + " | " + self.board[2])
			print(" -----------")
			print("  " + self.board[3] + " | " + self.board[4] + " | " + self.board[5])
			print(" -----------")
			print("  " + self.board[6] + " | " + self.board[7] + " | " + self.board[8])
			print()

			if self.whose_move == self.name:
				print(f"It's your turn, {self.name}!")
				print("Please select a position (1-9): ")
				move_input = input(">")
				send(self, f"MOVE {self.room} {move_input}")
			else:
				print("Waiting for the other player to move...")
			

	def menu(self):
		clear_console()

		print("Welcome! " + self.name)
		print()
		print("1. Create a new game")
		print("2. Check open games")
		print("3. Check all games")
		print()
		print("Please select an option: ")

		is_option_selected = False

		while not is_option_selected:
			option = input(">")

			if option == "1":
				self.state = "LOAD CREATE"
				is_option_selected = True
			elif option == "2":
				self.state = "LOAD LIST"
				is_option_selected = True
			elif option == "3":
				self.state = "LOAD LIST ALL"
				is_option_selected = True
			else:
				print("Invalid option, please try again!")

		self.update()

	def name(self):
		print()
		print("Please input your name: ")
		self.name = input(">")
		self.state = "LOAD SERVER CONNECTION"
		self.update()

	def proto(self):
		print("Welcome to TicTacToe!")
		print()
		print("How would you like to communicate to the server (TCP/UDP)?")
		self.protocol = input(">").upper()
		self.state = "NAME"
		self.update()


#--------------------------------Outside the Class--------------------------------

# sending to server thread
def send(self, payload=None):
	if payload is not None: self.socket.sendto(f"{payload}".encode("utf-8"), (self.server_ip, self.server_port))
	# self.event.wait()

	# server listening thread
def listen(self):
	# Handle the response from the server and update the UI accordingly
	def handle(message):
		tokens = message.split(' ')
		command = tokens[0]

		if command == "SESS":	# session is created
			self.state = "MENU"
		elif command == "JOND":	# joined a game
			self.state = "WAITING ROOM"
			self.room = tokens[2]
			self.is_game_started = False
		elif command == "YRMV": # moving
			self.state = "GAME"
			self.whose_move = tokens[2]
			if not self.is_game_started:	# player has joined - start game
				self.is_game_started = True
		elif command == "GAMS":
			self.games = tokens[1:]
			self.state = "LIST"
		elif command == "BORD":
			self.player_1 = tokens[2]
			if (len(tokens) >= 3): self.player_2 = tokens[3]
			if (len(tokens) >= 5): self.board = tokens[4]
		self.update()

	# check protocol to use
	if self.protocol == 'UDP':
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	elif self.protocol == 'TCP':
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.server_ip, self.server_port))

	self.is_connected = True
	self.event.set()
	# time.sleep(3)

		# while loop
	received_data = b""
	while self.is_connected:
		data, _ = self.socket.recvfrom(BUFFER_SIZE)
		received_data += data

		if not data:
			# If the received data is empty, the server has closed the connection
			print('Connection closed by the server')
			break

		if data.endswith(b"\n"):
			# If the received data ends with a newline character, it indicates the end of a complete message
			message = received_data.decode("utf-8").strip()
			print("Received from Server:", message)
			logging.info(message)
			handle(message)
			self.event.set()
			received_data = b""

	self.socket.close()



if __name__ == "__main__":
	clear_console()
	game = Game('localhost', 3116)