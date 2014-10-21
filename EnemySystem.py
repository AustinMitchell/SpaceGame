from __future__ import division
from random import randint
import math
import sys
import os
import pygame

import Color

from SpecialStats import SpecialStats
from Misc import draw_centered, load_image, deleter, width, height, bottom
from Vector import Vector
from Timer import Timer
from Bullet import Bullet

numEnemyTypes = 9

class EnemySystem(object):
    def __init__(self, imgList):
        self.enemyList = []
        self.imgList = imgList
        self.bullet = []
        self.specialStats = SpecialStats()

    # Spawn a new ship
    def spawn(self, shipType):
        self.enemyList.append(Enemy(Vector(width, randint(bottom, height)), shipType, self.imgList[shipType-1]))
        shipInit[shipType](self.enemyList[len(self.enemyList)-1], self.specialStats)

    # Performs 'hit' on all the enemy ships
    def hit(self, bulletList, eID):
        enemyList[eID].hit(bulletList)

    # When an enemy dies, an explosion is made and theres a chance to spawn a special, so I pass the systems here  
    def Update(self, explosionSystem, specialSystem, player):
        for e in self.enemyList:
            e.Update(player)
            e.hit(player.bullet)
            if e.hp <= 0:
                player.specialStats.score += 25 + e.shipType*5
                explosionSystem.new_explosion(e.pos)
                rand1 = randint(1, 8)
                rand2 = 0
                if rand1 <= 3:
                    if rand1 == 1:
                        rand2 = randint(1, len(specialSystem.weaponImgList)-1)
                    else:
                        rand1 = 2
                        rand2 = randint(1, len(specialSystem.statImgList))
                    specialSystem.new_item(e.pos, rand1, rand2)
            elif (e.pos-player.pos).mag() < e.size+player.size:
                player.hp -= e.crashDamage
                explosionSystem.new_explosion(e.pos)
            elif e.cooldown <= 1:
                shipShoot[e.shipType](self, e)
        deleter(self.enemyList, [e.hp <= 0 or e.pos.x < -e.size or (e.pos-player.pos).mag() < e.size+player.size for e in self.enemyList])

        for b in self.bullet:
            b.Update(player, bulletUpdate[b.bulletType])
            if (b.pos-player.pos).mag() < b.size+player.size:
                player.hp -= b.damage
        deleter(self.bullet, [(b.pos-player.pos).mag() < b.size+player.size or b.pos.x > width or b.pos.x < 0 or b.pos.y > height+100 or b.pos.x < -100 for b in self.bullet])

    def Draw(self, player, screen):
        for e in self.enemyList:
            e.Draw(player, screen)
        for b in self.bullet:
            b.Draw(player, bulletDraw[b.bulletType], screen)

class Enemy(object):
    def __init__(self, pos, shipType, image):
        self.pos = pos
        self.shipType = shipType
        self.baseImage = image
        self.image = image

        self.dir = Vector(0, 0)
        self.bulletNum = 0
        self.hp = 0
        self.maxhp = 0
        self.crashDamage = 0
        self.cooldown = 0

        self.size = (image.get_size()[0]+image.get_size()[1]) // 4
        self.angle = 0
        self.oldAngle = 0

    # Checks if ship is hit by any of the bullets in bulletList
    def hit(self, bulletList):
        for b in bulletList:
            if (self.pos-b.pos).mag() < self.size+b.size:
                self.hp -= b.damage
        deleter(bulletList, [(self.pos-b.pos).mag() < self.size+b.size for b in bulletList])

    def Update(self, player):
        self.cooldown = max(0, self.cooldown-1)
        shipUpdate[self.shipType](self, player)
        self.pos += self.dir
        self.pos.y = min(self.pos.y, height)
        self.pos.y = max(self.pos.y, bottom)

    def Draw(self, enemy, screen):
        if self.angle == 0:
            draw_centered(self.baseImage, screen, self.pos)
        else:
            if not self.oldAngle == self.angle:
                self.oldAngle = self.angle
                self.image = pygame.transform.rotate(self.baseImage, math.degrees(self.angle))
            draw_centered(self.image, screen, self.pos)

        shipDraw[self.shipType](self, enemy, screen)

        # Draws a health bar over enemy ships, but not the player.
        if self.shipType > 0:
            pygame.draw.rect(screen, Color.brightred, pygame.Rect(self.pos.x + self.size - self.size * (self.hp/self.maxhp) * 2, self.pos.y-self.size-6, self.size * (self.hp/self.maxhp) * 2, 2), 0)  

"""###########################################################################################"""

