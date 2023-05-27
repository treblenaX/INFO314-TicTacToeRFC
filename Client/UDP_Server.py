import socket


localIP     = "127.0.0.1"
localPort   = 8000
bufferSize  = 1024


msgFromServer       = "Hello, UDP Client"
bytesToSend         = str.encode(msgFromServer)


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

# Listen for incoming datagrams
print("UDP server up and listening")
while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)


    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)