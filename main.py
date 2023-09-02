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

# delays in ms when you hold down the keys
key_repeat_delay = 200
key_repeat_interval = 100

key_timers = {
    pygame.K_LEFT: 0,
    pygame.K_RIGHT: 0,
    pygame.K_DOWN: 0,
    pygame.K_UP: 0
}

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if game over, click any button to restart
        if event.type == pygame.KEYDOWN:
            if game.game_over:
                game.game_over = False
                game.reset()
        # automatic tetromino moving down
        if event.type == game_update and not game.game_over:
            game.move_down()

    # down, left, right, and rotate controls
    keys_pressed = pygame.key.get_pressed()
    for key in key_timers:
        if keys_pressed[key] and not game.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - key_timers[key] > key_repeat_delay:
                if current_time - key_timers[key] > key_repeat_interval:
                    key_timers[key] = current_time
                    if key == pygame.K_LEFT:
                        game.move_left()
                    elif key == pygame.K_RIGHT:
                        game.move_right()
                    elif key == pygame.K_DOWN:
                        game.move_down()
                    elif key == pygame.K_UP:
                        game.rotate()
        else:
            key_timers[key] = 0

    # fill in background with white, then draw the grid and current block on top of it
    screen.fill(background)
    game.draw(screen)
    pygame.display.update()
    # 60 fps
    clock.tick(200)
