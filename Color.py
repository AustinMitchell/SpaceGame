from __future__ import division
from random import randint
import math
import sys
import os
import pygame

# Predefined colour. I like this better
brightcyan = (0, 255, 255)
orange = (255, 128, 0)
yellow = (255, 255, 0)
purple = (255, 0, 255)
darkpurple = (128, 0, 128)
brightred = (255, 0, 0)
red = (128, 0, 0)
brightgreen = (0, 255, 0)
darkblue = (0, 0, 80)
blue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
darkgrey = (64, 64, 64)

# Scales a colour's values by a given ratio 
def scale_color(color, ratio):
    return [c*ratio for c in color]