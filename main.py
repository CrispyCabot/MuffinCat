import pygame
from pygame.locals import *
from config import width, height, PATH, size
from player import Player
from ledge import Plat
from cat import Cat
from random import randint
from enemy import Lobster, Spider
import time
import os
from star import Star

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('if u r reading this ur dumb')

font = pygame.font.SysFont('', 34)
bigFont = pygame.font.SysFont('', 94)
medFont = pygame.font.SysFont('', 55)

sun = []
for i in range(60):
    img = pygame.image.load(PATH+os.path.join('data', 'sun', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size*2), int(h*size*2)))
    sun.append(img)

col = 0
colM = .5

sunFrameCounter = 0

def main():
    player = Player(width/2,100)

    clock = pygame.time.Clock()

    platMap = [getPlatforms(-width), getPlatforms(420)]
    
    platforms = []
    enemies = []

    tim = time.time()
    maxTime = 60

    scoreboard = open('scoreboard.txt', 'r')
    scores = scoreboard.readlines()
    
    for i in scores: #removes \n
        scores[scores.index(i)] = i.rstrip('\n')

    newScoreIndex = 10
    nameInput = ''

    playing = True
    gameOver = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
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
                if x.x > player.x-player.w/2 and x.x < player.x+player.w/2 and x.y < player.y and x.y > player.y - player.h:
                    player.health -= 4
                    i.shots.remove(x)
            if type(i) is Lobster:
                if abs(i.x-player.x) < player.w and abs(i.y - player.y) < player.h/2:
                    player.health -= .5
        
        if player.health <= 0 or maxTime-(time.time()-tim) <= 0 or player.y > height+100:
            playing = False
            newHiScore, newScoreIndex = checkHighScore(int((player.relativeX-500)/100), scores)

        redraw(player, platforms, enemies, movement, tim, maxTime)
        pygame.display.update()

    while newHiScore:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    newHiScore = False
                elif event.key == K_BACKSPACE:
                    nameInput = nameInput[:-1]
                else:
                    nameInput += event.unicode
        redraw(player, platforms, enemies, movement, tim, maxTime)
        text = bigFont.render('New High Score', True, (255,255,0))
        loc = text.get_rect()
        loc.center = (width/2, 100)
        win.blit(text, loc)
        text = medFont.render('Enter your name', True, (100,100,0))
        loc = text.get_rect()
        loc.center = (width/2, 175)
        win.blit(text, loc)
        text = medFont.render(nameInput, True, (100,255,0))
        loc = text.get_rect()
        loc.center = (width/2, 250)
        win.blit(text, loc)
        pygame.display.update()
    
    if newScoreIndex != 10:
        scores.insert(newScoreIndex, nameInput + ' '+str(int((player.relativeX-500)/100)))
        scores.pop(5)
        file = open('scoreboard.txt', 'w')
        for i in scores:
            file.write(i+'\n')
    
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[K_q] or keys[K_ESCAPE]:
            return False
        if keys[K_r]:
            return True
        drawEnd(player, platforms, enemies, scores)
        pygame.display.update()

def checkHighScore(x, scores):
    scoreVals = []
    for i in scores:
        scoreVals.append(i.split()[1])
    for i in range(0, len(scoreVals)-1):
        if x > int(scoreVals[i]):
            return True, i
    return False, 10

sunX, sunY = -500, 200
sunYVel = 2
stars = []

def drawBackground(win):
    global col, colM, sunFrameCounter, sunX, sunY, sunYVel, stars
    col += colM
    if col > 255 or col < 0:
        col -= colM
        colM = colM*-1
    win.fill((int(col),int(col),int(col)))
    if col > 127: #daytime
        stars = []
        sunFrameCounter += 1
        if sunFrameCounter > 59:
            sunFrameCounter = 0

        sunX += 4
        sunY -= sunYVel
        sunYVel -= .015
        
        win.blit(sun[sunFrameCounter], (sunX,sunY))
    else:
        sunX, sunY = -500, 200
        sunYVel = 2
        if colM < 0:
            if col%5 == 0:
                stars.append(Star(randint(-100,0), randint(0,600)))
        for i in stars:
            i.draw(win)


def redraw(player, platforms, enemies, movement, tim, maxTime):
    drawBackground(win)
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, movement)
    player.draw(win, movement)
    text = font.render('Score: '+str(int((player.relativeX-500)/100)), True, (255-col,255-col,255-col))
    loc = text.get_rect()
    loc.topleft = (10,10)
    win.blit(text, loc)
    text = font.render('Time: '+str(int(maxTime-(time.time()-tim))), True, (255-col,255-col,255-col))
    loc = text.get_rect()
    loc.topright = (width-10, 10)
    win.blit(text, loc)
    #Hitbox
    #pygame.draw.rect(win, (255,0,0), pygame.Rect(player.x - player.w/2, player.y - player.h, player.w, player.h), 2)

def drawEnd(player, platforms, enemies, scores):
    win.fill((col,col,col))
    for i in platforms:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, [])
    text = font.render('Score: '+str(int((player.relativeX-500)/100)), True, (255-col,255-col,255-col))
    loc = text.get_rect()
    loc.topleft = (10,10)
    win.blit(text, loc)
    text = bigFont.render('Game Over', True, (255,102,102))
    loc = text.get_rect()
    loc.midtop = (width/2, 20)
    win.blit(text, loc)
    text = medFont.render('Scoreboard', True, (255,128,0))
    loc = text.get_rect()
    loc.midtop = (width/2, 100)
    win.blit(text, loc)
    ycounter = 175
    for i in scores:
        things = i.split()
        text = font.render(things[0], True, (50,50,255))
        loc = text.get_rect()
        loc.topright = (width/2-50, ycounter)
        win.blit(text, loc)
        text = font.render(things[1], True, (50,50,255))
        loc = text.get_rect()
        loc.topleft = (width/2+50, ycounter)
        win.blit(text, loc)
        ycounter += 50
    

def getPlatforms(x=0):
   # return [Plat(0+x, 550, 1000, 50)], [Lobster(200+x,520), Spider(400+x, 520)]
    if x == 420:
        return [Plat(0, 550, 1000, 50)], []
    possible = []
    enemies = []

    layout = [
        Plat(x+75,331,219,48),
        Plat(x+659,157,248,67)
    ]
    enemies = [
    ]
    possible.append((layout, enemies))

    layout = [
        Plat(x+45,509,70,26),
        Plat(x+169,509,75,26),
        Plat(x+323,509,79,23),
        Plat(x+498,508,76,23),
        Plat(x+626,505,73,26),
        Plat(x+729,506,103,25),
        Plat(x+405,301,164,30),
        Plat(x+714,115,248,40)
    ]
    enemies = [
            Lobster(485+x, 272)
    ]
    possible.append((layout, enemies))
    layout = [
        Plat(x+41,529,149,30),
        Plat(x+234,570,197,26),
        Plat(x+453,433,77,21),
        Plat(x+612,304,332,27)
    ]
    enemies = [
            Lobster(781+x, 278),
            Spider(491+x, 408)
    ]
    possible.append((layout, enemies))

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