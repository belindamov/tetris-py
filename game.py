import pygame
from block import Block
from blocks import LBlock, JBlock, IBlock, OBlock, SBlock, TBlock, ZBlock
from copyblocks import CLBlock, CJBlock, CIBlock, COBlock, CSBlock, CTBlock, CZBlock
from grid import Grid
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.copy = self.make_copy()
        self.next_block = self.get_random_block()
        self.next_next_block = self.get_random_block()
        self.next_next_next_block = self.get_random_block()
        self.next_next_next_next_block = self.get_random_block()
        self.game_over = False
        self.start_time = 0
        self.score = 0
        self.block_held = None
        self.theme_song = pygame.mixer.Sound('sounds/theme.ogg')
        self.theme_song.set_volume(0.5)
        self.theme_song.play(-1)
        self.place_sound = pygame.mixer.Sound('sounds/placedown.mp3')
        self.place_sound.set_volume(3)
        # temporary
        self.line_sound = pygame.mixer.Sound('sounds/line_clear.mp3')
        self.line_sound.set_volume(3)

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
        self.current_block.draw(screen, 140, 11)
        self.move_copy_outline()
        self.copy.draw(screen, 140, 11, outline=True)

        x_pos1 = 385 if self.next_block.type in (3, 4) else 400
        x_pos2 = 385 if self.next_next_block.type in (3, 4) else 400
        x_pos3 = 385 if self.next_next_next_block.type in (3, 4) else 400
        x_pos4 = 385 if self.next_next_next_next_block.type in (3, 4) else 400

        y_pos1 = 200 if self.next_block.type == 3 else 185
        y_pos2 = 290 if self.next_next_block.type == 3 else 275
        y_pos3 = 380 if self.next_next_next_block.type == 3 else 365
        y_pos4 = 470 if self.next_next_next_next_block.type == 3 else 455

        if self.block_held is not None:
            x_pos5 = 12 if self.block_held.type == 3 else 20
            y_pos5 = 23 if self.block_held.type == 3 else 26
            self.block_held.draw(screen, x_pos5, y_pos5)

        self.next_block.draw(screen, x_pos1, y_pos1)
        self.next_next_block.draw(screen, x_pos2, y_pos2)
        self.next_next_next_block.draw(screen, x_pos3, y_pos3)
        self.next_next_next_next_block.draw(screen, x_pos4, y_pos4)

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
        if not self.block_in_border(False) or (not self.block_fits() and not self.block_fits(False)):
            self.copy.move(0, 1)

    def move_copy_right(self):
        self.copy.move(0, 1)
        if not self.block_in_border(False) or (not self.block_fits() and not self.block_fits(False)):
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
        # get time that function is called
        self.start_time = pygame.time.get_ticks()
        tiles = self.current_block.get_cell_positions()
        # replace empty space with the tetromino
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.type
        # reassign the blocks accordingly
        self.current_block = self.next_block
        self.copy = self.make_copy()
        self.next_block = self.next_next_block
        self.next_next_block = self.next_next_next_block
        self.next_next_next_block = self.next_next_next_next_block
        self.next_next_next_next_block = self.get_random_block()
        # update score as needed if any rows are cleared
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.line_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True
        self.place_sound.play()

    def reset(self):
        self.grid.reset()
        self.blocks = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.copy = self.make_copy()
        self.next_block = self.get_random_block()
        self.next_next_block = self.get_random_block()
        self.next_next_next_block = self.get_random_block()
        self.next_next_next_next_block = self.get_random_block()
        self.block_held = None
        self.score = 0

    def update_score(self, lines_cleared, moved_down):
        scores = [0, 100, 300, 500, 800]
        self.score += scores[lines_cleared] + moved_down

    def hold_block(self):
        # if there is no block being held, assign the current block as the held block and reassign the blocks
        if self.block_held is None:
            self.block_held = self.current_block
            self.block_held.rotation_state = 0
            self.block_held.row_offset = 0
            self.block_held.col_offset = 0
            self.current_block = self.next_block
            self.copy = self.make_copy()
            self.next_block = self.next_next_block
            self.next_next_block = self.next_next_next_block
            self.next_next_next_block = self.next_next_next_next_block
            self.next_next_next_next_block = self.get_random_block()
        # if there is a block being held, replace the held block with the current block and play with held block
        else:
            self.block_held.row_offset = 0
            self.block_held.col_offset = 0
            self.current_block.row_offset = 0
            self.current_block.col_offset = 0
            og_held = self.block_held
            og_current = self.current_block
            self.current_block = og_held
            self.current_block.col_offset = 4 if self.current_block.type == 4 else 3
            self.copy = self.make_copy()
            self.block_held = og_current
            self.block_held.rotation_state = 0

