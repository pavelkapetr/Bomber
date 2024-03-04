import socket

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

msgToSend = "Vitej na serveru ty kapino".encode('utf-8')

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server fajci a posloucha")

while True:
    # bytesAddressPair je pole obsahující [msg, IPadres]
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    print(f"{bytesAddressPair[1]}: {bytesAddressPair[0].decode('utf-8')}")
    # Sending a reply to client
    UDPServerSocket.sendto(msgToSend, bytesAddressPair[1])
