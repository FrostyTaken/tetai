from blocks import Blocks
from bg import Grid
from blockshape import *
from game import Game


#Handle Block Movement
class Bot:
    step = 0
    path = []
    placement = []
    def handle_block(self,game:Game):
        
        #Loadig The Data
        block = game.current_block
        grid = game.get_grid()
        if(game.state == "block_locked"):
            self.placement = self.find_placement_point(block,grid)
            if(self.placement):
                self.path = []
                self.path = self.find_placement_path(self.placement,game.current_block,grid)
                print(self.placement[1],self.placement[2],self.placement[6],self.placement[4],self.placement[5])
                if(self.path != None):
                    print(self.path)
                    self.step = len(self.path) -1 
                
                
        if(self.path != None):    
        
            if(self.path[self.step] == "down"):
                game.move_down()
                self.step -= 1
                return
            elif(self.path[self.step] == "right"):
                game.move_right()
                self.step -= 1
                return
            elif(self.path[self.step] == "left"):
                game.move_left()
                self.step -= 1
                return
            else:
                game.state = "nothing"
                if(game.current_block.rotation != self.path[self.step]):
                    game.rotate()
                else:
                    self.step -= 1
                return
        
        #Rotate The Block first
        elif(False):
            if(block.rotation != self.placement[6]):
                if(game.rotate()):
                    return
                else:
                    game.move_down()
                    print("moving down")
                return
            
            #Move The Block to Get To the point
            
            print("Placement Details:")
            print("X Position:", self.placement[1])
            print("Column Offset:", self.placement[2])
            print("Gap Changes:", self.placement[3])
            print("Block Height:", self.placement[4])
            print("Completed Rows:", self.placement[5])
            print("Target Rotation:", self.placement[6])
            print("Current Rotation:", block.rotation)
            #Get The X Pos Right
            if(self.placement[1] > block.col_offset):
                game.move_right()
                return
            if(self.placement[1] < block.col_offset):
                game.move_left()
                return
            
            #Get The Y pos Right afterwards
            game.move_down()
            return


    #Fidning The Point To Place The Block into Desired Position 
    def find_placement_point(self,block: Blocks,grid: Grid):
        
        #Calculate Possible Drops For All Scenarios
        drops = self.find_all_drops(block,grid)
        drops = [drop for drop in drops if len(drop) > 6]
        
        #Find The Best Drop
        drop = self.find_best_drop(drops,block,grid)
        x_pos = drop[0][0].x() + drop[1]
        y_pos = drop[0][0].y() + drop[2]

        return drop


    #Calculate Possible Drops For All Scenarios
    def find_all_drops(self,block: Blocks, grid:Grid):
        
        drops = [[]]
        height = grid.get_peak_height() 

    
        for i in range(len(block.cells)):
            result = self.find_all_drops_for_block_variant(block.cells[i],grid,height,i)
            if(len(result) > 0):
                drops.extend(result)
        
        
        final =[[]] 
        for i in range(len(drops)):
            if(len(drops[i]) > 0):
                final.append(drops[i])
                    
        return final
    
    def find_all_drops_for_block_variant(self,block:[],grid:Grid,height:int,rotation:int):
        drops = [[]]

        for i in range(grid.column_number+3):
            for j in range(grid.row_number-height+3):
                if(self.block_fits_into_position(block,grid,i-3,j-3)):
                    block_height = self.calculate_height(block,i-3,j-3)
                    gap_change = self.calculate_gap_changes(block,grid,i-3,j-3)
                    completed_rows = self.completed_row(block,i-3,j-3,grid,height)
                    score = (completed_rows*4.5) - (gap_change*10) - ((block_height  + j) * 1.5) 
                    drops.append([block,i-3,j-3,gap_change,block_height,completed_rows,rotation,score])
                    
        
        return drops

    #Finding The Best Drop
    def find_best_drop(self,drops:[[]],block:Blocks,grid:Grid):
        for drop in drops:
            if(self.find_placement_path(drop,block,grid) == None):
                drop[7] = -999999
        
   

        
        best_score = max(drops, key=lambda x: x[7])[7]
        drops = list(filter(lambda drop: drop[7] == best_score, drops))  
        
        return drops[0]
        
    #Checks All 4 Points to Find if the block can fit into that position               
    def block_fits_into_position(self,block:[],grid:Grid,x:int,y:int):
        for i in range(len(block)):
            x_pos = block[i].x() + x
            y_pos = block[i].y() + (grid.row_number - y -2)
            if(x_pos >= grid.column_number or y_pos >= grid.row_number or y_pos < 0 or x_pos < 0 or not grid.is_empty(y_pos,x_pos)):
                return False
            
        return True

    #Making A Score System For Each Drop
    #Calculating The Gap Changes
    def calculate_gap_changes(self,block:[],grid:Grid,x:int,y:int):
        count = 0
        poses = [[]]
        for i in range(len(block)):
            x_pos = block[i].x() + x
            y_pos = block[i].y() + (grid.row_number - y -2) + 1
            if(y_pos < grid.row_number and y_pos > 0 and grid.is_empty(y_pos,x_pos)):
                count += 1
                poses.append([x_pos,y_pos])
        
        for i in range(len(block)):
            x_pos = block[i].x() + x
            y_pos = block[i].y() + (grid.row_number - y -2)
            for j in range(len(poses)):
                if(len(poses[j]) > 0 and poses[j][0] == x_pos and poses[j][1] == y_pos):
                    count -= 1
        
        return count

    #calculating the height generated by the block
    def calculate_height(self,block:[],x:int,y:int):  
        max_height = 0  
        for i in range(len(block)):
            y_pos = block[i].y() + y 
            if(y_pos > max_height):
                max_height = y_pos
                
        return max_height

    #calculate if resulting placement completes any rows and based up on the result we'll give score
    def completed_row(self,block:[],x:int,y:int,grid:Grid,height:int):
        completed_rows = 0
        new_list = [[]]
        for i in range(len(block)):
            y_pos = block[i].y() + (grid.row_number - y -2)
            x_pos = block[i].x() + x
            new_list.append([y_pos,x_pos])
            
        for i in range(height):
            fail = False
            for j in range(grid.column_number):
                suceed = True
                if(grid.is_empty(grid.row_number -1 -i,j)):
                    suceed = False
                    for k in range(len(new_list)):
                        if(len(new_list[k]) > 0 and new_list[k][0] == grid.row_number -1 -i and new_list[k][1] == j):
                            print(new_list[k])
                            suceed = True
                if(not suceed):
                    fail = True
                
            if(not fail):
                completed_rows += 1
                
        return completed_rows

    
    #Finding The Best Path
    def find_placement_path(self,placement:[],block:Blocks,grid:Grid):
        self.path_found = False
        self.found_path = []
        path = ["down","down"]
        x = placement[1]
        y = placement[2]
        self.down_arm(x,y,block,grid,placement.copy(),path.copy())
        self.right_arm(x,y,block,grid,placement.copy(),path.copy())
        self.left_arm(x,y,block,grid,placement.copy(),path.copy())
        if(not self.path_found):
            return None
        else:
            return (self.found_path)
            
    
        #Checks Wheter the block can move in between stated 2 points   
    #returns rotation value that's capable of the movment,
    #returns -1 if movement is not possible
    def can_block_move(self,x:int,y:int,new_x:int,new_y:int,block:Blocks,grid:Grid,currrent_rotation:int):
        
        differnce = abs(x - new_x) + abs(y-new_y)
        if(differnce != 1):
            return -1
        
        fits_prev = self.block_fits_into_position(block.cells[currrent_rotation],grid,x,y)
        fits_curr = self.block_fits_into_position(block.cells[currrent_rotation],grid,new_x,new_y)
        
        if(fits_prev and fits_curr):
            return currrent_rotation
        
        for rotation in range(len(block.cells)):
            fits_prev = self.block_fits_into_position(block.cells[rotation],grid,x,y)
            fits_curr = self.block_fits_into_position(block.cells[rotation],grid,new_x,new_y)
            if(fits_prev and fits_curr):
                return rotation
            else:
                return -1
        
        return -1
    
    #returns how many times you need to rotate it        
    def fix_rotation(self,old:int,new:int):
        difference = new-old
        if(difference < 0):
            difference += 4 
        return difference
        
    path_found = False
    found_path = []
    
    def left_arm(self,x:int,y:int,block:Blocks,grid:Grid,placement:[],direciton:[]):
        if(self.path_found):
            return None
        if(block.col_offset == x and block.row_offset == grid.row_number - y-2):
            self.path_found = True
            self.found_path = direciton
            return direciton
        if(x == 0):
            return 
        
        
        new_x = x-1
        new_y = y
        new_placement = placement
        #IF the Block can move in between those positions
        
        can_move = self.can_block_move(x,y,new_x,new_y,block,grid,placement[6])
        
        if (can_move == -1):
            return
        else:
            new_direction = direciton.copy()
            new_direction.append(placement[6])
            new_direction.append("right")
            new_placement[6] = can_move
        
        #recall the same function
        if(not self.path_found):
            self.left_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())
            self.down_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())      

            
    def right_arm(self,x:int,y:int,block:Blocks,grid:Grid,placement:[],direciton:[]):
        if(self.path_found):
            return None
        if(block.col_offset == x and block.row_offset == grid.row_number - y-2):
            self.path_found = True
            self.found_path = direciton
            return direciton
        if(x == grid.column_number-1):
            return 
        
        new_x = x+1
        new_y = y
        new_placement = placement
        #IF the Block can move in between those positions
        
        can_move = self.can_block_move(x,y,new_x,new_y,block,grid,placement[6])
        
        if (can_move == -1):
            return None
        else:
            new_direction = direciton.copy()
            new_direction.append(placement[6])
            new_direction.append("left")
            new_placement[6] = can_move
        
        #recall the same function
        if(not self.path_found):
            self.right_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())      
            self.down_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())      


    def down_arm(self,x:int,y:int,block:Blocks,grid:Grid,placement:[],direciton:[]):

        if(self.path_found):
            return None
        if(block.col_offset == x and block.row_offset == grid.row_number - y-2):
            self.path_found = True
            self.found_path = direciton
            return direciton
        if(y == grid.row_number -1):
            return 
        
        new_x = x
        new_y = y+1
        new_placement = placement
        #IF the Block can move in between those positions
        
        can_move = self.can_block_move(x,y,new_x,new_y,block,grid,placement[6])
        
        if (can_move == -1):
            return
        else:
            new_direction = direciton.copy()
            new_direction.append(placement[6])
            new_direction.append("down")
            new_placement[6] = can_move
        
        #recall the same function
        if(not self.path_found):
            self.down_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())   
            self.left_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())   
            self.right_arm(new_x,new_y,block,grid,new_placement,new_direction.copy())   