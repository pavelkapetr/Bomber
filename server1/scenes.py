import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1120, 720))
pygame.display.set_caption("Bomber - menu")


class Scene:
    def __init__(self):
        pass

    def event_handler(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass


class Menu(Scene):
    def __init__(self):
        super().__init__()

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def render(self, screen):
        screen.fill((0, 0, 0))


class Game(Scene):

    def __init__(self):
        super().__init__()

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def render(self, screen):
        screen.fill((0, 0, 0))
