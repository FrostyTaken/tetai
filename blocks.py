from colours import Colours
from pos import Pos
import pygame

class Blocks:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 35
        self.rotation = 0
        self.colours = Colours.get_cell_colour()
        self.col_offset = 0
        self.row_offset = 0
    
    def draw (self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.columns * self.cell_size, offset_y + tile.rows * self.cell_size,self.cell_size -1, self.cell_size -1)
            pygame.draw.rect(screen, self.colours[self.id], tile_rect)

    def move(self, rows, columns):
        self.col_offset += columns
        self.row_offset += rows

    def get_cell_positions(self):
        tiles = self.cells[self.rotation]
        moved_tiles = []
        for pos in tiles:
            pos = Pos(pos.rows + self.row_offset, pos.columns + self.col_offset)
            moved_tiles.append(pos)
        return moved_tiles
    
    def rotate(self):
        self.rotation += 1
        if self.rotation == len(self.cells):
            self.rotation = 0

    def undo_rotation(self):
        self.rotation -= 1
        if self.rotation == -1:
            self.rotation = len(self.cells) - 1