def e1Init(e, shipBuffs):
    e.dir = Vector(-3, 0)
    e.maxhp = 2 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e2Init(e, shipBuffs):
    e.dir = Vector(-2, 0)
    e.maxhp = 2 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
    if e.pos.x-50 < bottom:
        e.pos.x += 50
def e3Init(e, shipBuffs):
    e.dir = Vector(-2.5, 0)
    e.maxhp = 2.5 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e4Init(e, shipBuffs):
    e.dir = Vector(-2, 0)
    e.maxhp = 3 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e5Init(e, shipBuffs):
    e.dir = Vector(-2, 0)
    e.maxhp = 3 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e6Init(e, shipBuffs):
    e.dir = Vector(-9.5, 0)
    e.maxhp = 3.5 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 2 * shipBuffs.damageBuff
def e7Init(e, shipBuffs):
    e.dir = Vector(-1.5, 0)
    e.maxhp = 3.5 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e8Init(e, shipBuffs):
    e.dir = Vector(-1.5, 0)
    e.maxhp = 3.5 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1 * shipBuffs.damageBuff
def e9Init(e, shipBuffs):
    e.dir = Vector(-5.5, 0)
    e.maxhp = 3 * shipBuffs.healthBuff
    e.hp = e.maxhp
    e.crashDamage = 1.6 * shipBuffs.damageBuff

def e1Update(e, p):
    # Speeds up if player is within sight
    if abs(e.pos.y-p.pos.y) < e.size+p.size+5 and e.pos.x > p.pos.x:
        e.dir.x = e.dir.x*0.8 - 7*0.2
    else:
        e.dir.x = e.dir.x*0.7 - 3*0.3
def e2Update(e, p):
    # Spins in a loop while moving
    e.pos.x -= 2
    e.dir = e.dir.rotate(math.pi/30)
    e.angle = (e.angle-math.pi/30) % (math.pi*2)
def e3Update(e, p):
    pass
def e4Update(e, p):
   pass
def e5Update(e, p):
    # Image rotates
    e.angle = (e.angle + math.pi/50) % (math.pi*2)
def e6Update(e, p):
    # Image rotates
    e.angle = (e.angle + math.pi/8) % (math.pi*2)
def e7Update(e, p):
    # Image rotates
    if e.cooldown > 0:
        e.angle = (e.angle - 2*math.pi/e.cooldown) % (math.pi*2)
def e8Update(e, p):
    pass
def e9Update(e, p):
    if p.pos.y < e.pos.y:
        e.dir.y = e.dir.y*0.9 - 0.55
    else:
        e.dir.y = e.dir.y*0.9 + 0.55

    if abs(e.dir.y) < 0.1:
        e.dir.y = 0.1
    e.angle = math.atan(e.dir.x/e.dir.y) + math.pi/2
    if e.dir.y < 0 :
        e.angle += math.pi

    framesPassed_ = Timer.framesPassed%24 + 1
    if framesPassed_ <= 6:
        e.baseImage = load_image("e9-2.png")
        e.image = e.baseImage
    elif framesPassed_ <= 12:
        e.baseImage = load_image("e9.png")
        e.image = e.baseImage
    elif framesPassed_ <= 18:
        e.baseImage = load_image("e9-2.png")
        e.image = e.baseImage
    elif framesPassed_ <= 24:
        e.baseImage = load_image("e9-1.png")
        e.image = e.baseImage

def e1Draw(e, p, screen):
    pass
def e2Draw(e, p, screen):
    pass
def e3Draw(e, p, screen):
    pass
def e4Draw(e, p, screen):
    pass
def e5Draw(e, p, screen):
    pass
def e6Draw(e, p, screen):
    pass
def e7Draw(e, p, screen):
    pass
def e8Draw(e, p, screen):
    pass
def e9Draw(e, p, screen):
    pass

def e1Shoot(es, s):
    pass
def e2Shoot(es, e):
    pass
def e3Shoot(es, e):
    es.bullet.append(Bullet(Vector(e.pos.x-e.size, e.pos.y), Vector(-6, 0), e.shipType, load_image("bullet/e3bullet.png")))
    es.bullet[len(es.bullet)-1].damage = 1 * es.specialStats.damageBuff
    e.cooldown = 60 * es.specialStats.cooldownBuff
