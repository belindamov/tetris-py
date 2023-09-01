import pygame
import sys

pygame.init()
pink = (237, 192, 227)

screen = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Tetris (Python)")
clock = pygame.time.Clock()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(pink)
    pygame.display.update()
    # 60 fps
    clock.tick(60)
