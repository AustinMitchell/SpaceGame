from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Vector import Vector

# Generic game object
class GameObject(object):
    def __init__(self, pos, image):
        self.pos = pos
        self.dir = Vector(0, 0)
        self.baseImage = image
        self.image = image
        
        self.size = (image.get_size()[0]+image.get_size()[1]) // 4
        self.angle = 0
        self.oldAngle = 0
        self.value = []