import pygame
import main_variables
import math

def gameoverScreen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 52)
    game_over = game_over_font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(game_over, (260, 200))

def scoreHUD():
    font = pygame.font.Font('freesansbold.ttf',12)
    score = font.render("Score: " + str(main_variables.score_value), True, (0,0,255))
    screen.blit(score, (720,10))

def speedHUD():
    font = pygame.font.Font('freesansbold.ttf',12)
    score = font.render("Speed: " + str(math.fabs(hero.movementX)), True, (0,0,255))
    screen.blit(score, (720,25))