import pygame
import time

pygame.init()
bomba_obr1 = pygame.image.load("images/bomb.png")
bomba_obr2 = pygame.image.load("images/bomb_red.png")


class Bomba1:
    def __init__(self, spawn_x, spawn_y, dosah, cas):
        self.obr = bomba_obr1
        self.start = cas
        self.pole_x = spawn_x
        self.pole_y = spawn_y
        self.dosah = dosah
        self.zpozdeni = 1000
        self.zacatek_vybuchu = 0
        self.bum = False
        self.r_pok = True
        self.l_pok = True
        self.u_pok = True
        self.d_pok = True
        self.smrt = False
        self.bum_pole = []

    def fajci(self, mapa):
        nyni = time.time() * 1000
        if self.zpozdeni <= nyni - self.start < 2 * self.zpozdeni:
            return 4
        elif 2 * self.zpozdeni <= nyni - self.start < 3 * self.zpozdeni:
            return 5
        elif 3 * self.zpozdeni <= nyni - self.start < 4 * self.zpozdeni:
            self.bum_pole.append([self.pole_x, self.pole_y])
            self.vybuch(mapa)
            # print(self.bum_pole)
            for x, y in self.bum_pole:
                mapa[x][y] = 3
            return mapa

        elif 4 * self.zpozdeni <= nyni - self.start < 5 * self.zpozdeni:
            for x, y in self.bum_pole:
                mapa[x][y] = 1
            return mapa

    def vybuch(self, mapa):

        # expanze výbuchu doprava
        if self.r_pok:
            for i in range(1, self.dosah + 1):
                x_prav = self.pole_x + i
                if x_prav >= len(mapa) or mapa[x_prav][self.pole_y] == 0:
                    self.r_pok = False
                    break
                elif mapa[x_prav][self.pole_y] == 1:
                    print("r", [x_prav, self.pole_y])
                    self.bum_pole.append([x_prav, self.pole_y])
                elif mapa[x_prav][self.pole_y] == 2:
                    print("r", [x_prav, self.pole_y])
                    self.bum_pole.append([x_prav, self.pole_y])
                    self.r_pok = False
                    break

        # expanze výbucu doleva
        if self.l_pok:
            for i in range(-1, -self.dosah - 1, -1):
                x_lev = self.pole_x + i
                if x_lev < 0 or mapa[x_lev][self.pole_y] == 0:
                    self.l_pok = False
                    break
                elif mapa[x_lev][self.pole_y] == 1:
                    print("l", [x_lev, self.pole_y])
                    self.bum_pole.append([x_lev, self.pole_y])
                elif mapa[x_lev][self.pole_y] == 2:
                    print("l", [x_lev, self.pole_y])
                    self.bum_pole.append([x_lev, self.pole_y])
                    self.l_pok = False
                    break

        # expanze výbucu dolu
        if self.d_pok:
            for y in range(1, self.dosah + 1):
                y_dol = self.pole_y + y
                if y_dol >= len(mapa[0]) or mapa[self.pole_x][y_dol] == 0:
                    self.d_pok = False
                    break
                elif mapa[self.pole_x][y_dol] == 1:
                    print("d", [self.pole_x, y_dol])
                    self.bum_pole.append([self.pole_x, y_dol])
                elif mapa[y_dol][self.pole_x] == 2:
                    print("d", [self.pole_x, y_dol])
                    self.bum_pole.append([self.pole_x, y_dol])
                    self.d_pok = False
                    break

        # expanze výbuchu nahoru
        if self.u_pok:
            for y in range(-1, -self.dosah - 1, -1):
                y_up = self.pole_y + y
                if y_up < 0 or mapa[y_up][self.pole_x] == 0:
                    self.u_pok = False
                    break
                elif mapa[y_up][self.pole_x] == 1:
                    print("u", [y_up, self.pole_x])
                    self.bum_pole.append([y_up, self.pole_x])
                elif mapa[y_up][self.pole_x] == 2:
                    print("u", [y_up, self.pole_x])
                    self.bum_pole.append([y_up, self.pole_x])
                    self.u_pok = False
                    break
'''
    def draw(self, velikost_pole, novy_x, novy_y):
        if self.vykresluje:
            self.screen.blit(self.obr, (self.pole_x * velikost_pole + novy_x, self.pole_y * velikost_pole + novy_y))
'''
