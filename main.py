import pygame
import Initialization
import math
import main_variables
import random
from main_objects import character, weapon
from pygame import mixer


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

pygame.init()

start_up = Initialization
screen = start_up.window_start()

main_variables.NUMBER_OF_ENEMIES = random.randint(1,10)

# initialize player and boss
enemyList = []
hero = character("hero")
boss = character("boss")
attack = weapon("bamboo")
score_value = 0

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
    distanceX = 75
    distanceY = 0
    for i in range(enemyCount):
        enemyList.append(character("boss"))
        enemyList[i].X = random.randint(50+distanceX,350+distanceX)
        enemyList[i].Y = 50
        enemyList[i].movementX = main_variables.ENEMY_MOVEMENT_SPEED
        enemyList[i].movementY = main_variables.ENEMY_MOVEMENT_SPEED
        screen.blit(enemyList[i].getImage(), (enemyList[i].X, enemyList[i].Y))
        print("Enemy Spawned: ", enemyList[i].X)
        distanceY += 20
        distanceX += 60

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

def fire(x, y, weapon):
    #global knife_state
    weapon.state = "fire"
    screen.blit(weapon.getImage(), (x+25,y+10))

def collideAction(enemy,weapon):
    #global knife_state
    global score_value
    if weapon.state != "ready":
        bullet_sound = mixer.Sound('game over.wav')
        bullet_sound.set_volume(0.1)
        bullet_sound.play()
        score_value += 1
    weapon.state = "ready"
    enemy.X = 0
    enemy.y = 0
    enemy.movementX = main_variables.ENEMY_MOVEMENT_SPEED
    enemy.movementY = main_variables.ENEMY_MOVEMENT_SPEED
    print("======Boss Defeated=======", score_value)

def stopEnemies(enemyList):
    for enemy in enemyList:
        enemy.X = 0
        enemy.y = 0

def keyInputChecker(event):
    global running
    global speedUp
    global speedDown
    #global movementX
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            hero.movementX = -main_variables.movementX
            print("LEFT CLICKED")
        if event.key == pygame.K_RIGHT:
            hero.movementX = main_variables.movementX
            print("RIGHT CLICKED")
        if event.key == pygame.K_DOWN:
            hero.movementY = 1
            print("LEFT CLICKED")
        if event.key == pygame.K_UP:
            hero.movementY = -1
            print("RIGHT CLICKED")
        if event.key == pygame.K_SPACE:
            fire(attack.X, attack.Y, attack)
            print("FIRE")
        if event.key == pygame.K_1:
            speedUp += 0.3
            main_variables.movementX += speedUp
            print("Speed up: ", main_variables.movementX)
        if event.key == pygame.K_2:
            if main_variables.movementX > 0.1:
                speedDown += 0.1
                main_variables.movementX -= speedDown
            print("Speed down: ", main_variables.movementX)
        if event.key == pygame.K_ESCAPE:
            running = False

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            hero.movementX = 0
            print("Released")
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            hero.movementY = 0
            print("Released")

def basicHeroMovements():
    if hero.X <= 0:
        hero.X = 0
    if hero.X >= 750:
        hero.X = 750
    if hero.Y >= 550:
        hero.Y = 550
    if hero.Y <= 0:
        hero.Y = 0
    hero.X += hero.movementX
    hero.Y += hero.movementY

def basicWeaponMovement(weapon, hero):
    # weapon validation
    if weapon.state == "fire":
        fire(weapon.X, weapon.Y, weapon)
        weapon.Y -= weapon.movementY
    if weapon.Y <= 0:
        weapon.state = "ready"
    if weapon.state == "ready":
        weapon.Y = hero.Y
        weapon.X = hero.X

def basicEnemyMovement(enemy):
    if enemy.X <= 0:
        enemy.movementX = math.fabs(enemy.movementX)
        enemy.Y += 20
    if enemy.X >= 750:
        enemy.movementX = -1 * enemy.movementX
        enemy.Y += 20
    enemy.X += enemy.movementX

generateEnemy(main_variables.NUMBER_OF_ENEMIES)
running = True
# background
background = pygame.image.load('country-platform-preview.png')
background = pygame.transform.scale(background, (800, 600))
screen.fill((22, 36, 27))

while running:
    screen.blit(background, (0, 0))
    basicHeroMovements()
    basicWeaponMovement(attack, hero)
    scoreHUD()
    speedHUD()
    load_player(hero.X,hero.Y)
    for enemy in enemyList:
        screen.blit(enemy.getImage(), (enemy.X, enemy.Y))

    for event in pygame.event.get():
        keyInputChecker(event)
        if event.type == pygame.QUIT:
            running = False

    for enemy in enemyList:
        basicEnemyMovement(enemy)
        collision = isCollision(enemy.X, enemy.Y, attack.X, attack.Y)
        playerCollision = isCollision(enemy.X, enemy.Y, hero.X, hero.Y)
        if collision:
            collideAction(enemy, attack)
        if playerCollision:
            hero.movementX = 0
            hero.movementY = 0
            stopEnemies(enemyList)
            for boss in enemyList:
                boss.X = 2000
            gameoverScreen()
            break
        if enemy.Y >= 700:
            print("Game Over")
            for boss in enemyList:
                boss.X = 2000
            gameoverScreen()
            break

    pygame.display.update()
