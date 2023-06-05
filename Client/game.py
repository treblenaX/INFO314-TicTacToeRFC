import sys
import client
import os

def clear_console():
  command = 'clear'
  os.system(command)

def main():
  clear_console()
  print("Welcome to Tic Tac Toe Game!")
  print("Which protocol version are you using now? (TCP/UDP)")
  version = input()
  version = version.upper()
  clear_console()
  # print(version)
  name = input("Please input your name: ")
  clear_console()
  print("Welcome! " + name)
  print()

  player = client.Client('localhost', 3116, name, version)
  player.start()



if __name__ == "__main__":
	main()