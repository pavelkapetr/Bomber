import pygame
import mapa

pygame.init()

hrac_obr = pygame.image.load("images/ninja.png")
bomba1_obr = pygame.image.load("images/bomb.png")
bomba2_obr = pygame.image.load("images/bomb_red.png")
exploze = pygame.image.load("images/explosion.png")

class Player:
    def __init__(self):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = 1
        self.policko_y = 1
        self.posledne = pygame.time.get_ticks()
        self.cooldown = 100
        self.pocet_bomb = 1
        self.bomby = []
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
            elif klavesa[pygame.K_SPACE] and self.pocet_bomb > 0:
                self.vytvor_bombu()
                self.pocet_bomb -= 1

            self.posledne = nyni

    def vytvor_bombu(self):
        bomba_x = self.x
        bomba_y = self.y
        bomba = Bomba(bomba_x, bomba_y)
        self.bomby.append(bomba)

    def kontrola_bomb(self):
        nyni = pygame.time.get_ticks()
        k_odstraneni = []

        for bomba in self.bomby:
            if bomba.bum:
                if nyni - bomba.pocatek >= 3 * bomba.zpozdeni:
                    k_odstraneni.append(bomba)
                    self.pocet_bomb += 1
            else:
                bomba.fajci()
        for bomba in k_odstraneni:
            self.bomby.remove(bomba)

class Bomba:
    def __init__(self, x, y):
        self.obr = bomba1_obr
        self.x = x
        self.y = y
        self.bum = False
        self.zpozdeni = 1000
        self.pocatek = pygame.time.get_ticks()

    def fajci(self):
        nyni = pygame.time.get_ticks()
        if nyni - self.pocatek >= self.zpozdeni:
            self.obr = bomba2_obr
        if nyni - self.pocatek >= 2 * self.zpozdeni:
            self.obr = exploze
            self.bum = True


    def draw(self, screen):
        screen.blit(self.obr, (self.x + 28, self.y + 14))