import json
import sys

import pygame
from hrac import Hrac
from Bomba import Bomba1
from websockets.sync.client import connect
from client import msg

pygame.init()

# načtení potřebných obrázků
PLAYER_PIC = pygame.image.load("images/ninja.png")
ENEMY_PIC = pygame.image.load("images/enemy.png")
BOX_PIC = pygame.image.load("images/wooden-box.png")
GRASS_PIC = pygame.image.load("images/grass_texture.png")
WALL_PIC = pygame.image.load("images/wall.png")
EXP_GRASS_PIC = pygame.image.load("images/grass_explosion_texture.png")

# nastavení okna
pygame.display.set_icon(pygame.image.load("images/bomb.png"))
pygame.display.set_caption("Bomber")

# definování fontu a render textu
font = pygame.font.Font('freesansbold.ttf', 72)
text_queue = font.render("Waiting for players...", True, (255, 255, 255))

# nastavení velikosti okna
WIDTH = 1920
HEIGHT = 1140
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# nastavení veliskosti jednoho políčka a výpočet nových x a y aby hra byla na středu okna
POLE_SIZE = 128
mapa = None

# předdefinování hráče a pole bomb
P1 = Hrac(mapa, SCREEN, -50, -50)
bombs = []
mybomb = None

clock = pygame.time.Clock()

socket = connect("ws://localhost:8001")

def poslat(x, y, bomba=None):
    if bomba is None:
        socket.send(json.dumps(
            {
                "pozice" : (x, y),
                "bomby" : None
            }
        ))
    else:
        socket.send(json.dumps(
            {
                "pozice" : (x, y),
                "bomby" : (bomba.pole_x, bomba.pole_y, bomba.zacatek_vybuchu)
            }
        ))

while True:
    SCREEN.fill((0, 0, 0))
    clock.tick(59)

    socket.send("UŽ?")
    message = socket.recv()
    print(message)
    if message != "CEKAME":
        break

    # text
    SCREEN.blit(text_queue, (500, 500))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

jede = True
while jede:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jede = False
            pygame.quit()
            sys.exit()

    socket.send("info?")
    data_json = socket.recv()
    data = json.loads(data_json)
    mapa = data["mapa"]
    print(mapa)

    SCREEN.fill((0, 0, 0))
    # vykreslení mapy
    novy_x = (WIDTH - len(mapa) * POLE_SIZE) // 2
    novy_y = (HEIGHT - len(mapa[0]) * POLE_SIZE) // 2
    for rada in range(len(mapa)):
        for sloupec in range(len(mapa[0])):
            x = rada * POLE_SIZE + novy_x
            y = sloupec * POLE_SIZE + novy_y
            if mapa[rada][sloupec] == 0:
                SCREEN.blit(WALL_PIC, (x, y))
            if mapa[rada][sloupec] == 1:
                SCREEN.blit(GRASS_PIC, (x, y))
            if mapa[rada][sloupec] == 2:
                SCREEN.blit(BOX_PIC, (x, y))
            if mapa[rada][sloupec] == 3:
                SCREEN.blit(EXP_GRASS_PIC, (x, y))

    pozice_hracu = data["pozice_hracu"]
    index = data["index_hrace"]
    P_X, P_Y = pozice_hracu[index]

    key = pygame.key.get_just_pressed()
    if key[pygame.K_w] and P_Y > 1:
        if mapa[P_Y-1][P_X] != 0 and mapa[P_Y-1][P_X] != 2:
            P_Y -= 1
    elif key[pygame.K_s] and P_Y < 7:
        if mapa[P_Y+1][P_X] != 0 and mapa[P_Y+1][P_X] != 2:
            P_Y += 1
    elif key[pygame.K_a] and P_X > 1:
        if mapa[P_Y][P_X-1] != 0 and mapa[P_Y][P_X-1] != 2:
            P_X -= 1
    elif key[pygame.K_d] and P_X < 7:
        if mapa[P_Y][P_X+1] !=0 and mapa[P_Y][P_X+1] != 2:
            P_X += 1
    elif key[pygame.K_SPACE]:
        DE_START = pygame.time.get_ticks()
        bomba = Bomba1(P_X, P_Y, 1, DE_START, mapa, SCREEN)
        bombs.append(bomba)
        mybomb = bomba

    pozice_hracu[index] = (P_X, P_Y)
    for hrac in pozice_hracu:
        souradnice_x = hrac[0] * POLE_SIZE + novy_x
        souradnice_y = hrac[1] * POLE_SIZE + novy_y
        if hrac == (P_X, P_Y):
            SCREEN.blit(PLAYER_PIC, (souradnice_x, souradnice_y))
        else:
            SCREEN.blit(ENEMY_PIC, (souradnice_x, souradnice_y))

    for bomb in bombs:
        bomb.fajci()
        bomb.draw(POLE_SIZE, novy_x, novy_y)

    if len(bombs) >= 0:
        poslat(P_X, P_Y, mybomb)
    else:
        poslat(P_X, P_Y)

    pygame.display.flip()

pygame.quit()




'''
# hlavní loop hry
h1 = Hrac(mapa, screen, 1, 1)
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
'''


