import pygame

pygame.init()
bomba_obr1 = pygame.image.load("images/bomb.png")
bomba_obr2 = pygame.image.load("images/bomb_red.png")

class Bomba:
    def __init__(self, mapa, screen):
        self.obr = bomba_obr1
