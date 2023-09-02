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
        self.current_block.draw(screen)

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_in_border():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_in_border():
            self.current_block.move(0, -1)

    def move_down(self):
        # positive row increment means down
        self.current_block.move(1, 0)
        if not self.block_in_border():
            self.current_block.move(-1, 0)
            self.lock_in_place()

    def block_in_border(self):
        tiles = self.current_block.get_cell_positions()
        # if any position has a tile out of the border, return False
        for tile in tiles:
            if not self.grid.inside_border(tile.row, tile.col):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_in_border():
            # attempt to move tetromino left
            self.move_left()
            if not self.block_in_border():
                # attempt to move tetromino right
                self.move_right()

    def lock_in_place(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.type
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
