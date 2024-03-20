import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

msgToSend = "Waiting for players to join...".encode('utf-8')

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server fajci a posloucha")
players = []

while len(players) < 4:
    # bytesAddressPair je pole obsahující [msg, IPadres]
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    clientAdress = bytesAddressPair[1]
    msg = bytesAddressPair[0].decode('utf-8')
    if clientAdress not in players:
        players.append(clientAdress)
        print("Player joined: ", clientAdress)
        UDPServerSocket.sendto(msgToSend, clientAdress)

    # Sending a reply to client
    UDPServerSocket.sendto(msgToSend, bytesAddressPair[1])
