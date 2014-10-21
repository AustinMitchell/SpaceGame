from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Misc import draw_centered, deleter
from Vector import Vector

# Object to keep track of special items on the screen
class SpecialSystem(object):
    def __init__(self, type1ImgList, type2ImgList):
        self.weaponImgList = type1ImgList
        self.statImgList = type2ImgList
        self.item = []

    def new_item(self, pos, itemType, itemID):
        if itemType == 1:
            self.item.append(Special(pos, self.weaponImgList[itemID]))
        elif itemType == 2:
            self.item.append(Special(pos, self.statImgList[itemID-1]))

        self.item[len(self.item)-1].specialType = [itemType, itemID]

    def Update(self, player):
        for i in self.item:
            i.pos.x -= 1
            if (player.pos-i.pos).mag() < player.size+i.size:
                # note that 1 means weapon change, 2 means stat change
                if i.specialType[0] == 1:
                    player.specialStats.score += 100
                    if player.specialStats.weapon == i.specialType[1]:
                        player.specialStats.score += 150
                    else:
                        player.specialStats.weapon = i.specialType[1]
                elif i.specialType[0] == 2:
                    if i.specialType[1] == 1:
                        player.specialStats.speedBuff += 0.5
                    elif i.specialType[1] == 2:
                        player.specialStats.cooldownBuff *= 0.94
                    elif i.specialType[1] == 3:
                        player.specialStats.damageBuff += 0.15
                    elif i.specialType[1] == 4:
                        player.maxhp += 0.3
                        player.hp = min(player.maxhp, player.hp+1)

                    player.specialStats.score += 50

        deleter(self.item, [i.pos.x<0 or (player.pos-i.pos).mag() < player.size+i.size for i in self.item])

    def Draw(self, screen):
        for i in self.item:
            draw_centered(i.image, screen, i.pos)

class Special(object):
    def __init__(self, pos, image):
        self.pos = pos
        self.dir = Vector(0, 0)
        self.image = image        
        self.size = (image.get_size()[0]+image.get_size()[1]) // 4
        self.specialType = []