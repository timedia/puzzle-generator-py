##	NP(Number Place) Generator Module
##
##	This class has the main method.
##
##(c) 2019-2021  FUJIWARA Hirofumi, Knowledge Engineering Center, Time Intermedia, Inc.
## This code is licensed under MIT license (see LICENSE.txt for details)
##

import  parameter
import  numpy as np
import  sys
import  random
from solution import getANewSolution
import NP
import solver

SIZE = parameter.SIZE
SUBSIZE = parameter.SUBSIZE

XCOUNT = 2

pattern     = None  # boolean[][],  hint pattern, given from caller
hintcount   = 0
hintarray   = None  # int[][]
xcells      = None  # int[][]
problem     = None  # int[][]
blankcount  = 0     # current blank cell count

def generate( pat ):
    for i in range(400):
        print('*', end='', file=sys.stderr, flush=True)
        if generateOnce( pat ):
            sys.stderr.write( "SUCCESS  TRY {}\n".format(i))
            return True
    return False
            
def generateOnce( pat ):
    global pattern, xcells, blankcount, problem
    global hintarray
    
    pattern = pat
    xcells = np.zeros((XCOUNT,2)).astype(int)
    initialSetting()

    i = 0
    while i < 200:
        if blankcount == 0:                 # SUCCESS!!
            break

        backup = problem.copy()

        ## select XCOUNT cells and changed them
        selectXCells()
        clearXCells()

        ## change some cells value on problem
        blk = changeXCells()
			
	## if new problem is better, update current blankcount, and continue
	## else restore problem
        if blk >= 0 and blk < blankcount:
            blankcount = blk	    ## update blankcount
            i = 0
        else:			    ## restore from backup
            problem = backup
        i += 1
					
    return blankcount==0;

def initialSetting():
    global pattern, solution, problem, blankcount, hintcount, hintarray
    
    solution = getANewSolution()
		
    problem = makeInitialProblem( pattern, solution )

    blankcount = solver.solve(problem)

    hintcount = countTrue(pattern)	
    hintarray = getHintArray()


def countTrue( pt ):
    cnt = 0;
    for r in range(SIZE):
        for c in range(SIZE):
            if pt[r][c] != 0:
                cnt += 1
    return cnt

def getHintArray():
    global hintpos, pattern, hintcount
    hintpos = np.zeros((hintcount,2)).astype(int)

    idx = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if pattern[r][c] != 0:
                hintpos[idx][0] = r
                hintpos[idx][1] = c
                idx += 1
    return hintpos

def selectXCells():
    global xcells, hintarray,hintcount
    cnt = 0
    while cnt < XCOUNT:
        offr = random.randrange(hintcount)
        p = hintarray[offr]
        match = False
        for i in range(cnt):
            if xcells[i][0]==p[0] and xcells[i][1]==p[1]:
                match = True
        if not match:
            xcells[cnt][0] = p[0]
            xcells[cnt][1] = p[1]
            cnt += 1

def clearXCells():
    global problem, xcells
    for i in range(XCOUNT):
        problem[xcells[i][0]][xcells[i][1]] = 0

def changeXCells():
    global problem, xcells
    
    blk = solver.solve(problem)

    for i in range(XCOUNT):
        r = xcells[i][0]
        c = xcells[i][1]
        val = solver.getValue(r,c)
        if val > 0:
            problem[r][c] = val
            continue

        cans = solver.getCandidate(r,c)
        val = selectCandidate(cans)
        if val < 0:
            return  -1
        problem[r][c] = val

        blk = solver.solve(problem)
        if blk < 0:
            return -1
		
    return blk

def selectCandidate( cans ):
    r = random.randrange(SIZE)
    for  i in range(SIZE):
        v = ((r+i) % SIZE) + 1
        if cans[v] != 0:
            return v
    return -1

def makeInitialProblem( pattern, solution ):    
    prob =  np.zeros((SIZE,SIZE)).astype(int)
    for r in range(SIZE):
        for c in range(SIZE):
            if pattern[r][c] != 0:
                prob[r][c] = solution[r][c]
    return prob
	
def getProblem():
    global problem
    return problem

