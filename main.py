import pygame
from pygame.locals import *
from config import width, height
from player import Player
from ledge import Plat
from cat import Cat
from random import randint
import time

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('if u r reading this ur dumb')

def main():
    player = Player(width/2,100)

    clock = pygame.time.Clock()

    platforms = getPlatforms()

    cats = [Cat(randint(0,width),200)]
    
    click1 = 0
    click2 = 0

    playing = True
    tStart = time.time()
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONUP:
                if click1 == 0:
                    click1 = pygame.mouse.get_pos()
                else:
                    click2 = pygame.mouse.get_pos()
                    platforms.append(Plat(click1[0], click1[1], click1[0]-click1[0], click2[1]-click1[1]))
                    click1 = 0
        clock.tick(60)

        if time.time() - tStart > 3:
            cats.append(Cat(randint(0,width), 100))
            tStart = time.time()
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            playing = False
            for i in platforms:
                print('Plat'+str((i.x, i.y, i.w, i.h)))
        player.move(keys, platforms)
        for i in cats:
            i.move(player, platforms)
            for x in player.shots:
                if x.x < i.x+i.w/2-60 and x.x > i.x-i.w/2+60 and x.y < i.y and x.y > i.y-i.h:
                    i.health -= 3  
                    if i.health <= 0:
                        if i in cats:
                            cats.remove(i)
                    player.shots.remove(x)
            if abs(i.x-player.x) < 100 and abs(i.y-player.y) < 50:
                player.health -= .5

        redraw(player, platforms, cats)

def redraw(player, platforms, cats):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in cats:
        i.draw(win)
    player.draw(win)
    pygame.display.update()

def getPlatforms():
    possible = []
    layout = [
        Plat(0, 550, 1000, 50),
        Plat(204, 433, 651, 31),
        Plat(418, 306, 356, 50),
        Plat(560, 207, 169, 25),
        Plat(645, 124, 46, 8),
        Plat(125, 219, 184, 45)
    ]
    possible.append(layout)
    layout = [
        Plat(0, 550, 1000, 50),
        Plat(3, 2, 990, 246),
        Plat(26, 428, 189, 30),
        Plat(419, 428, 189, 30),
        Plat(736, 428, 189, 30)
    ]
    possible.append(layout)
    layout = [
        Plat(0, 550, 1000, 50),
        Plat(100,height-150, 100,20),
        Plat(300, height-150, 100,20),
        Plat(500, height-150, 100,20),
        Plat(700, height-150, 100,20),
        Plat(700, height-150, 100,20),
        Plat(200,height-250, 150,20),
        Plat(400,height-250, 150,20),
        Plat(600,height-250, 150,20)
    ]
    possible.append(layout)

    return possible[randint(0,len(possible)-1)]


main()