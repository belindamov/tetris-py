import pygame
from colours import *


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colours = Colours.get_cell_colours()

    def print_grid(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(self.grid[i][j], end=" ")
            print()

    def draw(self, screen):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell_value = self.grid[i][j]
                cell_rect = pygame.Rect(j*self.cell_size + 1, i*self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)

    def inside_border(self, row, col):
        if (0 <= row < self.num_rows) and (0 <= col < self.num_cols):
            return True
        return False
