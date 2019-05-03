import pygame
from pygame.locals import *
from config import width, height
from player import Player
from ledge import Plat
from cat import Cat
from random import randint
from enemy import Lobster, Spider
import time

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('if u r reading this ur dumb')

def main():
    player = Player(width/2,100)

    clock = pygame.time.Clock()

    platMap = [getPlatforms(-width), getPlatforms()]
    
    platforms = []
    enemies = []

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        clock.tick(60)

        platforms, enemies = checkPlatforms(platMap, enemies, player)
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            playing = False
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

        for i in player.shots:
            if i.x > width+20 or i.x < -20:
                player.shots.remove(i)
                break
            for x in enemies:
                if i.x < x.x+x.w/2 and i.x > x.x-x.w/2 and i.y < x.y and i.y > x.y-x.h:
                    x.health -= 5
                    player.shots.remove(i)
                    if x.health < 0:
                        enemies.remove(x)
                    break
        for i in enemies:
            for x in i.shots:
                if x.x > width+20 or x.x < -20:
                    i.shots.remove(x)
                    continue
                if x.x > player.x-50 and x.x < player.x+50 and x.y < player.y and x.y > player.y - player.h:
                    player.health -= 5
                    i.shots.remove(x)

        redraw(player, platforms, enemies, movement)

def redraw(player, platforms, enemies, movement):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, movement)
    player.draw(win, movement)
    pygame.display.update()

def getPlatforms(x=0):
   # return [Plat(0+x, 550, 1000, 50)], [Lobster(200+x,520), Spider(400+x, 520)]
    possible = []
    enemies = []

    layout = [
        Plat(x+52,456,882,111)
        ]
    enemies = [
        Spider(861+x, 422),
        Lobster(448+x, 418),
        Lobster(581+x, 413)
        ]
    possible.append((layout, enemies))

    layout = [
        Plat(x+17,506,971,68),
        Plat(x+101,423,806,34),
        Plat(x+190,341,648,25),
        Plat(x+284,269,487,38),
        Plat(x+358,196,350,33),
        Plat(x+435,143,223,23),
        Plat(x+491,74,123,19)
        ]
    enemies = [
        Lobster(551+x, 45),
        Spider(617+x, 117),
        Spider(655+x, 168),
        Spider(716+x, 241),
        Spider(783+x, 313),
        Spider(847+x, 395),
        Spider(924+x, 477)
        ]
    possible.append((layout, enemies))

    val = possible[randint(0,len(possible)-1)]
    return val[0], val[1]

def checkPlatforms(platMap, enemies, player):
    pos = round(player.relativeX / width)
    pos += 1
    plats = []
    try:
        for i in platMap[pos-2][0]:
            plats.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos-1][0]:
            plats.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos][0]:
            plats.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos+1][0]:
            plats.append(i)
    except IndexError:
        platMap.append(getPlatforms(width))
        for i in platMap[pos+1][0]:
            plats.append(i)
        for i in platMap[pos+1][1]:
            enemies.append(i)
    return plats, enemies

while main():
    main()