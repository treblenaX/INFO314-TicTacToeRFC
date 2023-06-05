import os
import socket
import threading
import time

BUFFER_SIZE = 1024

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
			send(self, "LIST CURR")
		elif self.state == "LOAD GAME JOIN":
			send(self, f"JOIN {self.room}")

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

	def game(self):
		self.game_start = False
		clear_console()

		print("You: " + self.name)
		print("Room: " + self.room)
		print()

		if not self.game_start:
			print("Waiting for another player to join...")

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
def send(self, payload):
	self.socket.sendto(f"{payload}".encode("utf-8"), (self.server_ip, self.server_port))
	self.event.wait()

	# server listening thread
def listen(self):
	# Handle the response from the server and update the UI accordingly
	def handle(message):
		tokens = message.split(' ')
		command = tokens[0]

		if command == "SESS":	# session is created
			self.state = "MENU"
		elif command == "JOND":	# joined a game
			self.state = "GAME"
			self.room = tokens[2]
		elif command == "YRMV": # moving
			self.state = "GAME"
			self.whose_move = tokens[2]
			if not self.game_started:	# player has joined - start game
				self.game_started = True
		elif command == "GAMS":
			self.games = tokens[1:]
			self.state = "LIST"

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
	while self.is_connected:
		message = self.socket.recvfrom(BUFFER_SIZE)[0].decode("utf-8").strip()
		# print("Receiver from Server: ", message)
		handle(message)
		self.event.set()

	self.socket.close()



if __name__ == "__main__":
	clear_console()
	game = Game('localhost', 3116)