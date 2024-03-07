import pygame
from Button import Button

pygame.init()

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
        self.play_button = Button(500, 300, 300, 100, "Play!")

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            self.play_button.eventHandler(event)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.play_button.render(screen)


class Game(Scene):

    def __init__(self):
        super().__init__()

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()

    def render(self, screen):
        screen.fill((0, 0, 0))
