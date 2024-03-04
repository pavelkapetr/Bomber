import socket

msgProServer = "Cau UDP Server".encode('utf-8')

serverAddress_Port = ("127.0.0.1", 20001)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(msgProServer, serverAddress_Port)

msgOdServer = UDPClientSocket.recvfrom(bufferSize)
msg = f"Message from Server {msgOdServer[0].decode('utf-8')}"
print(msg)
