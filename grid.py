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
                cell_rect = pygame.Rect(j*self.cell_size + 11, i*self.cell_size + 11, self.cell_size - 1,
                                        self.cell_size - 1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)

    def inside_border(self, row, col):
        if (0 <= row < self.num_rows) and (0 <= col < self.num_cols):
            return True
        return False

    def is_empty(self, row, col):
        if self.grid[row][col] == 0:
            return True
        return False

    def is_row_full(self, row):
        for j in range(self.num_cols):
            if self.grid[row][j] == 0:
                return False
        return True

    def clear_row(self, row):
        for j in range(self.num_cols):
            self.grid[row][j] = 0

    def move_row_down(self, row, amount):
        for j in range(self.num_cols):
            self.grid[row+amount][j] = self.grid[row][j]
            self.grid[row][j] = 0

    def clear_full_rows(self):
        filled = 0
        for i in range(self.num_rows-1, 0, -1):
            if self.is_row_full(i):
                self.clear_row(i)
                filled += 1
            elif filled > 0:
                self.move_row_down(i, filled)
        return filled

    def reset(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.grid[i][j] = 0
