from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Misc import draw_centered

# Generic bullet object
class Bullet(object):
    def __init__(self, pos, dir, bulletType, image):
        self.pos = pos
        self.dir = dir
        self.bulletType = bulletType
        self.baseImage = image
        self.image = image

        self.damage = 0
        self.size = (image.get_size()[0]+image.get_size()[1]) // 4
        self.angle = 0
        self.oldAngle = 0

    # Takes in enemy of the bullet's parent ship, some objects need a reference to the enemy
    def Update(self, enemy, bulletUpdate):
        bulletUpdate(self, enemy)
        self.pos += self.dir

    # Same deal over here
    def Draw(self, enemy, bulletDraw, screen):
        if self.angle == 0:
            draw_centered(self.baseImage, screen, self.pos)
        else:
            if not self.oldAngle == self.angle:
                self.oldAngle = self.angle
                self.image = pygame.transform.rotate(self.baseImage, math.degrees(self.angle))
            draw_centered(self.image, screen, self.pos)
        bulletDraw(self, enemy, screen)