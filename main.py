import pygame
import Initialization
import math
from main_objects import character
from pygame import mixer
import random

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
pygame.init()

screen = Initialization.window_start()

NUMBER_OF_ENEMIES = 10
ENEMY_MOVEMENT_SPEED = 0.7
movementX = 0.5
speedUp = 0
speedDown = 0

# music
mixer.music.load('mm8-clownman.mid')
mixer.music.play(-1)

class character:
    def __init__(self, type):
        self.type = type
        if type == "boss":
            image = pygame.image.load('tEm.gif')
            self.image = pygame.transform.scale(image, (75, 75))
            self.X = 350
            self.Y = 50
            self.movementX = 0.3
            self.movementy = 0.3
            print("Enemy Created: ", self.X, " | ", self.Y)
        if type == "hero":
            image = pygame.image.load('ZQjb.gif')
            self.image = pygame.transform.scale(image, (100, 100))
            self.X = 400
            self.Y = 500
            self.movementX = 0
            self.movementY = 0

    def getImage(self):
        return self.image

# initialize player and boss
enemyList = []
hero = character("hero")
boss = character("boss")
score_value = 0

# knife
knife = pygame.image.load('bamboo.png')
knife = pygame.transform.scale(knife, (25,25))
knifeX = 0
knifeY = 0
knife_moveX = 0.5
knife_moveY = 2
knife_state = "ready"

gameover = False


def gameoverScreen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 52)
    game_over = game_over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(game_over, (260, 200))

def scoreHUD():
    font = pygame.font.Font('freesansbold.ttf',12)
    score = font.render("Score: " + str(score_value), True, (0,0,255))
    screen.blit(score, (720,10))

def speedHUD():
    font = pygame.font.Font('freesansbold.ttf',12)
    score = font.render("Speed: " + str(math.fabs(hero.movementX)), True, (0,0,255))
    screen.blit(score, (720,25))

def generateEnemy(enemyCount):
    distanceX = 30
    distanceY = 0
    for i in range(enemyCount):
        enemyList.append(character("boss"))
        enemyList[i].X = random.randint(50+distanceX,600+distanceX)
        enemyList[i].Y = random.randint(0+distanceY,50+distanceY)
        enemyList[i].movementX = ENEMY_MOVEMENT_SPEED
        enemyList[i].movementy = ENEMY_MOVEMENT_SPEED
        screen.blit(enemyList[i].getImage(), (enemyList[i].X, enemyList[i].Y))
        print("Enemy Spawned: ", enemyList[i].X)
        distanceY += 10
        distanceX += 10

def isCollision(enemyX,enemyY,weaponX,weaponY):
    distance = math.sqrt((math.pow(enemyX-weaponX, 2)) + (math.pow(enemyY-weaponY, 2)))
    if distance < 30:
        return True
    else:
        return False

def load_player(x,y):
    screen.blit(hero.getImage(), (x,y))

def load_boss():
    screen.blit(boss.getImage(), (boss.X,boss.Y))

def fire(x, y):
    global knife_state
    knife_state = "fire"
    screen.blit(knife, (x+25,y+10))

def collideAction(enemy):
    global knife_state
    global score_value
    if knife_state != "ready":
        bullet_sound = mixer.Sound('game over.wav')
        bullet_sound.set_volume(0.1)
        bullet_sound.play()
        score_value += 1
    knife_state = "ready"
    enemy.X = 0
    enemy.y = 0
    enemy.movementX = ENEMY_MOVEMENT_SPEED
    enemy.movementy = ENEMY_MOVEMENT_SPEED
    print("======Boss Defeated=======", score_value)

def stopEnemies(enemyList):
    for enemy in enemyList:
        enemy.X = 0
        enemy.y = 0


generateEnemy(NUMBER_OF_ENEMIES)
running = True
# background
background = pygame.image.load('country-platform-preview.png')
background = pygame.transform.scale(background, (800, 600))
screen.fill((22, 36, 27))
while running:
    screen.blit(background, (0, 0))
    for enemy in enemyList:
        screen.blit(enemy.getImage(), (enemy.X, enemy.Y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.movementX = -movementX
                print("LEFT CLICKED")
            if event.key == pygame.K_RIGHT:
                hero.movementX = movementX
                print("RIGHT CLICKED")
            if event.key == pygame.K_DOWN:
                hero.movementY = 1
                print("LEFT CLICKED")
            if event.key == pygame.K_UP:
                hero.movementY = -1
                print("RIGHT CLICKED")
            if event.key == pygame.K_SPACE:
                fire(knifeX, knifeY)
                print("FIRE")
            if event.key == pygame.K_1:
                speedUp += 0.3
                movementX += speedUp
                print("Speed up: ", movementX)
            if event.key == pygame.K_2:
                if movementX > 0.1:
                    speedDown += 0.1
                    movementX -= speedDown
                print("Speed down: ", movementX)
            if event.key == pygame.K_ESCAPE:
                running = False
                break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                hero.movementX = 0
                print("Released")
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                hero.movementY = 0
                print("Released")

    if hero.X <= 0:
        hero.X = 0
    if hero.X >= 750:
        hero.X = 750
    if hero.Y >= 550:
        hero.Y = 550
    if hero.Y <= 0:
        hero.Y = 0

    # weapon validation
    if knife_state == "fire":
        fire(knifeX, knifeY)
        knifeY -= knife_moveY
    if knifeY <= 0:
        knife_state = "ready"
    if knife_state == "ready":
        knifeY = hero.Y
        knifeX = hero.X

    hero.X += hero.movementX
    hero.Y += hero.movementY

    scoreHUD()
    speedHUD()
    load_player(hero.X,hero.Y)

    for enemy in enemyList:
        if enemy.X <= 0:
            enemy.movementX = math.fabs(enemy.movementX)
            enemy.Y += 20
        if enemy.X >= 750:
            enemy.movementX = -1*enemy.movementX
            enemy.Y += 20
        if enemy.Y >= 300:
            print("Game Over")
            for boss in enemyList:
                boss.X = 2000
            gameoverScreen()
            break
        enemy.X += enemy.movementX

        collision = isCollision(enemy.X, enemy.Y, knifeX, knifeY)
        playerCollision = isCollision(enemy.X, enemy.Y, hero.X, hero.Y)

        if collision:
            collideAction(enemy)
        if playerCollision:
            hero.movementX = 0
            hero.movementY = 0
            stopEnemies(enemyList)

    pygame.display.update()