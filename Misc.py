from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Vector import Vector

# Screen parameters. The bottom is to allow a little space for a HUD
width = 1000
height = 650
bottom = 30

# Loads an image with the given filename from the directory
def load_image(filename):
    return pygame.image.load(os.path.join('resources', filename))

# Draws an image onto surface2 with the center being at 'position'
def draw_centered(surface1, surface2, position):
    rect = surface1.get_rect()
    if isinstance (position, Vector):
        rect = rect.move(position.x - rect.width//2, position.y - rect.height//2)
        surface2.blit(surface1, rect)
    else:
        rect = rect.move(position[0] - rect.width//2, position[1] - rect.height//2)
        surface2.blit(surface1, rect)

# Takes in an array of anything and an array of conditions, deletes elements which have the condition true in the same spot.
def deleter(array, condition):
    i = 0
    while i < len(array):
        if condition[i]:
            del array[i]
            del condition[i]
        else:
            i += 1