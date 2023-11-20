import pygame
import mapa

pygame.init()

hrac_obr = pygame.image.load("images/ninja.png")
bomba1_obr = pygame.image.load("images/bomb.png")
bomba2_obr = pygame.image.load("images/bomb_red.png")
exploze = pygame.image.load("images/explosion.png")


class Player:
    def __init__(self, mapa, screen):
        self.obr = hrac_obr
        self.x = 0
        self.y = 0
        self.policko_x = 1
        self.policko_y = 1
        self.posledne = pygame.time.get_ticks()
        self.cooldown = 100
        self.pocet_bomb = 1
        self.bomby = []
        self.dosah = 1
        self.bumbumbox = []
        self.mapa = mapa
        self.screen = screen

    def souradnice_policka(self, velikost_policka, novy_x, novy_y):
        x = self.policko_x * velikost_policka + novy_x
        y = self.policko_y * velikost_policka + novy_y
        return (x, y)

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
        bomba = Bomba(bomba_x, bomba_y, self.dosah, self.policko_x, self.policko_y, self.mapa, self.screen)
        self.bomby.append(bomba)

    def kontrola_bomb(self):
        nyni = pygame.time.get_ticks()
        k_odstraneni = []

        for bomba in self.bomby:
            if bomba.bum:
                if nyni - bomba.pocatek >= 3 * bomba.zpozdeni:
                    k_odstraneni.append(bomba)
                    self.pocet_bomb += 1
                    for i in range(bomba.policko_x - bomba.dosah, bomba.policko_x + bomba.dosah + 1):
                        for j in range(bomba.policko_y - bomba.dosah, bomba.policko_y + bomba.dosah + 1):
                            if (
                                    0 <= i < len(self.mapa) and 0 <= j < len(self.mapa[0])
                                    and (i != bomba.policko_x or j != bomba.policko_y)
                            ):
                                if self.mapa[i][j] == 2 or self.mapa[i][j] == 1:
                                    self.bumbumbox.append((i, j, nyni))
            else:
                bomba.fajci()
        for bomba in k_odstraneni:
            self.bomby.remove(bomba)


class Bomba(Player):
    def __init__(self, x, y, dosah, policko_x, policko_y, mapa, screen):
        super().__init__(mapa, screen)
        self.obr = bomba1_obr
        self.x = x
        self.y = y
        self.policko_x = policko_x
        self.policko_y = policko_y
        self.bum = False
        self.dosah = dosah
        self.zpozdeni = 1000
        self.pocatek = pygame.time.get_ticks()

    def fajci(self):
        nyni = pygame.time.get_ticks()
        if nyni - self.pocatek >= self.zpozdeni:
            self.obr = bomba2_obr
        if nyni - self.pocatek >= 2 * self.zpozdeni:
            self.obr = exploze
            self.bum = True

    def vybuch(self, mapa):
        if self.bum:
            self.zacatek_vybuchu = pygame.time.get_ticks()

            # expanze výbuchu doprava
            for dx in range(1, self.dosah + 1):
                i = self.policko_x + dx
                if i >= len(mapa) or mapa[i][self.policko_y] == 0:
                    break
                if mapa[i][self.policko_y] == 2:
                    mapa[i][self.policko_y] = 1
                    break
                self.screen.blit(exploze,((i * 128 + 384), (self.policko_y * 128 + (-6))))

            #expanze výbuchu doleva
            for dx in range(-1, -self.dosah - 1, -1):
                i = self.policko_x + dx
                if i < 0 or mapa[i][self.policko_y] == 0:
                    break
                if mapa[i][self.policko_y] == 2:
                    mapa[i][self.policko_y] = 1
                    break
                self.screen.blit(exploze, ((i * 128 + 384), (self.policko_y * 128 + (-6))))

            #expanze výbuchu dolů
            for dy in range(1, self.dosah + 1):
                j = self.policko_y + dy
                if j >= len(mapa[0]) or mapa[self.policko_x][j] == 0:
                    break
                if mapa[self.policko_x][j] == 2:
                    mapa[self.policko_x][j] = 1
                    break
                self.screen.blit(exploze, ((self.policko_x * 128 + 384), (j * 128 + (-6))))

            #expanze výbuchu nahorů
            for dy in range(-1, -self.dosah - 1, -1):
                j = self.policko_y + dy
                if j < 0 or mapa[self.policko_x][j] == 0:
                    break
                if mapa[self.policko_x][j] == 2:
                    mapa[self.policko_x][j] = 1
                    break
                self.screen.blit(exploze, ((self.policko_x * 128 + 384), (j * 128 + (-6))))

    def draw(self):
        if self.obr == bomba1_obr or self.obr == bomba2_obr:
            self.screen.blit(self.obr, (self.x + 28, self.y + 14))
        else:
            self.screen.blit(self.obr, (self.x, self.y))
