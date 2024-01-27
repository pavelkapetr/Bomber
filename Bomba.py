import pygame

pygame.init()
bomba_obr1 = pygame.image.load("images/bomb.png")
bomba_obr2 = pygame.image.load("images/bomb_red.png")


class Bomba1:
    def __init__(self, spawn_x, spawn_y, dosah, cas, mapa, screen):
        self.obr = bomba_obr1
        self.start = cas
        self.pole_x = spawn_x
        self.pole_y = spawn_y
        self.dosah = dosah
        self.mapa = mapa
        self.screen = screen
        self.zpozdeni = 1000
        self.zacatek_vybuchu = 0
        self.bum = False
        self.p_pok = True
        self.l_pok = True
        self.u_pok = True
        self.d_pok = True
        self.vykresluje = True
        self.bum_pole = []

    def fajci(self):
        nyni = pygame.time.get_ticks()
        if self.zpozdeni <= nyni - self.start < 2 * self.zpozdeni:
            self.obr = bomba_obr2
        elif 2 * self.zpozdeni <= nyni - self.start < 3 * self.zpozdeni:
            self.bum = True

    def vybuch(self):

        # expanze výbuchu doprava
        if self.p_pok:
            for i in range(self.dosah + 1):
                x_prav = self.pole_x + i
                if x_prav >= len(self.mapa) or self.mapa[x_prav][self.pole_y] == 0:
                    self.p_pok = False
                    break
                elif self.mapa[x_prav][self.pole_x] == 1:
                    self.mapa[x_prav][self.pole_y] = 3
                    self.bum_pole.append([x_prav, self.pole_y])
                elif self.mapa[x_prav][self.pole_y] == 2:
                    self.mapa[x_prav][self.pole_y] = 3
                    self.bum_pole.append([x_prav, self.pole_y])
                    self.p_pok = False
                    break

        # expanze výbucu doleva
        if self.l_pok:
            for i in range(-1, self.dosah - 1, -1):
                x_lev = self.pole_x + i
                if x_lev < 0 or self.mapa[x_lev][self.pole_y] == 0:
                    self.l_pok = False
                    break
                elif self.mapa[x_lev][self.pole_y] == 1:
                    self.mapa[x_lev][self.pole_y] = 3
                    self.bum_pole.append([x_lev, self.pole_y])
                elif self.mapa[x_lev][self.pole_y] == 2:
                    self.mapa[x_lev][self.pole_y] = 3
                    self.bum_pole.append([x_lev, self.pole_y])
                    self.l_pok = False
                    break

        # expanze výbucu dolu
        if self.d_pok:
            for y in range(1, self.dosah +1):
                y_dol = self.pole_y + y
                if y_dol >= len(self.mapa[0]) or self.mapa[self.pole_x][y_dol] == 0:
                    self.d_pok = False
                    break
                elif self.mapa[self.pole_x][y_dol] == 1:
                    self.mapa[self.pole_x][y_dol] = 3
                    self.bum_pole.append([self.pole_x, y_dol])
                elif self.mapa[self.pole_x][y_dol] == 2:
                    self.mapa[self.pole_x][y_dol] = 3
                    self.bum_pole.append([self.pole_x, y_dol])
                    self.d_pok = False
                    break

        # expanze výbuchu nahoru
        if self.u_pok:
            for y in range(-1, self.dosah - 1, -1):
                y_up = self.pole_y + y
                if y_up < 0 or self.mapa[self.pole_x][y_up] == 0:
                    self.u_pok = False
                    break
                elif self.mapa[self.pole_x][y_up] == 1:
                    self.mapa[self.pole_x][y_up] = 3
                    self.bum_pole.append([self.pole_x, y_up])
                elif self.mapa[self.pole_x][y_up] == 2:
                    self.mapa[self.pole_x][y_up] = 3
                    self.bum_pole.append([self.pole_x, y_up])
                    self.u_pok= False
                    break

    def draw(self, velikost_pole, novy_x, novy_y):
        print(self.pole_x)
        self.screen.blit(self.obr, (self.pole_x * velikost_pole + novy_x, self.pole_y * velikost_pole + novy_y))
