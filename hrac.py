import pygame
import mapa
from Bomba import Bomba1

pygame.init()
hrac_obr = pygame.image.load("server1/images/ninja.png")


class Hrac:
    def __init__(self, mapa, screen, spawn_x, spawn_y):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = spawn_x
        self.policko_y = spawn_y
        self.posledne = pygame.time.get_ticks()
        self.pocet_bomb = 2
        self.cooldown = 200
        self.dosah = 2
        self.mapa = mapa
        self.screen = screen
        self.zije = True

    def souradnice_policka(self, velikost_policka, novy_x, novy_y):
        x = self.policko_x * velikost_policka + novy_x
        y = self.policko_y * velikost_policka + novy_y
        return x, y

    def pohyb(self):
        # nyni = pygame.time.get_ticks()

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
        elif klavesa[pygame.K_SPACE] and self.pocet_bomb > 0:
            self.vytvor_bombu()
            self.pocet_bomb -= 1

        # self.posledne = nyni

    def vytvor_bombu(self):
        cas = pygame.time.get_ticks()
        bomba = Bomba1(self.policko_x, self.policko_y, self.dosah, cas, self.mapa, self.screen)
        return bomba

    def smrt (self):
        if self.mapa[self.policko_x][self.policko_y] == 3:
            self.zije = False
