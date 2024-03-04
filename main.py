import pygame
import mapa
from hrac import Hrac

pygame.init()

# nastavení okna
pygame.display.set_icon(pygame.image.load("images/bomb.png"))
pygame.display.set_caption("Bomber")

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

# hlavní loop hry
fajci = True
while fajci:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fajci = False

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

    # poslouchání mezerníkú -> položení bomby
    k = pygame.key.get_pressed()
    if k[pygame.K_SPACE] and h1.pocet_bomb > 0:
        h1.pocet_bomb -= 1
        x = h1.vytvor_bombu()
        bomb.append(x)

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
