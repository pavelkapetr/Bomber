import pygame
from scenes import Menu, Matchmaking
from client import receive, send
from prepinac_scen import get_scene

pygame.init()

# nastavení ikony a nadpisu okna
pygame.display.set_icon(pygame.image.load(r".\images\bomb.png"))
pygame.display.set_caption("Bomber")

# nastavení velikosti okna
sirka = 1280
vyska = 720
screen = pygame.display.set_mode((sirka, vyska))

currentScene = Menu()
running = True
while running:

    if get_scene() == "Game" and not isinstance(get_scene(), Matchmaking):
        currentScene = Matchmaking()
    elif get_scene() == "Menu" and not isinstance(get_scene(), Menu):
        currentScene = Menu()

    events = pygame.event.get()

    currentScene.event_handler(events)

    currentScene.update()
    currentScene.render(screen)

    pygame.display.flip()

pygame.quit()
