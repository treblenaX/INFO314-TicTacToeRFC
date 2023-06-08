import os
import socket
import threading
import logging
import sys

BUFFER_SIZE = 1024

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def clear_console():
	command = 'clear'
	os.system(command)


class Game():
	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

		self.reset()

		# self.send_event = threading.Event()
		self.event = threading.Event()

		self.state = "PROTO"
		self.update()

	def reset(self):
		self.game_stat_dict = {}
		self.list_queue = []

		self.room = None
		self.board = None
		self.games = None

		self.is_game_init = True
		self.is_game_started = False
		self.is_game_finished = False
		self.whose_move = None


	# call this whenever you want the UI to change or to do something
	def update(self):
		# load data switch case
		if self.state == "LOAD SERVER CONNECTION":
			# boot up the listening thread
			self.listen_thread = threading.Thread(target=listen, args=(self,))
			self.listen_thread.start()
			self.event.wait()
			self.event.clear()
			send(self, f"HELO 1 {self.name}")
		elif self.state == "LOAD CREATE":
			send(self, f"CREA {self.name}")
		elif self.state == "LOAD LIST":
			send(self, "LIST CURR")
		elif self.state == "LOAD LIST ALL":
			send(self, "LIST ALL")
		elif self.state == "LOAD GAME JOIN":
			send(self, f"JOIN {self.room}")
		elif self.state == "LOAD DISCONNECT":
			send(self, f"GDBY")
		elif self.state == "LOAD LIST STAT":
			self.list_queue = self.games
			for game in self.games:
				send(self, f"STAT {game}")
				self.event.wait()
				self.event.clear()
			self.state = "LIST"
			self.update()

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
		elif self.state == "WAITING":
			self.waiting()
		elif self.state == "END GAME":
			self.end_game()
		elif self.state == "GDBY":
			self.gdby()

	def gdby(self):
		self.is_connected = False
		print("Thanks for playing!!!")
		sys.exit()

	def end_game(self):
		print("Game Over!")
		print()
		if self.winner is not None:
			print(f"Winner: {self.winner}")
		else:
			print("Tie Game!")
		print()
		print("Would you like to play again? (y/n)")

		end_game_input = input('>').lower().strip()
		if end_game_input == "y":
			self.state = "MENU"
		else:
			self.state = "LOAD DISCONNECT"

		self.reset()
		self.update()


	def list(self):	# @TODO Shivansh
		clear_console()

		if len(self.game_stat_dict) == 0:
			print("There are no games available...")
			print()
			print("To create a game, type create().")
		else:
			print("Check these games out!")
			print(self.game_stat_dict)
			print()
			print()
			print("To join a game, type the game code - ex: AAAA")
			print("To leave, type leave().")
			print("To create a game, type create().")
			print()

		list_input = input('>').strip()

		if (list_input == "leave()"):
			self.state = "MENU"
		elif (list_input == "create()"):
			self.state = "LOAD CREATE"
		else:
			self.room = list_input
			self.state = "LOAD GAME JOIN"
		self.update()

	def waiting(self):
		clear_console()
		print("Joined room: " + self.room)
		print()
		print("Waiting for another player to join...")

	def game(self):
		# IN_PLAY - game has started
		# while not self.is_game_finished:
		clear_console()

		print("You: " + self.name)
		print("Room: " + self.room)
		print()

		if self.is_game_started:
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
		else:
			print("Waiting for player...")


	def menu(self):
		clear_console()

		print("Welcome! " + self.name)
		print()
		print("1. Create a new game")
		print("2. Check open games")
		print("3. Check all games")
		print("4. Quit")
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
			elif option == "4":
				self.state = "LOAD DISCONNECT"
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

		is_protocol_select = False
		self.protocol = input(">").upper()

		while not is_protocol_select:
			if self.protocol == "TCP":
				is_protocol_select = True
			elif self.protocol == "UDP":
				is_protocol_select = True
			else:
				print("Invalid protocol, please try again!")
				self.protocol = input(">").upper()

		self.state = "NAME"
		self.update()


#--------------------------------Outside the Class--------------------------------

# sending to server thread
def send(self, payload):
	self.send_thread = threading.Thread(target=send_thread, args=(self, payload,))
	self.send_thread.start()
	self.send_thread.join()

def send_thread(self, payload):
	self.socket.sendto(f"{payload}".encode("utf-8"), (self.server_ip, self.server_port))

	# server listening thread
def listen(self):
	# Handle the response from the server and update the UI accordingly

	# check protocol to use
	if self.protocol == 'UDP':
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	elif self.protocol == 'TCP':
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.server_ip, self.server_port))

	self.is_connected = True
	self.event.set()

	try:
		# while loop
		while self.is_connected:
			data, addr = self.socket.recvfrom(BUFFER_SIZE)
			message = data.decode("utf-8").strip()
			logging.info(message)
			# print("--------" + message + "--------")
			t = threading.Thread(target=handle, args=(self, message,))
			t.start()
	except (SystemExit):
		self.socket.close()

def handle(self, message):
	tokens = message.split(' ')
	command = tokens[0]

	if command == "SESS":	# session is created
		self.state = "MENU"
		self.update()
	elif command == "JOND":	# joined a game
		self.room = tokens[2]
		self.state = "WAITING"
		self.update()
	elif command == "YRMV": # moving
		if self.is_game_init:
			self.board = ['*', '*', '*', '*', '*', '*', '*', '*', '*']
			self.is_game_init = False
			self.is_game_started = True
			self.whose_move = tokens[2]
			self.state = "GAME"
			self.update()
	elif command == "GAMS":
		self.games = tokens[1:]
		self.state = "LOAD LIST STAT"
		self.update()
	elif command == "BORD":
		if not self.is_game_started:	# store for STAT case
			room = tokens[1]
			player_1 = tokens[2]

			self.game_stat_dict[room] = {
				"player_1": player_1,
			}

			if (len(tokens) >= 5):	# game in play or finished
				self.game_stat_dict[room]["player_2"] = tokens[3]
				self.game_stat_dict[room]["player_turn"] = tokens[4]
				self.game_stat_dict[room]["board"] = tokens[5]
				if (len(tokens) == 6): self.game_stat_dict[room]["winner"] = tokens[6]

			self.list_queue.remove(room)

			if (len(self.list_queue) == 0):
				self.event.set()
		else:
			# handle game interaction and update with BORD
			self.whose_move = tokens[4]
			if (len(tokens) >= 5):
				raw_board = tokens[5]
				self.board = raw_board.split('|')[1:]
			self.update()
	elif command == "TERM":
		# tie case
		if (len(tokens) == 3):
			self.is_game_finished = True
			self.state = "END GAME"
			self.winner = None
		# winner is found
		if (len(tokens) == 4):
			self.is_game_finished = True
			self.state = "END GAME"
			self.winner = tokens[2]
		self.update()
	elif command == "GDBY":	# session is cut - game is over
		self.state = "GDBY"
		self.update()




if __name__ == "__main__":
	clear_console()
	game = Game('localhost', 3116)