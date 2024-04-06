import json
import sys

import pygame
import time
from hrac import Hrac
from websockets.sync.client import connect

pygame.init()

# načtení potřebných obrázků
PLAYER_PIC = pygame.image.load("images/ninja.png")
ENEMY_PIC = pygame.image.load("images/enemy.png")
BOX_PIC = pygame.image.load("images/wooden-box.png")
GRASS_PIC = pygame.image.load("images/grass_texture.png")
GRASS_PICB = pygame.image.load("images/grass_texture_bombB.png")
GRASS_PICR = pygame.image.load("images/grass_texture_bombR.png")
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

# předdefinování hráče a bomby
P1 = Hrac(mapa, SCREEN, -50, -50)
Bomb = False

clock = pygame.time.Clock()

socket = connect("ws://localhost:8000")

cas = time.time()

# metoda posílající info o pozici hráče a vytvoření bomby
def poslat(x, y, bomba):
    socket.send(json.dumps(
        {
            "pozice": (x, y),
            "bomba": bomba
        }
    ))


# první smyčka, ve které se čeká na hráče
while True:
    SCREEN.fill((0, 0, 0))
    clock.tick(60)

    socket.send("UŽ?")
    message = socket.recv()
    if message != "CEKAME":
        print("Začínáme!")
        break

    # text
    SCREEN.blit(text_queue, (500, 500))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# inicializace hráče
Player_1 = Hrac(mapa, SCREEN, 0, 0)
bomb_at = None
jede = True
while jede:
    clock.tick(60)

    # poslech akcí okna - po zmáčknutí křížku se vypne
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jede = False
            pygame.quit()
            sys.exit()

    # načtení dat ze serveru
    socket.send("info?")
    data_json = socket.recv()
    data = json.loads(data_json)
    mapa = data["mapa"]
    Player_1.mapa = mapa

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
            if mapa[rada][sloupec] == 4:
                SCREEN.blit(GRASS_PICB, (x, y))
            if mapa[rada][sloupec] == 5:
                SCREEN.blit(GRASS_PICR, (x, y))

    pozice_hracu = data["pozice_hracu"]
    index = data["index_hrace"]
    Player_1.policko_x, Player_1.policko_y = pozice_hracu[index]
    P_X, P_Y = pozice_hracu[index]

    key = pygame.key.get_just_pressed()
    if key[pygame.K_SPACE] and Player_1.pocet_bomb > 0:
        Bomb = True
        Player_1.pocet_bomb -= 1
        bomb_at = time.time()

    if bomb_at is not None:
        print(time.time() - bomb_at)
        if time.time() - bomb_at >= 3:
            Player_1.pocet_bomb += 1
            bomb_at = None
    print(Player_1.pocet_bomb)

    Player_1.pohyb(key)

    Player_1.x, Player_1.y = Player_1.souradnice_policka(POLE_SIZE, novy_x, novy_y)
    if Player_1.zije:
        SCREEN.blit(Player_1.obr, (Player_1.x, Player_1.y))

    Player_1.smrt()

    pozice_hracu[index] = (Player_1.policko_x, Player_1.policko_y)
    for hrac in pozice_hracu:
        souradnice_x = hrac[0] * POLE_SIZE + novy_x
        souradnice_y = hrac[1] * POLE_SIZE + novy_y
        if hrac != (Player_1.policko_x, Player_1.policko_y):
            SCREEN.blit(ENEMY_PIC, (souradnice_x, souradnice_y))

    poslat(Player_1.policko_x, Player_1.policko_y, Bomb)
    Bomb = False

    pygame.display.flip()

pygame.quit()
