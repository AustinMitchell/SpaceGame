from __future__ import division
from random import randint
import math
import sys
import os
import pygame

import Color

from Vector import Vector
from SpecialStats import SpecialStats
from Misc import deleter, draw_centered, deleter, load_image, width, height, bottom
from Bullet import Bullet

class Player(object):
    def __init__(self, pos, speed, image):
        self.pos = pos
        self.dir = Vector(0, 0)
        self.baseImage = image
        self.image = image

        self.bullet = []
        self.bulletNum = 0
        self.speed = speed
        self.maxhp = 5
        self.hp = self.maxhp
        self.cooldown = 0
        self.specialStats = SpecialStats()

        self.size = (image.get_size()[0]+image.get_size()[1]) // 4
        self.angle = 0
        self.oldAngle = 0

    # Checks if ship is hit by any of the bullets in bulletList
    def hit(self, bulletList):
        for b in bulletList:
            if (self.pos-b.pos).mag() < self.size+b.size:
                self.hp -= b.damage
        deleter(bulletList, [(self.pos-b.pos).mag() < self.size+b.size for b in bulletList])

    def shoot(self):
        if self.cooldown <= 0:
            initBullet(self)

    def Update(self, enemy):
        self.cooldown = max(0, self.cooldown-1)
        self.pos += self.dir
        self.pos.x = min(self.pos.x, width)
        self.pos.x = max(self.pos.x, 0)
        self.pos.y = min(self.pos.y, height)
        self.pos.y = max(self.pos.y, bottom)

        for b in self.bullet:
            b.Update(enemy, bulletUpdate)
        deleter(self.bullet, [b.pos.x > width or b.pos.x < 0 for b in self.bullet])

    def Draw(self, enemy, screen):
        if self.angle == 0:
            draw_centered(self.baseImage, screen, self.pos)
        else:
            if not self.oldAngle == self.angle:
                self.oldAngle = self.angle
                self.image = pygame.transform.rotate(self.baseImage, math.degrees(self.angle))
            draw_centered(self.image, screen, self.pos)

        for b in self.bullet:
            b.Draw(enemy, bulletDraw, screen)

gunCooldown = (16, 16, 23, 7, 31, 47, 42) 
gunDamage = (0.8, 1, 0.6, 0.4, 0.15, 2, 1.6)
gunName = ("Basic Shot", "Fireball", "Triple Shot", "Laser Minigun", "Zapperball", "Homing Rockets", "Power Cannon")
def initBullet(p):
    gunType = p.specialStats.weapon
    if gunType == 0:
        # Weak single shot
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(10, 0), gunType, load_image("bullet/playerbullet0.png")))
        p.bullet[len(p.bullet)-1].damage = gunDamage[0]
        p.cooldown += gunCooldown[0]
    elif gunType == 1:
        # Powerful single shot
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(11, 0), gunType, load_image("bullet/playerbullet1.png")))
        p.bullet[len(p.bullet)-1].damage = gunDamage[1]
        p.cooldown += gunCooldown[1]
    elif gunType == 2:
        # Triple shot
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(9*math.cos(math.pi/20), 9*math.sin(math.pi/15)), gunType, load_image("bullet/playerbullet2.png")))
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(9, 0), gunType, load_image("bullet/playerbullet2.png")))
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(9*math.cos(-math.pi/20), 9*math.sin(-math.pi/15)), gunType, load_image("bullet/playerbullet2.png")))
        for i in range (1, 4):
            p.bullet[len(p.bullet)-i].damage = gunDamage[2]
        p.cooldown += gunCooldown[2]
    elif gunType == 3:
        # Fast shot
        while p.cooldown <= 1:
            rand = math.radians(randint(-5, 5))
            p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y+randint(-2, 2)), Vector(14*math.cos(rand), 14*math.sin(rand)), gunType, load_image("bullet/playerbullet3.png")))
            p.bullet[len(p.bullet)-1].damage = gunDamage[3]
            p.cooldown += gunCooldown[3]*p.specialStats.cooldownBuff
        p.cooldown /= p.specialStats.cooldownBuff
    elif gunType == 4:
        # Zapper shot
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(3, 0), gunType, load_image("bullet/playerbullet4.png")))
        p.bullet[len(p.bullet)-1].damage = gunDamage[4]
        p.cooldown += gunCooldown[4]
    elif gunType == 5:
        # Homing rocket
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(5, 0), gunType, load_image("bullet/playerbullet5.png")))
        p.bullet[len(p.bullet)-1].damage = gunDamage[5]
        p.cooldown += gunCooldown[5]
    elif gunType == 6:
        # Sniping shot
        p.bullet.append(Bullet(Vector(p.pos.x+p.size, p.pos.y), Vector(30, 0), gunType, load_image("bullet/playerbullet6.png")))
        p.bullet[len(p.bullet)-1].damage = gunDamage[6]
        p.cooldown += gunCooldown[6]
    p.bullet[len(p.bullet)-1].damage *= p.specialStats.damageBuff
    p.cooldown *= p.specialStats.cooldownBuff
    p.bulletNum += 1

def bulletUpdate(b, enemy):
    if b.bulletType == 4:
        # Random chance to do a bit of damage each frame
        for e in enemy:
            if randint(1, 10) == 1:
                if (b.pos-e.pos).mag() < b.size*9:
                    e.hp -= b.damage
    if b.bulletType == 5:
        # Finds closest enemy and changes direction to it 
        if not enemy == []:    
            distance = []
            closest = 0
            for e in enemy:
                distance.append((b.pos-e.pos).mag())
            for i in range(len(distance)):
                if distance[i] < distance[closest]:
                    closest = i
            targetVector = enemy[closest].pos - b.pos
            d = targetVector.mag()
            targetVector = targetVector * (2/d)
            b.dir = b.dir*0.9 + targetVector

            b.angle = b.dir.angle()

def bulletDraw(b, enemy, screen):
    if b.bulletType == 4:
        # Draws a crackling aura around the bullet. If enemy is in range, draws a crackling connection
        inRange = False
        for e in enemy:
            if (b.pos-e.pos).mag() < b.size*9:
                inRange = True
                for i in range(4):
                    rand = randint(10, 100)/100
                    target = [int(b.pos.x + (e.pos.x-b.pos.x) * rand), int(b.pos.y +(e.pos.y-b.pos.y) * rand)]
                    pygame.draw.circle(screen, Color.white, target, randint(1, 2))
        if not inRange:
            for i in range(2):
                rand = [int(b.pos.x+randint(-b.size, b.size)), int(b.pos.y+randint(-b.size, b.size)), randint(1, 2)]
                pygame.draw.circle(screen, Color.white, rand[:2], rand[2])