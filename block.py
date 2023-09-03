import self as self

from colours import *
import pygame
from position import *
from game import *
from grid import *


class Block:
    def __init__(self, block_type):
        self.grid = Grid()
        self.type = block_type
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.colours = Colours.get_cell_colours()
        self.row_offset = 0
        self.col_offset = 0

    def draw(self, screen, x_offset, y_offset):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(x_offset + tile.col * self.cell_size, y_offset + tile.row * self.cell_size,
                                    self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colours[self.type], tile_rect)

    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            new_position = Position(position.row + self.row_offset, position.col + self.col_offset)
            moved_tiles.append(new_position)
        return moved_tiles

    def rotate(self):
        self.rotation_state += 1
        # ensure rotation state does not go past the max amount of rotations
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0
