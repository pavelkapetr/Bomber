import socket

# Síťové nastavení
serverAddress_Port = ("127.0.0.1", 20001)
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize = 1024


def send(msg):
    toSend = msg.encode('utf-8')
    client_socket.sendto(toSend, serverAddress_Port)


def receive():
    serverInfo = client_socket.recvfrom(bufferSize)
    msgOdServer = f"{serverInfo[0].decode('utf-8')}"
    return msgOdServer
