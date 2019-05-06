import pygame
from pygame.locals import *
from config import width, height, PATH, size
import os
from player import Player
from ledge import Plat
from cat import Cat
from random import randint
import time
from enemy import Lobster, Spider

pygame.init()

win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('if u r reading this ur dumb')

playing = True

click1 = None
click2 = None

plats = []
enemies = []

player = Player(50,50)
movement = []

lobster = pygame.image.load(PATH+os.path.join('data', 'enemies', 'lobster','0.gif'))
w, h = lobster.get_rect().size
lobster = pygame.transform.scale(lobster, (int(w*size*1.5), int(h*size*1.5)))
spider = pygame.image.load(PATH+os.path.join('data', 'enemies', 'spider', '0.gif'))
w, h = spider.get_rect().size
spider = pygame.transform.scale(spider, (int(w*size*.5), int(h*size*.5)))

while playing:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == MOUSEBUTTONUP:
            if keys[K_l]:
                pos = pygame.mouse.get_pos()
                enemies.append(Lobster(pos[0], pos[1]))
                click1 = None
            elif keys[K_s]:
                pos = pygame.mouse.get_pos()
                enemies.append(Spider(pos[0], pos[1]))
                click1 = None
            elif click1 == None:
                click1 = pygame.mouse.get_pos()
            else:
                click2 = pygame.mouse.get_pos()
                plats.append(Plat(click1[0], click1[1], click2[0]-click1[0], click2[1]-click1[1]))
                click1 = None
                click2 = None

    if keys[K_q]:
        playing = False
    win.fill((255,255,255))
    if click1 != None:
        curr = pygame.mouse.get_pos()
        pygame.draw.rect(win, (255,0,0), pygame.Rect(click1[0], click1[1], curr[0]-click1[0], curr[1]-click1[1]),2)
    if keys[K_l]:
        loc = lobster.get_rect()
        loc.center = pygame.mouse.get_pos()
        win.blit(lobster, loc)
    elif keys[K_s]:
        loc = spider.get_rect()
        loc.center = pygame.mouse.get_pos()
        win.blit(spider, loc)
    for i in plats:
        i.draw(win)
    for i in enemies:
        i.draw(win, player, movement)
    pygame.display.update()

print('layout = [')
for i in plats:
    comma = ','
    if plats.index(i) == len(plats)-1:
        comma = ''
    print('\tPlat(x+'+str(i.x)+','+str(i.y)+','+str(i.w)+','+str(i.h)+')'+comma)
print(']')
print('enemies = [')
for i in enemies:
    comma = ','
    if enemies.index(i) == len(enemies)-1:
        comma = ''
    print('\t'+i.info()+comma)
print(']\npossible.append((layout, enemies))')

pygame.quit()