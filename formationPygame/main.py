import pygame
from article import Consensus
from math import sqrt

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1280
screen_height = 960

scaler_px2meter = 1/100
scaler_meter2px = 100

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Formation Control")

formation = Consensus([[3,1], [4.9,3], [2.8,4], [4.0, 1.3]], scaler_meter2px)
formation.create_formation([
    [[1,1],[2,sqrt(2)],[3,1]],
    [[0,1],[2,1],[3,sqrt(2)]],
    [[0,sqrt(2)],[1,1],[3,1]],
    [[0,1],[1,sqrt(2)],[2,1]]
    ])

formation_ord = Consensus([[3,5], [2.8,8], [4.9,7], [4.0, 5.3]], scaler_meter2px)
formation_ord.create_formation([
    [[1,1],[2,sqrt(2)],[3,1]],
    [[0,1],[2,1],[3,sqrt(2)]],
    [[0,sqrt(2)],[1,1],[3,1]],
    [[0,1],[1,sqrt(2)],[2,1]]
    ])

formation_exp = Consensus([[8,1], [9.9,3], [7.8,4], [9.0, 1.3]], scaler_meter2px, ctr="exp")
formation_exp.create_formation([
    [[1,1],[2,sqrt(2)],[3,1]],
    [[0,1],[2,1],[3,sqrt(2)]],
    [[0,sqrt(2)],[1,1],[3,1]],
    [[0,1],[1,sqrt(2)],[2,1]]
    ])

clock = pygame.time.Clock()

# Game loop
running = True
control = False
while running:
    dt = clock.tick(60) # returns how many miliseconds have passed since the last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        control = not control
    # if keys[pygame.K_s] and player1_paddle.bottom < screen_height:
    #     player1_paddle.y += paddle_speed
    # if keys[pygame.K_UP] and player2_paddle.top > 0:
    #     player2_paddle.y -= paddle_speed
    # if keys[pygame.K_DOWN] and player2_paddle.bottom < screen_height:
    #     player2_paddle.y += paddle_speed

    # Clear the screen
    screen.fill(black)

    # Draw paddles and ball
    # pygame.draw.ellipse(screen, white, robot)
    if control:
        formation.update(dt)
        formation_exp.update(dt)
        formation_ord.update(dt)
    formation.draw_formation(screen)
    formation_exp.draw_formation(screen)
    formation_ord.draw_formation(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
