import socket
import pygame
from server1.scenes import Menu, Game

# inicializace pygame
pygame.init()

# nastavení ikony a nadpisu okna
pygame.display.set_icon(pygame.image.load(r"C:/Bomber/images/bomb.png"))
pygame.display.set_caption("Bomber")

# nastavení velikosti okna
sirka = 1280
vyska = 720
screen = pygame.display.set_mode((sirka, vyska))

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


currentScene = Menu()
running = True
while running:
    events = pygame.event.get()
    currentScene.event_handler(events)

    currentScene.update()
    currentScene.render(screen)

    send("menu")
    received = receive()
    print(received)

    pygame.display.flip()

pygame.quit()
