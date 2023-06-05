import os
import socket
import threading

BUFFER_SIZE = 1024

def clear_console():
	command = 'clear'
	os.system(command)

class Console():
	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

		self.room = None
		self.board = None
		self.state = "PROTO"

		self.response_event = threading.Event()
		
		print("Welcome to Tic Tac Toe Game!")

		self.update()

	def wait(self):
		self.response_event.wait()
		self.response_event.clear()

	# call this whenever you want the UI to change or to do something	
	def update(self):
		print(self.state)
		if self.state == "PROTO":
			self.proto()
		elif self.state == "NAME":
			self.name()
		elif self.state == "INIT_SERVER":
			listen_thread = threading.Thread(target=listen, args=(self,))
			listen_thread.start()
			self.wait()
			self.state = "CONNECT"
			self.update()
		elif self.state == "CONNECT":
			send(self, f"HELO 1 {self.name}")
			self.wait()
		elif self.state == "MENU":
			self.menu()
		elif self.state == "CREATE":
			self.create()
		elif self.state == "GAME":
			self.game()
		elif self.state == "LOAD LIST":
			send(self, "LIST")
			self.wait()
			self.state = "DISPLAY LIST"
			self.update()
		elif self.state == "DISPLAY LIST":
			self.list()

	def list(self):
		print("Open games:")
		print()
		print(self.games)


	def game(self):
		self.game_start = False
		clear_console()
		print("You: " + self.name)
		print("Room: " + self.room)
		print()

		if not self.game_start:
			print("Waiting for another player to join...")

	def create(self):
		send(self, f"CREA {self.name}")

	def menu(self):
		clear_console()

		print("Welcome! " + self.name)
		print()
		print("1. Create a new game")
		print("2. Check open games")
		print("3. Check all games")
		print()
		print("Please select an option: ")

		option = input()

		if option == "1":
			self.state = "CREATE"
		elif option == "2":
			self.state = "LOAD LIST"
		elif option == "3":
			self.state = "LIST ALL"
		else:
			print("Invalid option, please try again!")

		self.update()

	def name(self):
		clear_console()

		self.name = input("Please input your name: ")
		self.state = "INIT_SERVER"
		self.update()

	def proto(self):
		clear_console()
		
		self.protocol = input("Which protocol version are you using now? (TCP/UDP)").upper()
		self.state = "NAME"
		self.update()

# sending to server thread
def send(self, payload):
	self.socket.sendto(f"{payload}".strip().encode("utf-8"), (self.server_ip, self.server_port))

# server listening thread
def listen(self):
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
			print(';seiufhlskehfef')
			self.games = tokens[1:]
			
		self.update()
	
	# check version
	if self.protocol == 'UDP':
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	elif self.protocol == 'TCP':
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.server_ip, self.server_port))

	self.is_connected = True
	self.response_event.set()
	print("DEBUG: Listening to server...")

	# while loop
	while self.is_connected:
		message = self.socket.recvfrom(BUFFER_SIZE)[0].decode("utf-8").strip()
		print(message)
		handle(message)
		self.response_event.set()

	self.socket.close()



if __name__ == "__main__":
	console = Console('localhost', 3116)