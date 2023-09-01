from colours import *


class Block:
    def __init__(self, block_type):
        self.type = block_type
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.colours = Colours.get_cell_colours()
    def draw(self, screen):
        pass

