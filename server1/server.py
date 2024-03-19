import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

msgToSend = "Waiting for players to join.."

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print(msgToSend)
players = []

while len(players) < 2:
    # bytesAddressPair je pole obsahující [msg, IPadres]
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    clientAdress = bytesAddressPair[1]
    msg = bytesAddressPair[0].decode('utf-8')
    if clientAdress not in players:
        players.append(clientAdress)
        print("Player joined: ", clientAdress)
        UDPServerSocket.sendto(msgToSend.encode('utf-8'), clientAdress)

print("All players has joined. Starting the game!")
for player in players:
    UDPServerSocket.sendto("Game is starting".encode('utf-8'), player)

UDPServerSocket.close()
