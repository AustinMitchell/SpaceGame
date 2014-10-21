from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Color import scale_color
from Misc import draw_centered
from Vector import Vector

# Clickable object
class Button (object):
    def __init__(self, p, size, stroke, fill, text, font):
        self.p = p
        self.size = size
        self.stroke = stroke
        self.fill = fill
        self.text = text
        self.font = font

        self.enabled = True
        self.clicking = False
        self.targetClrRatio = 0.76
        self.clrRatio = 0.76

    def is_hovering(self):
        mpos = pygame.mouse.get_pos()
        if mpos[0] > self.p.x and mpos[0] < self.p.x+self.size.x and mpos[1] > self.p.y and mpos[1] < self.p.y+self.size.y:
            return self.enabled
        else:
            return False

    def is_clicking(self):
        if self.is_hovering() and pygame.mouse.get_pressed()[0]:
            self.clicking = self.enabled
            return self.enabled
        else:
            clicking = False
            return False

    def is_clicked(self):
        if self.is_hovering() and self.clicking and not pygame.mouse.get_pressed()[0]:
            self.clicking = False
            return self.enabled
        else:
            if not self.is_hovering():
                self.clicking = False
            return False

    def Draw(self, screen):
        if not self.enabled:
            self.targetClrRatio = 0.68
        elif self.is_clicked():
            self.targetClrRatio = 1
        elif self.is_clicking():
            self.targetClrRatio = 0.92
        elif self.is_hovering():
            self.targetClrRatio = 0.84
        else:
            self.targetClrRatio = 0.76

        if self.clrRatio < self.targetClrRatio - 0.01:
            self.clrRatio += 0.02
        elif self.clrRatio > self.targetClrRatio + 0.01:
            self.clrRatio -= 0.02
        
        pygame.draw.rect(screen, scale_color(self.fill, self.clrRatio), pygame.Rect(self.p.toList(), self.size.toList()))
        pygame.draw.rect(screen, scale_color(self.stroke, self.clrRatio), pygame.Rect(self.p.toList(), self.size.toList()), 1)
        draw_centered(self.font.render(self.text, True, scale_color(self.stroke, self.clrRatio)), screen, Vector(self.p.x+self.size.x//2, self.p.y + self.size.y//2))
