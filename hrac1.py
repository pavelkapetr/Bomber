import pygame
import mapa

pygame.init()
hrac_obr = pygame.image.load("images/ninja.png")


class Player:
    def __init__(self, mapa, screen, spawn_x, spawn_y):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = spawn_x
        self.policko_y = spawn_y
        self.posledne = pygame.time.get_ticks()
        self.cooldown = 200

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
                self.polozeno = pygame.time.get_ticks()

            self.posledne = nyni