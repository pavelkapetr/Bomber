import pygame
import mapa

pygame.init()

hrac_obr = pygame.image.load("images/ninja.png")

class Player:
    def __init__(self):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = 1
        self.policko_y = 1
        self.posledne = pygame.time.get_ticks()
        self.cooldown = 100
    def souradnice_policka(self, velikost_policka, novy_x, novy_y):
        self.x = self.policko_x * velikost_policka + novy_x
        self.y = self.policko_y * velikost_policka + novy_y

    def pohyb(self):
        nyni = pygame.time.get_ticks()

        if nyni - self.posledne >= self.cooldown:
            klavesa = pygame.key.get_pressed()

            if klavesa[pygame.K_w] and self.policko_y > 1:
                if mapa.mapa[self.policko_x][self.policko_y - 1] != 0 and mapa.mapa[self.policko_x][self.policko_y - 1] != 2:
                    self.policko_y -= 1
            elif klavesa[pygame.K_s] and self.policko_y < 7:
                if mapa.mapa[self.policko_x][self.policko_y + 1] != 0 and mapa.mapa[self.policko_x][self.policko_y + 1] != 2:
                    self.policko_y += 1
            elif klavesa[pygame.K_a] and self.policko_x > 1:
                if mapa.mapa[self.policko_x - 1][self.policko_y] != 0 and mapa.mapa[self.policko_x - 1][self.policko_y] != 2:
                    self.policko_x -= 1
            elif klavesa[pygame.K_d] and self.policko_x < 7:
                if mapa.mapa[self.policko_x + 1][self.policko_y] != 0 and mapa.mapa[self.policko_x + 1][self.policko_y] != 2:
                    self.policko_x += 1

            self.posledne = nyni