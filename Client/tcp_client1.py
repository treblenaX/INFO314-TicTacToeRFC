import socket
import threading
import time


bufferSize = 1024

class Client(threading.Thread):
    def __init__(self, server_ip, server_port, name):
        threading.Thread.__init__(self)

        self.server_ip = server_ip
        self.server_port = server_port
        self.name = name

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))

        # Create a session
        print("Client is running!")
        self.client.sendall(f"HELO 1 {self.name}".encode())
        msgFromServer = self.client.recv(bufferSize)
        msg1 = msgFromServer.decode()
        print(msg1)



    def run(self):
        def receive():
            print("Receiver start")
            while True:
                try:
                    message, _ = self.client.recvfrom(bufferSize)
                    print("Server: ", message.decode())
                except:
                    pass

        t = threading.Thread(target=receive)
        t.start()
        # time.sleep(1)

        # LIST or Create
        while True:
            input_msg = input("Enter a message to send: ")
            print(input_msg)
            if input_msg == "quit":
                exit()
            # print(input_msg)
            else:
                self.client.sendto(input_msg.encode(), (self.server_ip, self.server_port))

            time.sleep(2)


if __name__ == "__main__":
    thread = Client('localhost', 3116, 'Sophie')
    thread.start()
