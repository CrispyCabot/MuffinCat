import pygame
from random import uniform, randint

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = randint(2,5)
        self.col = (randint(100,255),randint(100,255),randint(100,255))

    def draw(self, win):
        pygame.draw.circle(win, (255,255,255), (self.x, self.y), round(self.radius))
        if randint(0,50) == 0:
            self.col = (randint(100,255),randint(100,255),randint(100,255))
        self.radius += uniform(-.5,.5)
        if self.radius < 0:
            self.radius = 1
        self.x += 4