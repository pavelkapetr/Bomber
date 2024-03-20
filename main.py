import sys

import pygame
import mapa
from hrac import Hrac
from websockets.sync.client import connect
from client import msg

pygame.init()

# nastavení okna
pygame.display.set_icon(pygame.image.load("server1/images/bomb.png"))
pygame.display.set_caption("Bomber")
font = pygame.font.Font('freesansbold.ttf', 72)
text_queue = font.render("Waiting for players...", True, (255, 255, 255))

# nastavení velikosti okna
sirka = 1920
vyska = 1140
screen = pygame.display.set_mode((sirka, vyska))

# nastavení veliskosti jednoho políčka a výpočet nových x a y aby hra byla na středu okna
velikost_pole = 128
novy_x = (sirka - len(mapa.mapa[0]) * velikost_pole) // 2
novy_y = (vyska - len(mapa.mapa) * velikost_pole) // 2

# předdefinování hráče a pole bomb
h1 = Hrac(mapa.mapa, screen, 1, 1)
bomb = []

clock = pygame.time.Clock()

socket = connect("ws://localhost:8000")

while True:
    print("tvoja matka")
    screen.fill((0, 0, 0))
    clock.tick(60)

    socket.send("UŽ?")
    message = socket.recv()
    if message == "ZACINAME":
        break

    # text
    screen.blit(text_queue, (500, 500))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# hlavní loop hry
fajci = True
while fajci:

    # komunikace se serverem
    bomba_x, bomba_y = -1, -1
    if len(bomb) != 0:
        bomba_x, bomba_y = bomb[0].pole_x, bomb[0].pole_y
    data = {"hrac": (h1.x, h1.y), "bomba": (bomba_x, bomba_y)}
    # mapa, ostatni_hraci, ostatni_bomby = msg(socket, data)
    msg(socket, data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fajci = False

    # poslouchání mezerníkú -> položení bomby
    k = pygame.key.get_pressed()
    if k[pygame.K_SPACE] and h1.pocet_bomb > 0:
        h1.pocet_bomb -= 1
        x = h1.vytvor_bombu()
        bomb.append(x)

    # vyčištění plochy
    screen.fill((0, 0, 0))

    # projde mapu a vyakreslí jednotlivé prvky jako reprezentované obrázky
    for rada in range(len(mapa.mapa[0])):
        for sloupec in range(len(mapa.mapa)):
            x = rada * velikost_pole + novy_x
            y = sloupec * velikost_pole + novy_y
            if mapa.mapa[rada][sloupec] == 0:
                screen.blit(mapa.zed_obr, (x, y))
            if mapa.mapa[rada][sloupec] == 1:
                screen.blit(mapa.trava_obr, (x, y))
            if mapa.mapa[rada][sloupec] == 2:
                screen.blit(mapa.box_obr, (x, y))
            if mapa.mapa[rada][sloupec] == 3:
                screen.blit(mapa.trava_vybuch_obr, (x, y))

    # projde všechny bomby a zavolá potřebné metody pro chod
    for b in bomb:
        b.fajci()
        b.draw(velikost_pole, novy_x, novy_y)
        if b.smrt:
            bomb.remove(b)
            h1.pocet_bomb += 1
            print("BUM!")

    # volání metod ke správné funkci postavy
    h1.pohyb()
    h1.x, h1.y = h1.souradnice_policka(velikost_pole, novy_x, novy_y)
    if h1.zije:
        screen.blit(h1.obr, (h1.x, h1.y))
    h1.smrt()

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
