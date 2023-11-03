import pygame
from hrac import Player
import mapa

pygame.init()

pygame.display.set_icon(pygame.image.load("images/bomb.png"))
pygame.display.set_caption("Bomber")

sirka = 1920
vyska = 1140
screen = pygame.display.set_mode((sirka, vyska))
velikost_pole = 128

novy_x = (sirka - len(mapa.mapa[0]) * velikost_pole) // 2
novy_y = (vyska - len(mapa.mapa) * velikost_pole) // 2

h1 = Player()

fajci = True
while fajci:

# průchod polem mapa a vykreslení jednotlivých polí reprezentované obrázky
    for rada in range(len(mapa.mapa[0])):
        for sloupec in range(len(mapa.mapa)):
            x = rada * velikost_pole + novy_x
            y = sloupec * velikost_pole + novy_y
            if mapa.mapa[rada][sloupec] == 0:
                screen.blit(mapa.zed_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 1:
                screen.blit(mapa.trava_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 2:
                screen.blit(mapa.box_obr,(x, y))

    h1.pohyb()
    h1.souradnice_policka(velikost_pole, novy_x, novy_y)
    h1.kontrola_bomb()
    screen.blit(h1.obr, (h1.x, h1.y))

    for bomby in h1.bomby:
        bomby.fajci()
        bomby.draw(screen)
        if bomby.bum:
            bomby.vybuch(mapa.mapa)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fajci = False

    pygame.display.flip()

pygame.quit()
