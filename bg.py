import pygame
from colours import Colours

class Grid:
    def __init__(self):
        self.column_number = 10
        self.row_number = 20
        self.cell_size = 35
        self.grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.colours = Colours.get_cell_colour()

    def get_grid(self):
        return self.grid
    
    def show_grid(self):
        for rows in range(self.row_number):
            for columns in range(self.column_number):
                print (self.grid[rows][columns], end = " ")
            print()

    def is_inside(self, rows, columns):
        if rows >= 0 and rows < self.row_number and columns >= 0 and columns < self.column_number:
            return True
        return False

    def draw(self, screen):
        for rows in range(self.row_number):
            for columns in range(self.column_number):
                cell_value = self.grid[rows][columns]
                cell_x = columns * self.cell_size
                cell_y = rows * self.cell_size
                cell_width = self.cell_size
                cell_height = self.cell_size
                cell_rect = pygame.Rect(cell_x +190, cell_y + 11, cell_width -1, cell_height -1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)

    def is_empty(self, rows, columns):
        if self.grid[rows][columns] == 0:
            return True
        return False
    
    def is_row_full(self, rows):
        for columns in range (self.column_number):
            if self.grid[rows][columns] == 0:
                return False
        return True
    
    def is_row_empty(self,rows):
        for columns in range (self.column_number):
            if(self.grid[rows][columns] != 0):
                return False
        return True
    
    def get_peak_height(self):
        for rows in range(self.row_number):
            if(self.is_row_empty(19-rows)):
                return 19-rows
        return 0
    
    def clear_row(self, rows):
        for columns in range(self.column_number):
            self.grid[rows][columns] = 0

    def move_row_down(self, rows, row_number):
        for columns in range (self.column_number):
            self.grid[rows + row_number][columns] = self.grid[rows][columns]
            self.grid[rows][columns] = 0

    def clear_full_rows(self):
        completed = 0
        for rows in range(self.row_number -1, 0, -1):
            if self.is_row_full(rows):
                self.clear_row(rows)
                completed +=1
            elif completed > 0:
                self.move_row_down(rows, completed)
        return completed

    def reset(self):
        for rows in range (self.row_number):
            for columns in range (self.column_number):
                self.grid[rows][columns] = 0