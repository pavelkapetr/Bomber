import pygame
from scenes import Menu, Game
from client import receive, send

pygame.init()

# nastavení ikony a nadpisu okna
pygame.display.set_icon(pygame.image.load(r"images/bomb.png"))
pygame.display.set_caption("Bomber")

# nastavení velikosti okna
sirka = 1280
vyska = 720
screen = pygame.display.set_mode((sirka, vyska))

currentScene = Menu()
running = True
while running:
    events = pygame.event.get()
    currentScene.event_handler(events)

    currentScene.update()
    currentScene.render(screen)

    pygame.display.flip()

pygame.quit()
