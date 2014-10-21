from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Vector import Vector
from Misc import draw_centered, deleter, width, height, bottom

# Keeps track of all the stars in the background. 
class StarSystem(object):
    def __init__(self, numStars, imgList):
        self.star = [Star(Vector(randint(0, width), randint(0, height)), randint(5, 20) / -10, imgList[randint(0, len(imgList) - 1)]) for  i in range(numStars)]

    def Update(self):
        for i in range(len(self.star)):
            self.star[i].pos.x += self.star[i].speed
            if self.star[i].pos.x < -10:
                self.star[i].pos = Vector(width, randint(bottom, height))
                self.star[i].speed = randint(5, 20) / -10

    def Draw(self, screen):
        for s in self.star:
            draw_centered(s.image, screen, s.pos)

class Star(object):
    def __init__(self, pos, speed, image):
        self.pos = pos
        self.speed = speed
        self.image = image   