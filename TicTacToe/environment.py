import numpy as np
import random
import copy
from utils import *

class environment:
    
    def __init__(self, base=3, random_state=None):
        
        self.base = base
        self.side = base**2
        self.board = np.zeros((self.base, self.base))
        self.available_positions = None
        self.unavailable_position = None
        self.current_state = self.board
        self.next_state = self.board
        self.random_state = random_state
        self.last_play = None

    def single_play(self, action, state):
        
        # Action is a tuple formed by (row, col, number)
        
        position = action[0:2]
        symbol = action[2]
        
        number = symbol2num(symbol)
        
        unavailable_positions = np.argwhere(state != 0)
        if list(position) in unavailable_positions.tolist():
            raise ValueError('Select an available position.')
            
        if (self.last_play == symbol) and (symbol is not None):  
            print('It is not your time to play, let your opponent have fun too!')
        else:
            self.last_play = symbol
              
            stop = self._check_board(state)

            if not stop:

                self.current_state = state.copy()

                if number not in (1, 2):
                    raise ValueError('number should be either 1 or 2.')
                else:
                    state[position[0], position[1]] = number

                self.next_state = state.copy()

            else:
                self.current_state = state.copy()
                self.next_state = state.copy()

        self.available_positions = np.argwhere(state == 0)
        self.unavailable_positions = np.argwhere(state != 0)
       
     
    @staticmethod
    def _check_board(state):
        
        nrow, ncol = state.shape
        diag = np.diag(state)
        adiag = np.fliplr(state).diagonal()
        
        stop = False
        if len(set(diag)) == 1 and diag[0] != 0:
            stop = True
        elif len(set(adiag)) == 1 and adiag[0] != 0:
            stop = True
        else:
           
            for i in range(nrow):
                u = state[i,:]
                if len(set(u)) == 1 and u[0] != 0:
                    stop = True
                    
            if not stop:
                for i in range(nrow):
                    u = state[:,i]
                    if len(set(u)) == 1 and u[0] != 0:
                        stop = True
                
        return stop

    
    def reset(self):
     
        self.board = np.zeros((self.base, self.base))
        self.available_positions = None
        self.unavailable_position = None
        self.current_state = self.board
        self.next_state = self.board

    @staticmethod
    def print_board(board):
        
        side  = np.shape(board)[0]
        #board_print = []
        
        for i in range(side):
            
            row = []
            for j in range(side):
                
                symbol = num2symbol(board[i, j])
                row.append(symbol)
            
            print(row)
                    
        
        
        
        