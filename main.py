import pygame
import sys
from grid import *

pygame.init()
background = (245, 225, 252)

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris (Python)")
clock = pygame.time.Clock()

game_grid = Grid()
game_grid.print_grid()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(background)
    game_grid.draw(screen)
    pygame.display.update()
    # 60 fps
    clock.tick(60)
