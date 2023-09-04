import pygame.time

from block import Block
from blocks import SBlock
from copyblocks import *
from grid import *
from blocks import *
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.copy = self.make_copy()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.start_time = 0
        self.score = 0

    def get_random_block(self):
        # if list is empty, replace it
        if len(self.blocks) == 0:
            self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        # randomly sample without replacement
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        self.move_copy_outline()
        self.copy.draw(screen, 11, 11, outline=True)

        x_pos = 255 if self.next_block.type in (3, 4) else 270
        y_pos = 290 if self.next_block.type == 3 else (280 if self.next_block.type == 4 else 270)
        self.next_block.draw(screen, x_pos, y_pos)

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_in_border() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_in_border() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        # positive row increment means down
        self.current_block.move(1, 0)
        if not self.block_in_border() or not self.block_fits():
            self.current_block.move(-1, 0)
            if pygame.time.get_ticks() - self.start_time >= 2500:
                self.lock_in_place()
                self.update_score(0, 1)

    def rotate(self):
        self.current_block.rotate()
        if not self.block_in_border() or not self.block_fits():
            # attempt to move tetromino left
            self.move_left()
            if not self.block_in_border() or not self.block_fits():
                # attempt to move tetromino right
                self.move_right()
                if not self.block_in_border() or not self.block_fits():
                    # attempt to move tetromino up
                    self.current_block.move(-1, 0)

    def move_copy_left(self):
        self.copy.move(0, -1)
        if not self.block_in_border(False) or not self.block_fits():
            self.copy.move(0, 1)

    def move_copy_right(self):
        self.copy.move(0, 1)
        if not self.block_in_border(False) or not self.block_fits():
            self.copy.move(0, -1)

    def move_copy_outline(self):
        self.copy.row_offset = self.current_block.row_offset
        while self.block_in_border(False) and self.block_fits(False):
            self.copy.move(1, 0)
        self.copy.move(-1, 0)
        while self.copy.row_offset < self.current_block.row_offset:
            self.copy.move(1, 0)

    def rotate_copy(self):
        self.copy.rotate()
        if not self.block_in_border(False) or not self.block_fits(False):
            # attempt to move tetromino left
            self.move_copy_left()
            if not self.block_in_border(False) or not self.block_fits(False):
                # attempt to move tetromino right
                self.move_copy_right()
                if not self.block_in_border(False) or not self.block_fits(False):
                    # attempt to move tetromino up
                    self.copy.move(-1, 0)
        self.copy.col_offset = self.current_block.col_offset

    def move_both_left(self):
        self.move_left()
        self.move_copy_left()

    def move_both_right(self):
        self.move_right()
        self.move_copy_right()

    def rotate_both(self):
        self.rotate()
        self.rotate_copy()

    def spacebar_auto_place(self):
        current_block = self.current_block
        while self.block_in_border() and self.block_fits() and current_block == self.current_block:
            self.current_block.move(1, 0)
        self.current_block.move(-1, 0)
        self.lock_in_place()

    def make_copy(self):
        copy = None
        types = {
            1: CLBlock(),
            2: CJBlock(),
            3: CIBlock(),
            4: COBlock(),
            5: CSBlock(),
            6: CTBlock(),
            7: CZBlock()
        }
        for key in types:
            if self.current_block.type == key:
                copy = types[key]
        return copy

    def block_in_border(self, current=True):
        # current = True if self.current_block, = False if self.copy
        tiles = self.current_block.get_cell_positions() if current else self.copy.get_cell_positions()
        # if any position has a tile out of the border, return False
        return all(
            self.grid.inside_border(tile.row, tile.col) for tile in tiles)

    def empty_below(self):
        tiles = self.copy.get_cell_positions()
        for tile in tiles:
            if tile.row == 19 or not self.grid.is_empty(tile.row + 1, tile.col):
                return False
        return True

    def block_fits(self, current=True):
        tiles = self.current_block.get_cell_positions() if current else self.copy.get_cell_positions()
        return all(
            self.grid.is_empty(tile.row, tile.col) for tile in tiles)

    def lock_in_place(self):
        self.start_time = pygame.time.get_ticks()
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.type
        self.current_block = self.next_block
        self.copy = self.make_copy()
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def update_score(self, lines_cleared, moved_down):
        scores = [0, 100, 300, 500, 800]
        self.score += scores[lines_cleared] + moved_down
