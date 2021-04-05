import pygame
def window_start():
    # window creation
    screen = pygame.display.set_mode((800,600))

    # change title
    pygame.display.set_caption("Newbie game")

    # set icon
    icon = pygame.image.load('chat.png')
    pygame.display.set_icon(icon)



    # color
    #screen.fill((22, 36, 27))
    pygame.display.update()

    return screen

def gameover():
    boss_moveX = 0
    boss_moveY = 0
    hero_moveX = 0
    hero_moveY = 0
    print("======GAME OVER=========")