import pygame

pygame.init()

hrac_obr = pygame.image.load("images/ninja.png")

class Player:
    def __init__(self, x, y):
        self.obr = hrac_obr
        self.x = x
        self.y = y

