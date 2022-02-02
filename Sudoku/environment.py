import numpy as np
import random
from utils import *

class environment:
    
    def __init__(self, known_num=10, base=3, random_state=None):
        
        self.base = base
        self.side = base**2
        self.known_num = known_num
        self.board = np.zeros((self.side, self.side))
        self.available_positions = None
        self.unavailable_position = None
        self.current_state = self.board
        self.next_state = self.board
        self.block_index = None
        self.block_position = None
        self.random_state = random_state

    def single_play(self, action, state):
        
        # Action is a tuple formed by (row, col, number)
        
        position = action[0:2]
        number = action[2]
        
        # Check current available positions: however the game will ensure 
        # that only available positions are considered.
        unavailable_positions = np.argwhere(state != 0)
        if list(position) in unavailable_positions.tolist():
            raise ValueError('Select an available position.')
        else:
            
            valid = self._check_single_play(action, state)
     
        if valid:
            
            self.current_state = state.copy()

            if number > self.side and number < 1:
                raise ValueError('number should be an integer 1<=number<=9.')
            else:
                state[position[0], position[1]] = number

            self.next_state = state.copy()
            #reward = 1
            
        else:
            
            self.current_state = state.copy()
            self.next_state = state.copy()
            #reward = -1
            
        self.available_positions = np.argwhere(state == 0)
        self.unavailable_positions = np.argwhere(state != 0)
       
 
    def _check_single_play(self, action, state):
        
        position = action[0:2]
        number = action[2]
        
        row = state[position[0], :]
        col = state[:, position[1]]
        
        block_index = self.block_index
        block_position = self.block_position
        idx = int(block_index[position[0], position[1]])
        
        p = block_position[idx]
        prow = p[0]
        pcol = p[1]
        
        block_mat = state[prow[0]:prow[1], pcol[0]:pcol[1]]
        
        valid = True
        if (number in row) or (number in col) or (number in block_mat):
            valid = False

        return valid
    
    def _get_acceptable_num(self, position, state):
        
        row = state[position[0], :]
        col = state[:, position[1]]
        
        block_index = self.block_index
        block_position = self.block_position
        idx = int(block_index[position[0], position[1]])
        
        p = block_position[idx]
        prow = p[0]
        pcol = p[1]
        
        block_mat = state[prow[0]:prow[1], pcol[0]:pcol[1]]
        
        conflicting_numbers = set(row.tolist() + col.tolist() + block_mat.flatten().tolist())
        conflicting_numbers = list(conflicting_numbers)
        conflicting_numbers = [num for num in conflicting_numbers if num != 0]
        acceptable_numbers = [num for num in range(1, self.side + 1) if (num not in conflicting_numbers)]
        
        return acceptable_numbers, conflicting_numbers
    
    def _get_existing_num(self, position, state):
        
        # Get the existing numbers in the rows and columns corresponding to position.
      
        row = state[position[0], :]
        col = state[:, position[1]]
        
        block_index = self.block_index
        block_position = self.block_position
        idx = int(block_index[position[0], position[1]])
        
        p = block_position[idx]
        prow = p[0]
        pcol = p[1]
        
        block_mat = state[prow[0]:prow[1], pcol[0]:pcol[1]]
        
        num_row = [num for num in row.tolist() if num != 0]
        num_col = [num for num in col.tolist() if num != 0]
        num_block = [num for num in block_mat.flatten().tolist() if num != 0]
        
        return num_row, num_col, num_block
        
    
    def create_environment(self):
        
        random.seed(self.random_state)
        self.block_index, self.block_position = block_index_matrix(self.base)
        board_full = self._create_board()
        board = self._delete_numbers(board_full, self.known_num)
        self.board = board
        
        self.available_positions = np.argwhere(board == 0)
        
        self.current_state = board
        #print(board)
        #print(' ')
        #print(board_null)
        #self.print_board(board_null)
        
    @staticmethod
    def _delete_numbers(board, known_num):
        
        board_ = board.copy()
        side = len(board_[0,:])
        squares = side*side
        
        #empties = squares * 3//4
        empties = squares - known_num

        for p in sample(range(squares),empties):
            board_[p//side][p%side] = 0
            
        return board_
        
    def _create_board(self):
        
        # Retrieved from: https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
        
        base  = self.base
        side  = self.side

        rBase = range(base) 
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))

        # produce board using randomized baseline pattern
        board = [ [nums[pattern(r,c, base, side)] for c in cols] for r in rows ]

        # for line in board: print(line)
        board = np.array(board)
        
        return board
    
    @staticmethod
    def print_board(board):
        base  = int(np.sqrt(board.shape[0]))
        side  = board.shape[0]
        line0  = expandLine("╔═══╤═══╦═══╗", base)
        line1  = expandLine("║ . │ . ║ . ║", base)
        line2  = expandLine("╟───┼───╫───╢", base)
        line3  = expandLine("╠═══╪═══╬═══╣", base)
        line4  = expandLine("╚═══╧═══╩═══╝", base)

        symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nums   = [ [""]+[symbol[n] for n in row] for row in board ]
        print(line0)
        for r in range(1,side+1):
            print( "".join(n+s for n,s in zip(nums[r-1],line1.split("."))) )
            print([line2,line3,line4][(r%side==0)+(r%base==0)])
        
        
        
        