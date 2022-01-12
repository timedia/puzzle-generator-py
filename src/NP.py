##	NP(Number Place) Main Module
##
##	This class has the main method.
##
##(c) 2019-2021  FUJIWARA Hirofumi, Knowledge Engineering Center, Time Intermedia, Inc.
## This code is licensed under MIT license (see LICENSE.txt for details)
##

import  solver
import  random
import  sys, time
import  numpy as np
import  parameter
import generator

SIZE = parameter.SIZE
SUBSIZE = parameter.SUBSIZE

class Problem:
    def __init__(self):      # , prob, idstr, blk, ans, pat ):
        self.problem = None
        self.id      = None
        self.blanks  = None
        self.answer  = None
        self.pattern = None

datainput = sys.stdin
dataoutput = None

random.seed()

def readProblemTitle(line):
    return line

def readProblemBody(linebody):
    if len(linebody)<SIZE:
        return None
    bd = np.zeros((SIZE,SIZE)).astype(int)
    for r in range(SIZE):
        line = linebody[r]
        tokens = line.split()
        for c in range(SIZE):
            str = tokens[c]
            val = 0
            if str != '-':
                val = int(str)
            bd[r][c] = val
    return	bd

def readPatternBody(linebody):
    if len(linebody)<SIZE:
        return None
    bd = np.zeros((SIZE,SIZE)).astype(int)      # 0/1
    for r in range(SIZE):
        line = linebody[r]
        tokens = line.split()
        for c in range(SIZE):
            if tokens[c] == '-':
                bd[r][c] = 0
            else:
                bd[r][c] = 1
                
    return	bd;
	
def countHint(bd):
    cnt = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if bd[r][c] != 0:
                cnt += 1
    return cnt


def printBoard( ps, bd ):
    for r in range(SIZE):
        for c in range(SIZE):
            if bd[r][c] == 0:
                ps.write("- ")
            else:
                ps.write("{} ".format(bd[r][c]) )
        ps.write("\n")

def printHintBoard( ps,  bd ):
    for r in range(SIZE):
        for c in range(SIZE):  
            if bd[r][c]!=0:
                ps.write("X ")
            else:
                ps.write("- ")
        ps.write("\n")

def copyBoard( fr, to ):
    for r in range(SIZE):
        for c in range(SIZE):
            to[r][c] = fr[r][c]

# 問題を解く
def solveNP(filename):
    problems = []

    with open(filename) as f:
        lines = [l.rstrip('\n') for l in f.readlines()]

    while len(lines) > SIZE:
        pr = Problem()
        line = lines.pop(0)
        pr.id = readProblemTitle(line)
        linebody = lines[:SIZE]
        lines = lines[SIZE:]

        pr.problem = readProblemBody(linebody)
##        print(pr.problem)
        problems.append(pr)
##        printBoard(sys.stdout,pr.problem)

    # 全問を解くループ
    start_time = time.perf_counter()    

    for pb  in  problems:
        pb.blanks = solver.solve(pb.problem)
        if pb.blanks >= 0:
            pb.answer = solver.getAnswer()

    exe_time = time.perf_counter() - start_time 

    # 全問を解いた結果表示のループ
    success = 0;
    for pb in problems:
        if dataoutput!=None:
            dataoutput.write(pb.id,'\n')
        sys.stderr.write("{}\n".format(pb.id))

        if pb.blanks < 0:
            if dataoutput!=None:
                dataoutput.write("ERROR\n")
            sys.stderr.write("ERROR\n")
        else:
            printBoard(sys.stderr,pb.problem)
            sys.stderr.write('{}\n'.format(pb.blanks))
            printBoard(sys.stderr,pb.answer)
            sys.stderr.write('\n')

        if pb.blanks==0:
            success += 1

    probSize = len(problems)
    sys.stderr.write( "Total {}    Success {}\n".format(probSize,success))
    sys.stderr.write( "Time\t{:06f} sec\n".format(exe_time) )

def generateNP(filename):
    problems = []

    with open(filename) as f:
        lines = [l.rstrip('\n') for l in f.readlines()]

    while len(lines) > 0:
        pr = Problem()
        line = lines.pop(0)
        pr.id = readProblemTitle(line)
        linebody = lines[:SIZE]
        lines = lines[SIZE:]
        if len(linebody) == SIZE:
            pr.pattern = readPatternBody(linebody)
            problems.append(pr)

    # 全問作るループ
    start_time = time.perf_counter()  
    
    failureCount=0
    successCount=0
    n=0

    for pb in problems:
        pattern = pb.pattern
        n += 1
        sys.stderr.write("No.{}   H {}\n".format(n,countHint(pattern)))
        if dataoutput != None:
            dataoutput.write("No.{}   H {}\n".format(n,countHint(pattern)))
        printHintBoard(sys.stderr,pattern)

        if generator.generate(pattern):
            pb.problem = generator.getProblem()
            if dataoutput != None:
                printBoard(dataoutput,pb.problem)
            printBoard(sys.stderr,pb.problem)
            successCount += 1
        else:
            if dataoutput != None:
                dataoutput.write("FAILURE\n")
            sys.stderr.write("FAILURE\n")
            failureCount += 1
        sys.stderr.write('\n')

    exe_time = time.perf_counter() - start_time 


    probSize = len(problems)
    sys.stderr.write( "total {}  failure {}\n".format((successCount+failureCount),failureCount))
    sys.stderr.write( "Time\t{:06f} sec\n".format(exe_time) )


def printErrorMessage():
    print("===== arguments input error =====")
    print("python3  NP.py  -s  problem_file   [answer_file]")
    print("python3  NP.py  -g  pattern_file   [problem_file]")

##  -------------------- main() ------------------------
def main(args):

    if len(args) < 2:
        printErrorMessage()
        return

    try:
        datainput = open(args[2],'r')
        if len(args)>=4:
            dataoutput = open(args[3],'w')
    except:
        print( '*** File open error ***')
        datainput.close()
        dataoutput.close()
        sys.exit()
    
    if args[1] == '-s':
        solveNP(args[2])
    elif args[1] == '-g':
        generateNP(args[2])
    else:
        printErrorMessage()
        sys.exit()

#  -------------------- start from here ------------------------
if __name__ == "__main__":
    args = sys.argv
#    args = ['NP.py', '-g', 'data/20P.txt']
    main(args)

