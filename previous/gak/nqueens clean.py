import sys
import time
from time import sleep
from sys import stdout

def create_board(n):
    '''
    init n queens where each one has an x y position
    '''
    return [(None, None) for i in range(0,n)]

def init_board(board):
    '''
    for a brute force alg, sets the first queen to 0 0
    '''
    return board

def is_legal(board,x,y,n_queens):
    '''
    check if an x y position is legal  
    '''
    #check row , col, diag1 and diag2
    for i in range(0,n_queens):
        if(( board[i][0]==x ) or ( board[i][1]==y ) or ( board[i][0]-board[i][1] == x-y ) or ( board[i][0]+board[i][1] == x+y ) ):
            return False

    return True


# printing methods:

def print_line(n):
        print('|',end='')
        for i in range(0,n):
            print('---|', end='')
        print('')

def print_board(board):
    n = len(board)
    print_line(n)
    for i in range(0,n):
        print('|',end='')
        for j in range(0,n):
            if(board[i]==[i,j]):
                print(' R |',end='')
            else:
                print('   |',end='')
        print('')
        print_line(n)

def delete_print(n):
    for i in range(0,(n*2)+2):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

def dinamic_print(board):
    sleep(0.02)
    delete_print(len(board))
    print_board(board)


def fast_ds_all_solutions(n):
    print('Trying to solve with n = ' + str(n))
    board = create_board(n)
    x = 0
    y = 0
    n_queens=0
    solutions=0

    while(True):
        if(is_legal(board,x,y,n_queens)):
            board[n_queens]=[x,y]
            n_queens = n_queens+1
            y = 0
            x += 1
            if(n_queens == n):
                solutions += 1
            
        elif(y == n-1):
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y = y + 1
            board[n_queens-1] = [None,None]
            n_queens = n_queens-1
            if(y >= n): 
                y = board[n_queens-1][1]
                x = board[n_queens-1][0]
                if(y == None):
                    break #end
                y = y + 1
                board[n_queens-1]=[None,None]
                n_queens = n_queens-1
        else:
            y = y + 1
    if(solutions!=0):
        print('All solutions found!: ' + str(solutions))
    else:
        print('There is no solution jackass')

def fast_ds_one_solution(n):
    # print('Trying to find n = ' + str(n))
    # INIT:
    board = create_board(n)
    x = 0
    y = 0
    n_queens=0

    #MAIN:
    while( x < n ):

        if(is_legal(board,x,y,n_queens)):
            board[n_queens] = (x,y)
            n_queens += 1
            y = 0
            x += 1

        elif(y == n-1): # backtracking
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y += 1
            board[n_queens-1] = (None,None)
            n_queens -= 1

            if(y >= n): #doble backtracking
    
                y = board[n_queens-1][1]
                x = board[n_queens-1][0]
                if(y == None):                
                    break
                
                y += 1
                board[n_queens-1] = [None,None]
                n_queens = n_queens-1

        else:
            y += 1

    if(n_queens==n):
        print('Solution found!')
    else:
        print('There is no solution jackass')
    print_board(board)
   
# n_queens_vs_ds_all_solutions(int(sys.argv[1]))
# n_queens_vs_ds_one_solution(int(sys.argv[1]))
fast_ds_all_solutions(int(sys.argv[1]))
# fast_ds_one_solution(int(sys.argv[1]))
