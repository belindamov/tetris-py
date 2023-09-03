import pygame
import sys
from game import *
from colours import Colours

pygame.init()
background = (20, 20, 20)

title_font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

score_surface = title_font.render("Score", True, Colours.white)
score_rect = pygame.Rect(320, 55, 170, 60)

next_block_surface = title_font.render("Next", True, Colours.white)
next_block_rect = pygame.Rect(320, 215, 170, 180)

game_over_surface = title_font.render("GAME OVER", True, Colours.white)
game_over_outline = title_font.render("GAME OVER", True, Colours.black)

game_over_surface2 = small_font.render("Press ENTER", True, Colours.white)
game_over_outline2 = small_font.render("Press ENTER", True, Colours.black)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris (Python)")
clock = pygame.time.Clock()

game = Game()

# increase timer by 200 ms with every user event
game_update = pygame.USEREVENT
pygame.time.set_timer(game_update, 200)

# delays in ms when you hold down the keys
key_repeat_delay = 60
key_repeat_interval = 65

key_timers = {
    pygame.K_LEFT: 0,
    pygame.K_RIGHT: 0,
    pygame.K_DOWN: 0,
}

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # if game over, click enter to restart
            if game.game_over:
                if event.key == pygame.K_RETURN:
                    game.game_over = False
                    game.reset()
            # if space is pressed, automatically place the block
            if event.key == pygame.K_SPACE and not game.game_over:
                game.spacebar_auto_place()
                game.update_score(0, 2)
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()
        # automatic tetromino moving down
        if event.type == game_update and not game.game_over:
            game.move_down()

    # down, left, and right controls
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
        else:
            key_timers[key] = 0

    # current score
    score_num_surface = title_font.render(str(game.score), True, Colours.white)
    # fill in background with white, then draw the grid and current block on top of it
    screen.fill(background)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_block_surface, (375, 180, 50, 50))

    # draw the rectangle for the score
    pygame.draw.rect(screen, Colours.grey_pink, score_rect, 0, 10)
    # display the score
    screen.blit(score_num_surface, score_num_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
    # draw the rectangle that displays the next tetromino
    pygame.draw.rect(screen, Colours.grey_pink, next_block_rect, 0, 10)
    game.draw(screen)

    if game.game_over:
        # create an outline for the game over text by drawing the text in every offset direction
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    screen.blit(game_over_outline, (77 - dx, 260 - dy))
                    screen.blit(game_over_outline2, (100 - dx, 300 - dy))
        # display the game over text
        screen.blit(game_over_surface, (77, 260))
        screen.blit(game_over_surface2, (100, 300))

    pygame.display.update()
    # 60 fps
    clock.tick(60)
