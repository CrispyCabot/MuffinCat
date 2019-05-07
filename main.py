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

font = pygame.font.SysFont('', 34)
bigFont = pygame.font.SysFont('', 94)
medFont = pygame.font.SysFont('', 55)

def main():
    player = Player(width/2,100)

    clock = pygame.time.Clock()

    platMap = [getPlatforms(-width), getPlatforms(420)]
    
    platforms = []
    enemies = []

    tim = time.time()
    maxTime = 60

    playing = True
    gameOver = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        clock.tick(60)

        platforms, enemies = checkPlatforms(platMap, enemies, player)
        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
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
                continue
            for x in enemies:
                if i.x < x.x+x.w/2 and i.x > x.x-x.w/2 and i.y < x.y+x.h/2 and i.y > x.y-x.h/2:
                    x.health -= 5
                    player.shots.remove(i)
                    if x.health < 0:
                        enemies.remove(x)
        for i in enemies:
            for x in i.shots:
                if x.x > width+20 or x.x < -20:
                    i.shots.remove(x)
                    continue
                if x.x > player.x-50 and x.x < player.x+50 and x.y < player.y and x.y > player.y - player.h:
                    player.health -= 4
                    i.shots.remove(x)
            if type(i) is Lobster:
                if abs(i.x-player.x) < 50 and abs(i.y - player.y) < 50:
                    player.health -= .5
        
        if player.health <= 0 or maxTime-(time.time()-tim) <= 0 or player.y > height+100:
            playing = False

        redraw(player, platforms, enemies, movement, tim, maxTime)
    
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        if keys[K_r]:
            return True
        drawEnd(player, platforms, enemies)

def redraw(player, platforms, enemies, movement, tim, maxTime):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, movement)
    player.draw(win, movement)
    text = font.render('Score: '+str(int((player.relativeX-500)/100)), True, (0,0,0))
    loc = text.get_rect()
    loc.topleft = (10,10)
    win.blit(text, loc)
    text = font.render('Time: '+str(int(maxTime-(time.time()-tim))), True, (0,0,0))
    loc = text.get_rect()
    loc.topright = (width-10, 10)
    win.blit(text, loc)
    pygame.display.update()

def drawEnd(player, platforms, enemies):
    win.fill((255,255,255))
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, [])
    text = font.render('Score: '+str(int((player.relativeX-500)/100)), True, (0,0,0))
    loc = text.get_rect()
    loc.topleft = (10,10)
    win.blit(text, loc)
    text = bigFont.render('Game Over', True, (255,102,102))
    loc = text.get_rect()
    loc.midtop = (width/2, 20)
    win.blit(text, loc)
    text = medFont.render('Scoreboard', True, (218,165,32))
    loc = text.get_rect()
    loc.midtop = (width/2, 100)
    win.blit(text, loc)
    pygame.display.update()
    

def getPlatforms(x=0):
   # return [Plat(0+x, 550, 1000, 50)], [Lobster(200+x,520), Spider(400+x, 520)]
    if x == 420:
        return [Plat(0, 550, 1000, 50)], []
    possible = []
    enemies = []

    layout = [
        Plat(x+15,503,164,43),
        Plat(x+249,502,172,36),
        Plat(x+486,502,175,33),
        Plat(x+724,499,179,30),
        Plat(x+405,426,106,31),
        Plat(x+416,326,91,35),
        Plat(x+413,250,103,23),
        Plat(x+412,140,100,33),
        Plat(x+612,95,239,31),
        Plat(x+146,70,209,43)
    ]
    enemies = [
            Lobster(455+x, 109),
            Spider(572+x, 474),
            Spider(337+x, 474),
            Lobster(462+x, 297)
    ]
    possible.append((layout, enemies))

    layout = [
        Plat(x+11,530,973,52)
    ]
    enemies = [
            Spider(838+x, 501),
            Lobster(712+x, 498)
    ]
    possible.append((layout, enemies))

    layout = [
            Plat(x+13,523,273,42),
            Plat(x+309,452,232,34),
            Plat(x+568,351,276,30),
            Plat(x+822,507,165,42)
    ]
    enemies = [
            Spider(910+x, 480),
            Lobster(592+x, 320),
            Spider(796+x, 323),
            Lobster(247+x, 493)
    ]
    possible.append((layout, enemies))

    layout = [
        Plat(x+15,528,132,39),
        Plat(x+69,449,136,28),
        Plat(x+129,368,138,28),
        Plat(x+193,271,138,25),
        Plat(x+286,172,156,30),
        Plat(x+409,94,183,24),
        Plat(x+767,91,158,33),
        Plat(x+779,198,143,40),
        Plat(x+792,302,131,38),
        Plat(x+788,388,147,38),
        Plat(x+766,475,196,37)
    ]
    enemies = [
            Spider(913+x, 452),
            Spider(864+x, 361),
            Spider(857+x, 274),
            Spider(853+x, 171),
            Spider(849+x, 67),
            Lobster(208+x, 340)
    ]
    possible.append((layout, enemies))

    layout = [
        Plat(x+29,510,260,41),
        Plat(x+346,394,80,28),
        Plat(x+527,304,66,27),
        Plat(x+834,517,148,43)
    ]
    enemies = [
            Spider(910+x, 488)
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
        platMap.append(getPlatforms(width))
        for i in platMap[pos][0]:
            plats.append(i)
        for i in platMap[pos][1]:
            enemies.append(i)
    return plats, enemies

while main():
    main()