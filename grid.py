import pygame


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colours = self.get_cell_colours()

    def print_grid(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                print(self.grid[i][j], end=" ")
            print()

    def get_cell_colours(self):
        pink_white = (245, 225, 252)
        muted_pink = (156, 67, 133)
        purple_pink = (110, 66, 98)
        baby_pink = (209, 128, 168)
        salmon = (255, 94, 135)
        purple = (215, 125, 219)
        purple2 = (158, 12, 207)
        grey_purple = (109, 91, 115)
        return [baby_pink, muted_pink, purple_pink, pink_white, salmon, purple, purple2, grey_purple]

    def draw(self, screen):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell_value = self.grid[i][j]
                cell_rect = pygame.Rect(j*self.cell_size + 1, i*self.cell_size + 1, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)
