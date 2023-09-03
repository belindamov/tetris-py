import pygame.time

from block import Block
from grid import *
from block import *
from blocks import *
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
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

    # def calculate_shadow_offset(self):
    #     copy = Block(self.current_block.type)
    #     copy.cells = self.current_block.get_cell_positions()
    #     copy.row_offset = 580
    #     tiles = copy.get_cell_positions()
    #     for tile in tiles:
    #         if not self.grid.is_empty(tile.row, tile.col):
    #             copy.row_offset -= 30
    #     return copy.row_offset

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        # 580 bottom, -30 up each row
        # self.current_block.draw_outline(screen, 11)

        if self.next_block.type == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.type == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

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

    def spacebar_auto_place(self):
        current_block = self.current_block
        while self.block_in_border() and self.block_fits() and current_block == self.current_block:
            self.current_block.move(1, 0)
            if not self.block_in_border() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_in_place()

    def block_in_border(self):
        tiles = self.current_block.get_cell_positions()
        # if any position has a tile out of the border, return False
        for tile in tiles:
            if not self.grid.inside_border(tile.row, tile.col):
                return False
        return True

    def lock_in_place(self):
        self.start_time = pygame.time.get_ticks()
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.type
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.col):
                return False
        return True

    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def update_score(self, lines_cleared, moved_down):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800
        self.score += moved_down
