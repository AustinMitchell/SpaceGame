from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Misc import load_image, draw_centered

# Object to keep track of explosions on the screen
class ExplosionSystem(object):
    def __init__(self):
        self.sound = pygame.mixer.Sound("resources/explosion/explosion.wav")
        self.imgList = []
        for i in range(5, 75):
            self.imgList.append(load_image("explosion/explosion" + str(i) + ".png"))

        self.explosion = []

    # Creates arrays of doubles, first being a vector and last one being a counter
    def new_explosion(self, pos):
        self.explosion.append([pos, 1])
        self.sound.play()

    def Draw(self, screen):
        for ex in self.explosion:
            if ex[1] >= len(self.imgList):
                del ex
            else:
                draw_centered(self.imgList[ex[1]], screen, ex[0])
                ex[1] += 2