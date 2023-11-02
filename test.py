import pygame
from hrac import Player
import mapa

pygame.init()

sirka = 1920
vyska = 1080
screen = pygame.display.set_mode((sirka, vyska))
velikost_pole = 128

h1 = Player(100, 100)

novy_x = (sirka - len(mapa.mapa[0]) * velikost_pole) // 2
novy_y = (vyska - len(mapa.mapa) * velikost_pole) // 2

fajci = True

while fajci:


    screen.blit(h1.obr, (h1.x, h1.y))

    for rada in range(len(mapa.mapa)):
        for sloupec in range(len(mapa.mapa[0])):
            x = rada * velikost_pole + novy_x
            y = sloupec * velikost_pole + novy_y
            if mapa.mapa[rada][sloupec] == 0:
                screen.blit(mapa.zed_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 1:
                screen.blit(mapa.trava_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 2:
                screen.blit(mapa.box_obr,(x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fajci = False

    pygame.display.flip()

pygame.quit()
