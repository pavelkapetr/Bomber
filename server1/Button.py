import pygame
from client import send
from prepinac_scen import set_scene, get_scene

pygame.init()
pygame.font.init()


class Button:
    def __init__(self, id, x, y, width, height, text):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.statement = 'normal'
        self.color = {
            'normal': (255, 255, 255),
            'hover': (102, 102, 102),
            'pressed': (51, 51, 51)
        }

    def eventHandler(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click()

    def hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.statement = 'hover'
        else:
            self.statement = 'normal'

    def click(self):
        self.statement = 'pressed'
        send(f"klik {self.id}")
        if get_scene() == "Menu":
            set_scene("Game")
        elif get_scene() == "Game":
            set_scene("Menu")

    def render(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 36)

        pygame.draw.rect(screen, self.color[self.statement], self.rect)

        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class Text:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def render(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 72)
        render = font.render(self.text, True, (255, 255, 255))
        screen.blit(render, (self.x, self.y))