import pygame
from Button import Button, Text

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
        self.play_button = Button(1, 500, 350, 300, 100, "Play!")
        self.heading = Text(500, 200, "Bomber")

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            self.play_button.eventHandler(event)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.play_button.render(screen)
        self.heading.render(screen)


class Game(Scene):

    def __init__(self):
        super().__init__()
        self.xButton = Button(2, 1230, 0, 50, 50, "x")

    def event_handler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            self.xButton.eventHandler(event)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.xButton.render(screen)
