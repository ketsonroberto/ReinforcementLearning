import numpy as np
import random
from utils import *

class agent:
    
    def __init__(self, environment=None, random_state=None):
        
        self.random_state = random_state
        self.environment = environment
        self.win = False
        self.game_over = False
        
        
    def play_game(self):
        
        np.random.seed(self.random_state)
        available_positions = self.environment.available_positions
        np.random.shuffle(available_positions)
        
        #if len(self.available_positions)==0:
        #    self.win = True
     
        num_row=None
        num_col=None
        num_block=None
        if len(available_positions) !=0:
            available_positions = self.environment.available_positions
            np.random.shuffle(available_positions)
            
            position = (available_positions[0][0], available_positions[0][1])
            acceptable_numbers, _ = self.environment._get_acceptable_num(position, self.environment.board)
            acceptable_numbers = np.array(acceptable_numbers)
            np.random.shuffle(acceptable_numbers)
            #print(self.environment.win, acceptable_numbers)
            
            num_row, num_col, num_block = self.environment._get_existing_num(position, self.environment.board)
            
            if len(acceptable_numbers) != 0:
                number = acceptable_numbers[0]
                #number = np.random.randint(1, high=10)
                action = (available_positions[0][0], available_positions[0][1], number)
                self.environment.single_play(action, self.environment.board)
            else:
                self.game_over = True
        else:
            self.win = True
            
        r = self._get_reward(num_row, num_col, num_block, self.win, self.game_over, self.environment.side)
        
        return r
            
    @staticmethod
    def _get_reward(num_row, num_col, num_block, win, game_over, side):
        
        if win:
            reward = 2
        elif game_over:
            reward = -2
        else:
            n = 3 * (side - 1)
            n_r = len(num_row) 
            n_c = len(num_col) 
            n_b = len(num_block) 
            reward = (n_r + n_c + n_b) / n

        return reward
    
    
                
  
        
 
    