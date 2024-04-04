import pygame
from Bomba import Bomba1

pygame.init()
hrac_obr = pygame.image.load("images/ninja.png")


class Hrac:
    def __init__(self, mapa, screen, spawn_x, spawn_y):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = spawn_x
        self.policko_y = spawn_y
        self.posledne = pygame.time.get_ticks()
        self.pocet_bomb = 1
        self.mapa = mapa
        self.screen = screen
        self.zije = True

    def souradnice_policka(self, velikost_policka, novy_x, novy_y):
        x = self.policko_x * velikost_policka + novy_x
        y = self.policko_y * velikost_policka + novy_y
        return x, y

    def pohyb(self, klavesa):
        # nyni = pygame.time.get_ticks()

        #print(self.policko_y, self.policko_x)
        # klavesa = pygame.key.get_pressed()
        if self.mapa is not None:
            if klavesa[pygame.K_w] and self.policko_y > 1:
                if self.mapa[self.policko_x][self.policko_y - 1] != 0 and self.mapa[self.policko_x][self.policko_y - 1] != 2:
                    self.policko_y -= 1
            elif klavesa[pygame.K_s] and self.policko_y < 7:
                if self.mapa[self.policko_x][self.policko_y + 1] != 0 and self.mapa[self.policko_x][self.policko_y + 1] != 2:
                    self.policko_y += 1
            elif klavesa[pygame.K_a] and self.policko_x > 1:
                if self.mapa[self.policko_x - 1][self.policko_y] != 0 and self.mapa[self.policko_x - 1][self.policko_y] != 2:
                    self.policko_x -= 1
            elif klavesa[pygame.K_d] and self.policko_x < 7:
                if self.mapa[self.policko_x + 1][self.policko_y] != 0 and self.mapa[self.policko_x + 1][self.policko_y] != 2:
                    self.policko_x += 1
            elif klavesa[pygame.K_SPACE] and self.pocet_bomb > 0:
                self.pocet_bomb -= 1

    # def smrt(self):



