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

    platMap = [getPlatforms(-width), getPlatforms()]
    for i in range(1,4):
        platMap.append(getPlatforms(width))
    
    platforms = []
    for i in platMap[0]:
        platforms.append(i)
    for i in platMap[1]:
        platforms.append(i)
    for i in platMap[2]:
        platforms.append(i)

    cats = []

    diff = 3
    
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

        platforms = checkPlatforms(platMap, platforms, player)

        if time.time() - tStart > diff:
            cats.append(Cat(randint(0,width), 0))
            tStart = time.time()
            diff -= .02
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
        for i in cats:
            i.move(player, platforms, movement)
            if i.y > height+100:
                cats.remove(i)
                continue
            for x in player.shots:
                if x.x < i.x+i.w/2-60 and x.x > i.x-i.w/2+60 and x.y < i.y and x.y > i.y-i.h:
                    i.health -= 3  
                    player.shots.remove(x)
                elif x.x < -200 or x.x > width+200:
                    player.shots.remove(x)
            if abs(i.x-player.x) < 100 and abs(i.y-player.y) < 50:
                player.health -= .5
            if player.explode:
                if abs(i.x-player.x) < 150 and abs(i.y-player.y) < 150:
                    i.health -= 7
            if i.health <= 0:
                if i in cats:
                    cats.remove(i)

        redraw(player, platforms, cats, movement)

def redraw(player, platforms, cats, movement):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in cats:
        i.draw(win)
    player.draw(win, movement)
    pygame.display.update()

def getPlatforms(x=0):
    #return [Plat(0+x, 550, 1000, 50)]
    possible = []
    layout = [
        Plat(0+x, 550, 1000, 50),
        Plat(204+x, 433, 651, 31),
        Plat(418+x, 306, 356, 50),
        Plat(560+x, 207, 169, 25),
        Plat(645+x, 124, 46, 8),
        Plat(125+x, 219, 184, 45)
    ]
    possible.append(layout)
    layout = [
        Plat(0+x, 550, 1000, 50),
        Plat(3+x, 2, 990, 246),
        Plat(26+x, 428, 189, 30),
        Plat(419+x, 428, 189, 30),
        Plat(736+x, 428, 189, 30)
    ]
    possible.append(layout)
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
    possible.append(layout)
    layout = [Plat(0+x, 550, 1000, 50)]
    possible.append(layout)

    val = possible[randint(0,len(possible)-1)]
    return val

def checkPlatforms(platMap, platforms, player):
    pos = round(player.relativeX / width)
    pos += 1
    plats = []
    try:
        for i in platMap[pos-1]:
            plats.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos]:
            plats.append(i)
    except IndexError:
        pass
    try:
        for i in platMap[pos+1]:
            plats.append(i)
    except IndexError:
        platMap.append(getPlatforms(width))
        for i in platMap[pos+1]:
            plats.append(i)
    return plats


while main():
    main()