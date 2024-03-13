from bg import Grid
from blockshape import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [OBlock(), ZBlock(), IBlock(), LBlock(), TBlock(), SBlock(), JBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.state = "block_locked"

    def get_grid(self):
        return self.grid
    
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [OBlock(), ZBlock(), IBlock(), LBlock(), TBlock(), SBlock(), JBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        self.state = "nothing"
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        self.state = "nothing"
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
        
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            self.state = "block_locked"
        else:
            self.state = "nothing"


    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.rows, tile.columns) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 190, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, -80, 285)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, -80, 270)
        else:
            self.next_block.draw(screen, -60, 270)

    def rotate(self):
        self.current_block.rotate()
        self.state = "nothing"
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
            return False
        return True

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for pos in tiles:
            self.grid.grid[pos.rows][pos.columns] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.rows, tile.columns) == False:
                return False
        return True
    
    def reset(self):
        self.grid.reset()
        self.blocks = [OBlock(), ZBlock(), IBlock(), LBlock(), TBlock(), SBlock(), JBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        if lines_cleared == 4:
            self.score += 800
        self.score += move_down_points