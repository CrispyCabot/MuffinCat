import pygame
from pygame.locals import *
from config import width, height
from player import Player
from ledge import Plat
from cat import Cat
from random import randint
from enemy import Lobster
import time

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('if u r reading this ur dumb')

def main():
    player = Player(width/2,100)

    clock = pygame.time.Clock()

    platMap = [getPlatforms(-width), getPlatforms(), getPlatforms(width)]
    
    platforms = []
    enemies = []
    for i in platMap[0][0]:
        platforms.append(i)
    for i in platMap[0][1]:
        enemies.append(i)
    for i in platMap[1][0]:
        platforms.append(i)
    for i in platMap[1][1]:
        enemies.append(i)
    for i in platMap[2][0]:
        platforms.append(i)
    for i in platMap[2][1]:
        enemies.append(i)
    
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

        platforms, enemies = checkPlatforms(platMap, platforms, player)
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            playing = False
            for i in platforms:
                print('Plat'+str((i.x, i.y, i.w, i.h)))
            return False
        if keys[K_r]:
            return True
        movement = player.move(keys, platforms)
        for i in platforms:
            for x in movement:
                i.x += x
        for i in enemies:
            for x in movement:
                i.x += x

        redraw(player, platforms, enemies, movement)

def redraw(player, platforms, enemies, movement):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player)
    player.draw(win, movement)
    pygame.display.update()

def getPlatforms(x=0):
    return [Plat(0+x, 550, 1000, 50)], [Lobster(200+x,500)]
    possible = []
    enemies = []
    layout = [
        Plat(0+x, 550, 1000, 50),
        Plat(204+x, 433, 651, 31),
        Plat(418+x, 306, 356, 50),
        Plat(560+x, 207, 169, 25),
        Plat(645+x, 124, 46, 8),
        Plat(125+x, 219, 184, 45)
    ]
    possible.append((layout, enemies))
    layout = [
        Plat(0+x, 550, 1000, 50),
        Plat(3+x, 2, 990, 246),
        Plat(26+x, 428, 189, 30),
        Plat(419+x, 428, 189, 30),
        Plat(736+x, 428, 189, 30)
    ]
    possible.append((layout, enemies))
    layout = [
        Plat(0+x, 550, 1000, 50),
        Plat(100+x,height-150, 100,20),
        Plat(300+x, height-150, 100,20),
        Plat(500+x, height-150, 100,20),
        Plat(700+x, height-150, 100,20),
        Plat(700+x, height-150, 100,20),
        Plat(200+x,height-250, 150,20),
        Plat(400+x,height-250, 150,20),
        Plat(600+x,height-250, 150,20)
    ]

    possible.append((layout, enemies))
    layout = [Plat(0+x, 550, 1000, 50)]
    possible.append((layout, enemies))

    val = possible[randint(0,len(possible)-1)]
    return val[0], val[1]

def checkPlatforms(platMap, platforms, player):
    pos = round(player.relativeX / width)
    pos += 1
    plats = []
    enemies = []
    try:
        for i in platMap[pos-1][0]:
            plats.append(i)
        for i in platMap[pos-1][1]:
            enemies.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos][0]:
            plats.append(i)
        for i in platMap[pos][1]:
            enemies.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos+1][0]:
            plats.append(i)
        for i in platMap[pos+1][1]:
            enemies.append(i)
    except IndexError:
        platMap.append(getPlatforms(width))
        for i in platMap[pos+1][0]:
            plats.append(i)
        for i in platMap[pos+1][1]:
            enemies.append(i)
    return plats, enemies


while main():
    main()