#cython: language_level=3
##
##	NP(Number Place) Solution Module
##
##	solve a Number Place problem with basic mdthods.
##
##(c) 2019-2021  FUJIWARA Hirofumi, Knowledge Engineering Center, Time Intermedia, Inc.
## This code is licensed under MIT license (see LICENSE.txt for details)

import parameter
import  random
import  sys
import NP
import numpy as np
import  parameter

SIZE = parameter.SIZE
SUBSIZE = parameter.SUBSIZE

REPLACE = 10

board = np.array( [ [6,9,5, 3,4,1, 8,7,2], 
                    [7,2,3, 9,8,5, 4,6,1],
                    [8,4,1, 6,2,7, 5,3,9],
                    [5,1,6, 8,3,2, 9,4,7],
                    [9,3,7, 1,6,4, 2,5,8],
                    [2,8,4, 7,5,9, 6,1,3],
                    [1,7,2, 4,9,6, 3,8,5],
                    [3,6,9, 5,1,8, 7,2,4],
                    [4,5,8, 2,7,3, 1,9,6]])

def getANewSolution():
    for i in range(REPLACE):
        line1 = random.randrange(SIZE)
        line2 = line1+1
        if line2 % SUBSIZE == 0:
            line2 -= SUBSIZE
        if i % 2 == 0:
            exchangeVline( line1, line2 )
        else:
            exchangeHline( line1, line2 )
    return board

def exchangeHline( r1, r2 ):
    for c in range(SIZE):
        board[r2][c], board[r1][c] = board[r1][c], board[r2][c]

def exchangeVline( c1, c2 ):
    for r in range(SIZE):
        board[r][c2], board[r][c1] = board[r][c1], board[r][c2]

## main for test  -------------------------------------------------
def main():
    for i in range(10):
        bd = getANewSolution()
        print("No.",i)
        NP.printBoard(sys.stdout,bd)

if __name__ == '__main__':
    main()

    