def e4Shoot(es, e):
    es.bullet.append(Bullet(Vector(e.pos.x-e.size, e.pos.y), Vector(-3.5, 0), e.shipType, load_image("bullet/e4bullet.png")))
    es.bullet.append(Bullet(Vector(e.pos.x+e.size, e.pos.y), Vector(3.5, 0), e.shipType, load_image("bullet/e4bullet.png")))
    es.bullet.append(Bullet(Vector(e.pos.x, e.pos.y+e.size), Vector(0, 3.5), e.shipType, load_image("bullet/e4bullet.png")))
    es.bullet.append(Bullet(Vector(e.pos.x, e.pos.y-e.size), Vector(0, -3.5), e.shipType, load_image("bullet/e4bullet.png")))
    for i in range(1, 5): 
        es.bullet[len(es.bullet)-i].damage = 1 * es.specialStats.damageBuff
    e.cooldown = 80 * es.specialStats.cooldownBuff
def e5Shoot(es, e):
    es.bullet.append(Bullet(Vector(e.pos.x + e.size*math.cos(e.angle), e.pos.y + e.size*math.sin(e.angle)), Vector(4*math.cos(e.angle), 4*math.sin(e.angle)), e.shipType, load_image("bullet/e5bullet.png")))
    es.bullet[len(es.bullet)-1].damage = 1.2 * es.specialStats.damageBuff
    e.cooldown = 26 * es.specialStats.cooldownBuff
def e6Shoot(es, e):
    pass
def e7Shoot(es, e):
    for i in range(-4, 5):
        es.bullet.append(Bullet(Vector(e.pos.x, e.pos.y), Vector(i*1.5, (abs(i)-4)*1.5), e.shipType, load_image("bullet/e7bullet.png")))
        es.bullet.append(Bullet(Vector(e.pos.x, e.pos.y), Vector(i*1.5, (-abs(i)+4)*1.5), e.shipType, load_image("bullet/e7bullet.png")))
        es.bullet[len(es.bullet)-1].damage = 0.5*es.specialStats.damageBuff
        es.bullet[len(es.bullet)-2].damage = 0.5*es.specialStats.damageBuff
    e.cooldown = 180 * es.specialStats.cooldownBuff
def e8Shoot(es, e):
    e.bulletNum += 1
    if e.bulletNum == 2:
        e.bulletNum = 0
    initSide = 1
    if e.bulletNum%2 == 0:
        initSide = -1
    es.bullet.append(Bullet(Vector(e.pos.x, e.pos.y + (e.size-3)*initSide), Vector(-5, 0), e.shipType, load_image("bullet/e8bullet.png")))
    es.bullet[len(es.bullet)-1].damage = 1.2 * es.specialStats.damageBuff
    e.cooldown = 50 * es.specialStats.cooldownBuff
def e9Shoot(es, e):
    pass

def e1BulletUpdate(b, p):
    pass
def e2BulletUpdate(b, p):
    pass
def e3BulletUpdate(b, p):
    pass
def e4BulletUpdate(b, p):
    pass
def e5BulletUpdate(b, p):
    b.angle = (b.angle+math.pi/20) % (math.pi*2)
def e6BulletUpdate(b, p):
    pass
def e7BulletUpdate(b, p):
    pass
def e8BulletUpdate(b, p):
    pass
def e9BulletUpdate(b, P):
    pass

def e1BulletDraw(b, p, screen):
    pass
def e2BulletDraw(b, p, screen):
    pass
def e3BulletDraw(b, p, screen):
    pass
def e4BulletDraw(b, p, screen):
    pass
def e5BulletDraw(b, p, screen):
    pass
def e6BulletDraw(b, p, screen):
    pass
def e7BulletDraw(b, p, screen):
    pass
def e8BulletDraw(b, p, screen):
    pass
def e9BulletDraw(b, p, screen):
    pass

shipInit = [None, e1Init, e2Init, e3Init, e4Init, e5Init, e6Init, e7Init, e8Init, e9Init]
shipUpdate = [None, e1Update, e2Update, e3Update, e4Update, e5Update, e6Update, e7Update, e8Update, e9Update]
shipDraw = [None, e1Draw, e2Draw, e3Draw, e4Draw, e5Draw, e6Draw, e7Draw, e8Draw, e9Draw]
shipShoot = [None, e1Shoot, e2Shoot, e3Shoot, e4Shoot, e5Shoot, e6Shoot, e7Shoot, e8Shoot, e9Shoot]
bulletUpdate = [None,
                e1BulletUpdate, e2BulletUpdate, e3BulletUpdate, e4BulletUpdate,
                e5BulletUpdate, e6BulletUpdate, e7BulletUpdate, e8BulletUpdate,
                e9BulletUpdate]
bulletDraw = [None,
              e1BulletDraw, e2BulletDraw, e3BulletDraw, e4BulletDraw,
              e5BulletDraw, e6BulletDraw, e7BulletDraw, e8BulletDraw,
              e9BulletDraw]