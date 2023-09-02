import pygame
import sys
from game import *

pygame.init()
background = (255, 255, 255)

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris (Python)")
clock = pygame.time.Clock()

game = Game()

# increase timer by 200 ms with every user event
game_update = pygame.USEREVENT
pygame.time.set_timer(game_update, 200)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # down, left, right, and rotate controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            elif event.key == pygame.K_RIGHT:
                game.move_right()
            elif event.key == pygame.K_DOWN:
                game.move_down()
            elif event.key == pygame.K_UP:
                game.rotate()
        # automatic tetromino moving down
        if event.type == game_update:
            game.move_down()

    # fill in background with white, then draw the grid and current block on top of it
    screen.fill(background)
    game.draw(screen)
    pygame.display.update()
    # 60 fps
    clock.tick(60)
