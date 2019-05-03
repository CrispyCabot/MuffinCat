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

playing = True

click1 = None
click2 = None

plats = []

while playing:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == MOUSEBUTTONUP:
            if click1 == None:
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
    for i in plats:
        i.draw(win)
    pygame.display.update()

for i in plats:
    print('Plat'+str((i.x, i.y, i.w, i.h)))

pygame.quit()