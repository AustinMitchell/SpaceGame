from __future__ import division
from random import randint
import math
import sys
import os
import pygame

class Timer(object):
    framesPassed = 0
    
    def __init__(self):
        pass

    @staticmethod
    def Update():
        Timer.framesPassed += 1