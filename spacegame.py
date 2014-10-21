from __future__ import division
from random import randint
import math
import sys
import os
import pygame

from Color import *

from Misc import load_image, draw_centered, width, height, bottom
from Button import Button
from StarSystem import StarSystem
from ExplosionSystem import ExplosionSystem
from SpecialSystem import SpecialSystem
from EnemySystem import EnemySystem, numEnemyTypes
from Player import Player, gunName, gunCooldown, gunDamage
from Timer import Timer
from Vector import Vector

# Main game class
class Game(object):
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        
        # set up display
        self.screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)

        # use a black background
        self.bg_color = black

        # Set up game resources (fonts, misc. pictures/sound) 
        self.f1 = pygame.font.SysFont("Arial", 11)
        self.f2 = pygame.font.SysFont("Impact", 32)
        self.f3 = pygame.font.SysFont("Impact", 64)

        pygame.mixer.music.load("resources/menu.wav")
        pygame.mixer.music.play(-1)

        self.gameOverImage = load_image("gameover.png")
        self.instructionImage = [load_image("instructions"+str(i)+".png") for i in range(1, 4)]

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        # Setup all buttons for the game
        self.start = Button(Vector(400, 200), Vector(200, 100), brightgreen, darkgrey, "Start Game", self.f2)
        self.cont = Button(Vector(800, 400), Vector(175, 75), brightgreen, darkgrey, "Continue", self.f2)
        self.prev = Button(Vector(50, 425), Vector(150, 50), orange, darkgrey, "Previous", self.f2)
        self.next = Button(Vector(800, 425), Vector(150, 50), orange, darkgrey, "Next", self.f2)
        self.back = Button(Vector(425, 425), Vector(150, 50), orange, darkgrey, "Back", self.f2)
                                 
        self.instructions = Button(Vector(400, 350), Vector(200, 100), brightgreen, darkgrey, "Instructions", self.f2)
        self.currentPage = 0

        self.engageSmoothJazz = Button(Vector(350, 500), Vector(300, 100), purple, darkgrey, "Engage Smooth Jazz", self.f2)
        self.smoothJazzEnabled = False

        # Number of enemy types and current upper enemy level that can spawn
        self.numEnemies = 9
        self.currentEnemy = 1
        self.baseCurrentEnemy = 1
        self.minEnemy = 1

        # Sets up a star generator
        self.starSystem = StarSystem(300, [load_image ("star"+str(i)+".png").convert_alpha() for i in range(1, 5)])

        # Sets up an explosion generator
        self.explosion = ExplosionSystem()

        # Sets up a special item generator
        self.wepImage = [load_image("wep"+str(i)+".png").convert_alpha() for i in range(7)]
        self.buffImage = [load_image("special"+str(i)+".png").convert_alpha() for i in range(1, 5)]
        self.special = SpecialSystem(self.wepImage, self.buffImage)

        # Sets up an enemy generator
        self.enemy = EnemySystem([load_image ("e"+str(i)+".png").convert_alpha() for i in range(1, self.numEnemies+1)])

        # Sets up player and related variables
        self.player = Player(Vector(50, height//2), 7, load_image("player.png").convert_alpha())
        self.shooting = False
        self.oldhp = self.player.hp

        # Variable to keep track of game state
        self.state = "MENU"

        # Different in-game timers
        self.gameMessage = ""
        self.gameTimer = 0
        self.gameTimerBuff = 1
        self.baseSpawnTime = 33
        self.spawnTime = self.baseSpawnTime
        self.spawnTimer = self.spawnTime

    def reset(self):
        self.player = Player(Vector(50, height//2), 7, load_image("player.png").convert_alpha())
        self.shooting = False
        self.oldhp = self.player.hp

        self.currentEnemy = 1
        self.baseCurrentEnemy = 1
        self.minEnemy = 1

        self.enemy = EnemySystem([load_image ("e"+str(i)+".png").convert_alpha() for i in range(1, self.numEnemies+1)])

        self.currentEnemy = 1

        self.explosion = ExplosionSystem()

        self.special = SpecialSystem(self.wepImage, self.buffImage)

        self.gameMessage = ""
        self.gameTimer = 0
        self.gameTimerBuff = 1
        self.baseSpawnTime = 33
        self.spawnTime = self.baseSpawnTime
        self.spawnTimer = self.spawnTime

    # Main update method
    def Update(self):
        if self.state == "MENU":
            self.starSystem.Update()
            if self.start.is_clicked():
                self.state = "GAME"
                if not self.smoothJazzEnabled:
                    pygame.mixer.music.load("resources/game.wav")
                    pygame.mixer.music.play(-1)
            elif self.instructions.is_clicked():
                self.state = "INSTRUCTIONS"
            elif self.engageSmoothJazz.is_clicked():
                self.smoothJazzEnabled = (self.smoothJazzEnabled == False)
                if self.smoothJazzEnabled:
                    pygame.mixer.music.load("resources/smoothjazz.wav")
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.load("resources/menu.wav")
                    pygame.mixer.music.play(-1)
        elif self.state == "INSTRUCTIONS":
            self.starSystem.Update()
            if self.back.is_clicked():
                self.state = "MENU"
                self.currentPage = 0
            elif self.next.is_clicked():
                self.currentPage = min(self.currentPage+1, 2)
            elif self.prev.is_clicked():
                self.currentPage = max(self.currentPage-1, 0)
        elif self.state == "GAMEOVER":
            if self.cont.is_clicked():
                self.state = "MENU"
                if not self.smoothJazzEnabled:
                    pygame.mixer.music.load("resources/menu.wav")
                    pygame.mixer.music.play(-1)
                self.reset()
                                 
        elif self.state == "GAME":
            if self.player.hp <= 0:
                self.state = "GAMEOVER"
                self.explosion.new_explosion(self.player.pos)
            
            self.gameTimer += 1
            if self.gameTimer >= 210*self.gameTimerBuff:
                self.gameTimer = 0
                self.spawnTime = self.baseSpawnTime
                self.gameMessage = ""
                self.minEnemy = 1
                self.currentEnemy = self.baseCurrentEnemy
            elif self.gameTimer == int(150*self.gameTimerBuff):
                rand = randint(1, 2)
                if rand <= 1 and self.currentEnemy < self.numEnemies:
                    self.currentEnemy += 1
                    self.baseCurrentEnemy += 1
                    self.gameMessage = "Enemy Max Level +"
                else:
                    rand = randint(1, 6)
                    if rand == 1:
                        if randint(1, 2) == 1 and self.currentEnemy >= 6:
                            self.gameMessage = "Massive Slicer Wave"
                            self.spawnTime = 2
                            self.minEnemy = 6
                            self.currentEnemy = 6
                        else:
                            self.gameMessage = "Super Wave"
                            self.spawnTime = 3
                    elif rand == 2:
                        self.enemy.specialStats.cooldownBuff *= 0.92
                        self.gameMessage = "Enemy Cooldown Buff +"
                    elif rand == 3:
                        self.enemy.specialStats.healthBuff += 0.25
                        self.gameMessage = "Enemy Health Buff +"
                    elif rand == 4:
                        self.enemy.specialStats.damageBuff += 0.15
                        self.gameMessage = "Enemy Damage Buff +"
                    elif rand == 5:
                        self.baseSpawnTime *= 0.92
                        self.gameMessage = "Enemy Spawn Time +"
                    elif rand == 6:
                        self.gameTimerBuff *= 0.96
                        self.gameMessage = "Event Timer Decreased"
            
            self.spawnTimer -= 1
            if self.spawnTimer <= 0:
                self.spawnTimer = self.spawnTime
                self.enemy.spawn(randint(self.minEnemy, self.currentEnemy))
            
            self.starSystem.Update()
            
            self.player.Update(self.enemy.enemyList)
            self.player.hp = max(0, self.player.hp)

            if self.shooting:
                self.player.shoot()

            self.special.Update(self.player)
            self.enemy.Update(self.explosion, self.special, self.player)

    # Main draw method
    def Draw(self):
        if self.state == "MENU":
            self.starSystem.Draw(self.screen)
            self.start.Draw(self.screen)
            self.instructions.Draw(self.screen)
            self.engageSmoothJazz.Draw(self.screen)
            draw_centered(self.f3.render("SUPER SPACE GAME", True, orange), self.screen, (500, 100))
            draw_centered(self.f1.render("All images and code(excepting pygame) by:", True, brightcyan), self.screen, (850, 200))
            draw_centered(self.f1.render("Nathaniel Mitchell", True, brightcyan), self.screen, (850, 215))
        elif self.state == "INSTRUCTIONS":
            self.starSystem.Draw(self.screen)
            draw_centered(self.instructionImage[self.currentPage], self.screen, (500, 250))
            self.prev.Draw(self.screen)
            self.next.Draw(self.screen)
            self.back.Draw(self.screen)
        elif self.state == "GAMEOVER":
            draw_centered(self.gameOverImage, self.screen, (300, 200))
            draw_centered(self.f3.render("GAME OVER", True, brightred), self.screen, (300, 100))
            draw_centered(self.f2.render("Your final score was:", True, yellow), self.screen, (700, 100))
            draw_centered(self.f2.render(str(self.player.specialStats.score), True, orange), self.screen, (800, 150))
            self.explosion.Draw(self.screen)
            self.cont.Draw(self.screen)
        elif self.state == "GAME":
            # Draws all objects
            self.starSystem.Draw(self.screen)
            self.explosion.Draw(self.screen)
            self.player.Draw(self.enemy.enemyList, self.screen)                
            self.special.Draw(self.screen)
            self.enemy.Draw(self.player, self.screen)
            self.drawHUD()

            # Display any in game messages
            if self.gameMessage != "":
                draw_centered(self.f2.render(self.gameMessage, True, yellow), self.screen, (500, 100))
            
        pygame.display.flip()

    # Main game loop
    def run(self):
        running = True
        while running:
            event = pygame.event.wait()

            # Player is asking to quit
            if event.type == pygame.QUIT:
                running = False

            # Player presses a key
            elif event.type == pygame.KEYDOWN:
                # WASD keys set the player direction
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.dir.x = -self.player.speed-self.player.specialStats.speedBuff
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.dir.x = self.player.speed+self.player.specialStats.speedBuff 
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.dir.y = -self.player.speed-self.player.specialStats.speedBuff
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player.dir.y = self.player.speed+self.player.specialStats.speedBuff

                # Checks if a player is trying to shoot
                if event.key == pygame.K_SPACE:
                    self.shooting = True
                
            elif event.type == pygame.KEYUP:
                # Letting go of WASD resets the player direction as needed
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.dir.x = max(0, self.player.dir.x)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.dir.x = min(0, self.player.dir.x)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.dir.y = max(0, self.player.dir.y)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player.dir.y = min(0, self.player.dir.y)

                if event.key == pygame.K_SPACE:
                    self.shooting = False
                    
            # Draws a new frame, frequency defined by self.FPS
            elif event.type == self.REFRESH:
                Timer.Update()
                
                self.Update()
                self.Draw()
                if self.oldhp != self.player.hp:
                    if self.oldhp > self.player.hp:
                        self.screen.fill(red)
                    else:
                        self.screen.fill(self.bg_color)
                    self.oldhp = self.player.hp
                else:
                    self.screen.fill(self.bg_color)

            else:
                pass # an event type we don't handle       

    def drawHUD(self):
        # Draws HUD
        pygame.draw.rect(self.screen, grey, pygame.Rect(0, 0, width, bottom))
        
        draw_centered(self.buffImage[0], self.screen, (15, 15))
        pygame.draw.rect(self.screen, black, pygame.Rect(30, 5, 160, 20))
        draw_centered(self.f1.render(str((self.player.specialStats.speedBuff+self.player.speed)*30) + " pixels per sec (" +
                                       str(int((self.player.speed+self.player.specialStats.speedBuff)*1000 / self.player.speed) / 10) + "%)",
                                       True, brightgreen), self.screen, (105, 15))
        
        draw_centered(self.buffImage[1], self.screen, (210, 15))
        pygame.draw.rect(self.screen, black, pygame.Rect(225, 5, 160, 20))
        draw_centered(self.f1.render(str(int(30 / (self.player.specialStats.cooldownBuff*gunCooldown[self.player.specialStats.weapon]) * 100) / 100) +
                                     " shots per sec (" + str(int(1000/self.player.specialStats.cooldownBuff)/10) + "%)",
                                     True, brightgreen), self.screen, (300, 15))
        
        draw_centered(self.buffImage[2], self.screen, (405, 15))
        pygame.draw.rect(self.screen, black, pygame.Rect(420, 5, 160, 20))
        draw_centered(self.f1.render(str(self.player.specialStats.damageBuff*gunDamage[self.player.specialStats.weapon]) + " damage (" +
                                       str(self.player.specialStats.damageBuff*100) + "%)", True, brightgreen), self.screen, (495, 15))
        
        draw_centered(self.wepImage[self.player.specialStats.weapon], self.screen, (600, 15))
        pygame.draw.rect(self.screen, black, pygame.Rect(615, 5, 120, 20))
        pygame.draw.rect(self.screen, blue, pygame.Rect(615, 5, int(120-120*(self.player.cooldown/gunCooldown[self.player.specialStats.weapon]*self.player.specialStats.cooldownBuff)), 20))
        draw_centered(self.f1.render(gunName[self.player.specialStats.weapon], True, brightgreen), self.screen, (670, 15))
        
        draw_centered(self.buffImage[3], self.screen, (755, 15))
        pygame.draw.rect(self.screen, black, pygame.Rect(770, 5, 100, 20))
        pygame.draw.rect(self.screen, red, pygame.Rect(770, 5, int(100*(self.player.hp/self.player.maxhp)), 20))
        draw_centered(self.f1.render(str(int(self.player.hp*10) / 10) + " / " + str(self.player.maxhp), True, white), self.screen, (810, 15))

        pygame.draw.rect(self.screen, darkblue, pygame.Rect(885, 5, 100, 20))
        draw_centered(self.f1.render("Score: " + str(self.player.specialStats.score), True, white), self.screen, (935, 15))


Game().run()
pygame.quit()
sys.exit()
