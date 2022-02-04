from random import sample
import numpy as np

def num2symbol(num):

    if num == 0:
        symbol = '_'
    elif num == 1:
        symbol = 'X'
    elif num == 2:
        symbol = 'O'
    
    return symbol

def symbol2num(symbol):

    if symbol == '_':
        num = 0
    elif symbol == 'X':
        num = 1
    elif symbol == 'O':
        num = 2
    
    return num

def block_index_matrix(base):
    
    side = base**2

    c = 0
    posi = []
    M = np.zeros((side, side))
    for i in np.arange(0,side, base):
        for j in np.arange(0,side, base):
            posi.append([[i,i+base], [j,j+base]])
            M[i:i+base, j:j+base] = int(c)
            c+=1
            
    posi = np.array(posi)
    return M, posi

# pattern for a baseline valid solution
def pattern(r,c, base, side): 
    return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
def shuffle(s): 
    return sample(s,len(s))

def expandLine(line, base):
    return line[0]+line[5:9].join([line[1:5]*(base-1)]*base)+line[9:13]