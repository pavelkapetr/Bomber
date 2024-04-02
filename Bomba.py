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
        self.p_pok = True
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
            mapa = self.vybuch(mapa)
            for x, y in self.bum_pole:
                mapa[x][y] = 1
            return mapa

    def vybuch(self, mapa):

        # expanze výbuchu doprava
        if self.p_pok:
            for i in range(self.dosah + 1):
                x_prav = self.pole_x + i
                if x_prav >= len(mapa) or mapa[self.pole_y][x_prav] == 0:
                    self.p_pok = False
                    break
                elif mapa[self.pole_y][x_prav] == 1:
                    mapa[self.pole_y][x_prav] = 3
                    self.bum_pole.append([self.pole_y, x_prav])
                elif mapa[self.pole_y][x_prav] == 2:
                    mapa[self.pole_y][x_prav] = 3
                    self.bum_pole.append([self.pole_y, x_prav])
                    self.p_pok = False
                    break

        # expanze výbucu doleva
        if self.l_pok:
            for i in range(-1, -self.dosah - 1, -1):
                x_lev = self.pole_x + i
                if x_lev < 0 or mapa[self.pole_y][x_lev] == 0:
                    self.l_pok = False
                    break
                elif mapa[self.pole_y][x_lev] == 1:
                    mapa[self.pole_y][x_lev] = 3
                    self.bum_pole.append([x_lev, self.pole_y])
                elif mapa[self.pole_y][x_lev] == 2:
                    mapa[self.pole_y][x_lev] = 3
                    self.bum_pole.append([self.pole_y, x_lev])
                    self.l_pok = False
                    break

        # expanze výbucu dolu
        if self.d_pok:
            for y in range(1, self.dosah + 1):
                y_dol = self.pole_y + y
                if y_dol >= len(mapa[0]) or mapa[y_dol][self.pole_x] == 0:
                    self.d_pok = False
                    break
                elif mapa[y_dol][self.pole_x] == 1:
                    mapa[y_dol][self.pole_x] = 3
                    self.bum_pole.append([y_dol, self.pole_x])
                elif mapa[y_dol][self.pole_x] == 2:
                    mapa[y_dol][self.pole_x] = 3
                    self.bum_pole.append([y_dol, self.pole_x])
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
                    mapa[y_up][self.pole_x] = 3
                    self.bum_pole.append([y_up, self.pole_x])
                elif mapa[y_up][self.pole_x] == 2:
                    mapa[y_up][self.pole_x] = 3
                    self.bum_pole.append([self.pole_x, y_up])
                    self.bum_pole.append([y_up, ])
                    self.u_pok = False
                    break
        print(self.bum_pole)
        return mapa
'''
    def draw(self, velikost_pole, novy_x, novy_y):
        if self.vykresluje:
            self.screen.blit(self.obr, (self.pole_x * velikost_pole + novy_x, self.pole_y * velikost_pole + novy_y))
'''
