import pygame
from hrac import Player
import mapa

pygame.init()

pygame.display.set_icon(pygame.image.load("images/bomb.png"))
exploze = pygame.image.load("images/explosion.png")
pygame.display.set_caption("Bomber")

sirka = 1920
vyska = 1140
screen = pygame.display.set_mode((sirka, vyska))

velikost_pole = 128
novy_x = (sirka - len(mapa.mapa[0]) * velikost_pole) // 2
novy_y = (vyska - len(mapa.mapa) * velikost_pole) // 2

h1 = Player(mapa.mapa, screen)

fajci = True
while fajci:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fajci = False

    #vyčištění plochy
    screen.fill((0, 0, 0))

    # projde mapu a vyakreslí jednotlivé prvky jako reprezentované obrázky
    for rada in range(len(mapa.mapa[0])):
        for sloupec in range(len(mapa.mapa)):
            x = rada * velikost_pole + novy_x
            y = sloupec * velikost_pole + novy_y
            if mapa.mapa[rada][sloupec] == 0:
                screen.blit(mapa.zed_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 1:
                screen.blit(mapa.trava_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 2:
                screen.blit(mapa.box_obr, (x, y))

    # projde všechny bomby a upraví jejich stav
    for bomby in h1.bomby:
        if bomby.bum:
            bomby.vybuch(mapa.mapa)

        bomby.fajci()
        bomby.draw()
        for x, y in bomby.odbouchnuto:
            screen.blit(exploze, (x, y))

    h1.pohyb()
    h1.x, h1.y = h1.souradnice_policka(velikost_pole, novy_x, novy_y)
    h1.kontrola_bomb()
    screen.blit(h1.obr, (h1.x, h1.y))

    pygame.display.flip()

pygame.quit()
