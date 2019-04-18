import pygame
from pygame.locals import *
from config import width, height
from player import Player
from ledge import Plat
from cat import Cat

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)

def main():
    player = Player(100,100)

    clock = pygame.time.Clock()

    platforms = [Plat(0,height-50,width,50),
                Plat(100,height-150, 100,20),
                Plat(300, height-150, 100,20),
                Plat(500, height-150, 100,20),
                Plat(700, height-150, 100,20),
                Plat(700, height-150, 100,20),
                Plat(200,height-250, 150,20),
                Plat(400,height-250, 150,20),
                Plat(600,height-250, 150,20)
                ]

    cats = [Cat(100,200)]

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            playing = False
        player.move(keys, platforms)
        for i in cats:
            i.move(player, platforms)

        redraw(player, platforms, cats)

def redraw(player, platforms, cats):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in cats:
        i.draw(win)
    player.draw(win)
    pygame.display.update()

main()