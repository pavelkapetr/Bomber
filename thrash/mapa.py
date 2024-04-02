import pygame

pygame.init()

"""
0 = Zeď
1 = Tráva
2 = Box
3 = Tráva (momentálně probíhá výbuch)
"""

# načtení potřebných png souborů do proměnných
box_obr = pygame.image.load("../images/wooden-box.png")
trava_obr = pygame.image.load("../images/grass_texture.png")
zed_obr = pygame.image.load("../images/wall.png")
trava_vybuch_obr = pygame.image.load("../images/grass_explosion_texture.png")

# předdefinovaná mapa
mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 2, 2, 1, 1, 0],
    [0, 1, 0, 2, 0, 2, 0, 1, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 2, 2, 2, 2, 2, 2, 0],
    [0, 1, 0, 2, 0, 2, 0, 1, 0],
    [0, 1, 1, 2, 2, 2, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
