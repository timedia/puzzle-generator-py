##	NP(Number Place) Solver Module
##
##	This class has the main method.
##
##(c) 2019-2021  FUJIWARA Hirofumi, Knowledge Engineering Center, Time Intermedia, Inc.
## This code is licensed under MIT license (see LICENSE.txt for details)
##

import  parameter
import  numpy as np
import  sys
import  NP

SIZE = parameter.SIZE
SUBSIZE = parameter.SUBSIZE

board       = None
candidate   = None

def solve( bd ):
    initialize()
    blanks = setProblem(bd)
    
    if blanks < 0:
        return -1

    try:
        checkLoop()
    except:
        return -1

    return blankCount()

def initialize():
    global candidate, board
    
    board = np.zeros((SIZE,SIZE)).astype(int)
    candidate = np.ones((SIZE,SIZE,SIZE+1)).astype(int)
    

def setProblem( bd ):
    try:
        for r in range(SIZE):
            for c in range(SIZE):
                if bd[r][c] != 0:
                    setValue( r, c, bd[r][c] )
    except:
        return -1
    
    return blankCount()


def checkLoop():    
    changed = True
    while changed:
        changed = False

        for r in range(0,SIZE,SUBSIZE):         # 3x3 Blocok Check
            for c in range(0,SIZE,SUBSIZE):
                if checkBlock(c,r):
                    changed = True
        if changed:
            continue

        for r in range(SIZE):            # HLine check
            if checkHline(r):
                changed = True

        for c in range(SIZE):            # VLine check
            if checkVline(c):
                changed = True

        if changed:
            continue

        for r in range(SIZE):            # Cell check
            for c in range(SIZE):
                if checkCell(c,r):
                    changed = True

        if blankCount() == 0:
            break

## --------------------		set value	--------------------

def setValue( r,  c, v ):    
    if candidate[r][c][v]==0:
        raise Exception

    if board[r][c]!=0:
        if board[r][c] != v:
            raise Exception
        return

    board[r][c] = v
    for n in range(1,SIZE+1):
        candidate[r][c][n] = 0
    
    r0 = (r//SUBSIZE)*SUBSIZE
    c0 = (c//SUBSIZE)*SUBSIZE

    for i in range(SIZE):
        candidate[r][i][v] = 0
        candidate[i][c][v] = 0
        candidate[r0+(i//SUBSIZE)][c0+i%SUBSIZE][v] = 0

## --------------------		get value	--------------------

def getAnswer():
    ans = np.zeros((SIZE,SIZE)).astype(int)        
    NP.copyBoard( board, ans )
    return ans

def getValue(r,c):
    return board[r][c]

def getCandidate(r,c):
    return candidate[r][c]

## --------------------		print	--------------------

def printCandidate():
    print("Solver.candidate:")

    for r in range(SIZE):
        for c in range(SIZE):
            for n in range(1,SIZE+1):
                if candidate[r][c][n]!= 0:
                    h = n
                else:
                    h = 0
                if h!=0:
                    print(h,end='')
                else:
                    print('-',end='')
            print(' ',end='')
        print()
        

def printBoard():
    sys.stdeerr.write("Solver.board:\n")
    NP.printBoard(sys.stderr,board)

## --------------------	check box/line/cell & set	--------------------

def checkBlock( c0, r0 ):    
    changed = False
    for n in range(1,SIZE+1):
        exist = False
        cnt = 0
        col = 0
        row = 0
        for r in range(r0,r0+SUBSIZE):
            for c in range(c0,c0+SUBSIZE):
                can = candidate[r][c][n]
                if board[r][c] == n:
                    exist = True
                if can == 1:
                    cnt += 1
                    col = c
                    row = r
            
        if not exist:
            if cnt == 1:
                setValue( row, col, n )
                changed = True
            elif cnt == 0:
                raise Exception

    return changed		

def checkHline(r):    
    changed = False
    for n in range(1,SIZE+1):
        exist = False
        cnt = 0
        col = 0
        for c in range(SIZE):
            if board[r][c] == n:
                exist = True
            if candidate[r][c][n]!=0:
                cnt += 1
                col = c

        if not exist:
            if cnt == 1:
                setValue( r, col, n )
                changed = True
            elif cnt == 0:
                raise Exception
            
    return changed

def checkVline( c ):    
    changed = False
    for n in range(1,SIZE+1):
        exist = False
        cnt = 0
        row = 0
        for r in range(SIZE):
            if board[r][c] == n:
                exist = True
            if candidate[r][c][n]!=0:
                cnt += 1
                row = r

        if not exist:
            if cnt == 1:
                setValue( row, c, n )
                changed = True
            elif cnt == 0:
                raise Exception

    return changed

def checkCell(c,r):    
    if board[r][c] != 0:
        return False

    cnt = 0
    v = 0
    for n in range(1,SIZE+1):
        if candidate[r][c][n]!=0:
            cnt += 1
            v = n

    if cnt == 1:
        setValue( r, c, v )
    elif cnt == 0:
        raise Exception

    return cnt==1

## --------------------	blank count	--------------------

def blankCount():
    cnt = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                cnt += 1

    return cnt

