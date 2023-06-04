import sys
import client
import os

def clear_console():
  command = 'clear'
  os.system(command)

def main():
  print("Welcome to Tic Tac Toe Game!")
  print("Which protocol version are you using now? (TCP/UDP)")
  version = input()
  version = version.upper()
  # print(version)
  name = input("Please input your name: ")
  print("Welcome! " + name)
  clear_console()

  player = client.Client('localhost', 3116, name, version)
  player.start()


if __name__ == "__main__":
  main()