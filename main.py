import pygame

import mapa, hrac

pygame.init()
sirka = 1920
vyska = 1080
screen = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("Bomber")
rozliseni = (800, 600)
meritko = (
    sirka / rozliseni[0],
    vyska / rozliseni[1]
)
# upravení obázků naa potřebnou velikost
velikost_policka = 256
zed_obr2 = pygame.transform.scale(mapa.zed_obr, (int(velikost_policka * meritko[0]), int(velikost_policka * meritko[1])))
trava_obr2 = pygame.transform.scale(mapa.trava_obr, (int(velikost_policka * meritko[0]), int(velikost_policka * meritko[1])))
box_obr2 = pygame.transform.scale(mapa.box_obr, (int(velikost_policka * meritko[0]), int(velikost_policka * meritko[1])))
#výpočet velikosti mapy
mapa_sirka = len(mapa.mapa[0]) * velikost_policka * meritko[0]
mapa_vyska = len(mapa.mapa) * velikost_policka * meritko[1]

#výpočet nových souřadnic x,y
novy_x = (sirka - mapa_sirka) / 2
novy_y = (vyska - mapa_vyska) / 2
Fajci = True

# hlavní loop hry
while Fajci:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Fajci = False



    for rada in range(len(mapa.mapa)):
        for sloupec in range(len(mapa.mapa[0])):
            x = rada * velikost_policka * meritko[0] + novy_x
            y = sloupec * velikost_policka * meritko[1] + novy_y
            if mapa.mapa[rada][sloupec] == 0:
                screen.blit(mapa.zed_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 1:
                screen.blit(mapa.trava_obr, (x, y))
            elif mapa.mapa[rada][sloupec] == 2:
                screen.blit(mapa.box_obr,(x, y))

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            sirka, vyska = event.dict['size']
            scale_factor = (
                sirka / rozliseni[0],
                vyska / rozliseni[1]
            )
            # Update the screen surface with the new size
            screen = pygame.display.set_mode((sirka, vyska), pygame.RESIZABLE)

    pygame.display.flip()

pygame.quit()