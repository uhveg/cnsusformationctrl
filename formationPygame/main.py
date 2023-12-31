import pygame
from article import Consensus
from math import sqrt

# Screen dimensions
screen_width = 1280
screen_height = 960

scaler_px2meter = 1/100
scaler_meter2px = 100

def draw_grid(screen):
    vlines = screen_width // scaler_meter2px
    hlines = screen_height // scaler_meter2px
    for i in range(1, hlines+1):
        pygame.draw.line(screen, (100, 100, 100), (0, scaler_meter2px*i), (screen_width,  scaler_meter2px*i), 1)
    for i in range(1, vlines+1):
        pygame.draw.line(screen, (100, 100, 100), (scaler_meter2px*i, 0), (scaler_meter2px*i, screen_height), 1)


# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Formation Control")

# formation_csc = Consensus([[3,3], [2.8,5], [4.9,5], [4.0, 3.3]], scaler_meter2px)
# formation_csc.create_formation([
#     [[1,1],[2,sqrt(2)],[3,1]],
#     [[0,1],[2,1],[3,sqrt(2)]],
#     [[0,sqrt(2)],[1,1],[3,1]],
#     [[0,1],[1,sqrt(2)],[2,1]]
#     ])

# formation_exp = Consensus([[8,3], [7.8,5], [9.9,5], [9.0, 3.3]], scaler_meter2px, ctr="exp")
# formation_exp.create_formation([
#     [[1,1],[2,sqrt(2)],[3,1]],
#     [[0,1],[2,1],[3,sqrt(2)]],
#     [[0,sqrt(2)],[1,1],[3,1]],
#     [[0,1],[1,sqrt(2)],[2,1]]
#     ])

formation_csc = Consensus([[4.95,5], [5,5]], scaler_meter2px)
formation_csc.create_formation([
    [[1,1]],
    [[0,1]]
    ])

formation_exp = Consensus([[8.95,5], [9,5]], scaler_meter2px, ctr="exp")
formation_exp.create_formation([
    [[1,1]],
    [[0,1]]
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
    if keys[pygame.K_ESCAPE]:
        running = False
    # if keys[pygame.K_s] and player1_paddle.bottom < screen_height:
    #     player1_paddle.y += paddle_speed
    # if keys[pygame.K_UP] and player2_paddle.top > 0:
    #     player2_paddle.y -= paddle_speed
    # if keys[pygame.K_DOWN] and player2_paddle.bottom < screen_height:
    #     player2_paddle.y += paddle_speed

    # Clear the screen
    screen.fill(black)
    draw_grid(screen)
    # Draw paddles and ball
    # pygame.draw.ellipse(screen, white, robot)
    if control:
        formation_csc.update(dt)
        formation_exp.update(dt)
    formation_csc.draw_formation(screen)
    formation_exp.draw_formation(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
