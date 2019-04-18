import pygame
from config import PATH
import os

platImg = pygame.image.load(PATH+os.path.join('data', 'platform.png'))

class Plat:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.transform.scale(platImg, (w,h))

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def hit(self, x, y, lastY):
        if x > self.x and x < self.x+self.w and y >= self.y and lastY <= self.y:
            return True, self.y
        return False, 0

    def xhit(self, x, y):
        if x > self.x and x < self.x+self.w and y == self.y:
            return True
        return False
