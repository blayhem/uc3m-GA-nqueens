import sys
import time
from time import sleep
from sys import stdout

def create_board(n):
    '''
    init n queens where each one has an x y position
    '''
    board = []
    for i in range(0,n):
        board.append([None,None])
    return board

def init_board(board):
    '''
    for a brute force alg, sets the first queen to 0 0
    '''
    return board

def is_legal(board,x,y,n_queens):
    '''
    check if an x y position is legal  
    for i in range(1,20):
        string = 'this data \n is intended' + str(i)
        stdout.write("\r%s" % string)
        stdout.flush()
        sleep(1)
    stdout.write("\r  \r\n") # clean up 
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


# end printing methods

def n_queens_vs_ds_one_solution(n):
    print('Trying to solve with n = ' + str(n))
    print('This solution dinamily print the search, as is it a simple example of the search, its really slow')
    print('This print wont work if the board doesnt fit in the terminal screen')
    board = init_board(create_board(n))
    # init variables
    # print(str(is_legal(board,2,0)))
    x = 0
    y = 0
    n_queens=0
    print_board(board)
    start = time.time()
    while( x < n ):

        if(is_legal(board,x,y,n_queens)):
            print('New queen into [' + str(x)+','+str(y)+']')
            board[n_queens]=[x,y]
            n_queens = n_queens+1
            y = 0
            x = x + 1
            dinamic_print(board)

        elif(y == n-1): # backtracking
            print('Backtracking!')
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y = y + 1
            board[n_queens-1]=[None,None]
            n_queens = n_queens-1
            dinamic_print(board)
            if(y >= n): #doble backtracking
                print('Backtracking!')
                y = board[n_queens-1][1]
                x = board[n_queens-1][0]
                if(y == None):
                    
                    break
                
                y = y + 1
                board[n_queens-1]=[None,None]
                n_queens = n_queens-1
                dinamic_print(board)

        else:
            y = y + 1
    end = time.time()
    
    if(n_queens==n):
        print('Solution found!')
    else:
        print('There is no solution jackass')
    print(end - start)

def n_queens_vs_ds_all_solutions(n):
    print('Trying to solve with n = ' + str(n))
    print('This solution dinamily print the search so its slow')
    print('This print wont work if the board doesnt fit in the terminal screen')
    board = init_board(create_board(n))
    x = 0
    y = 0
    n_queens=0
    solutions=0
    print_board(board)
    start = time.time()
    while(True):

        if(is_legal(board,x,y,n_queens)):
            print('New queen into [' + str(x)+','+str(y)+']')
            board[n_queens]=[x,y]
            n_queens = n_queens+1
            y = 0
            x = x + 1
            dinamic_print(board)
            if(n_queens == n):

                print('Solution found!')
                dinamic_print(board)
                solutions=solutions+1
            

        elif(y == n-1): # backtracking
            print('Backtracking!')
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y = y + 1
            board[n_queens-1]=[None,None]
            n_queens = n_queens-1
            dinamic_print(board)
            if(y >= n): #doble backtracking
                print('Backtracking!')
                y = board[n_queens-1][1]
                x = board[n_queens-1][0]
                if(y == None):
                    
                    break #end
                
                y = y + 1
                board[n_queens-1]=[None,None]
                n_queens = n_queens-1
                dinamic_print(board)

        else:
            y = y + 1
        
    end = time.time()

    if(solutions!=0):
        print('All solutions found!: ' + str(solutions))
    else:
        print('There is no solution jackass')
    print(end - start)

def fast_ds_all_solutions(n):
    print('Trying to solve with n = ' + str(n))
    board = init_board(create_board(n))
    x = 0
    y = 0
    n_queens=0
    solutions=0
    start = time.time()

    while(True):
        if(is_legal(board,x,y,n_queens)):
            board[n_queens]=[x,y]
            n_queens = n_queens+1
            y = 0
            x = x + 1
            if(n_queens == n):
                solutions=solutions+1
            
        elif(y == n-1):
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y = y + 1
            board[n_queens-1]=[None,None]
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
    end = time.time()
    if(solutions!=0):
        print('All solutions found!: ' + str(solutions))
    else:
        print('There is no solution jackass')
    print(end - start)

def fast_ds_one_solution(n):
    print('Trying to find n = ' + str(n))
    board = init_board(create_board(n))
    x = 0
    y = 0
    n_queens=0
    start = time.time()
    while( x < n ):

        if(is_legal(board,x,y,n_queens)):
            board[n_queens]=[x,y]
            n_queens = n_queens+1
            y = 0
            x = x + 1

        elif(y == n-1): # backtracking
            y = board[n_queens-1][1]
            x = board[n_queens-1][0]
            y = y + 1
            board[n_queens-1]=[None,None]
            n_queens = n_queens-1

            if(y >= n): #doble backtracking
    
                y = board[n_queens-1][1]
                x = board[n_queens-1][0]
                if(y == None):                
                    break
                
                y = y + 1
                board[n_queens-1]=[None,None]
                n_queens = n_queens-1

        else:
            y = y + 1

    end = time.time()
    
    if(n_queens==n):
        print('Solution found!')
    else:
        print('There is no solution jackass')
    print_board(board)
    print(end - start)
   
# n_queens_vs_ds_all_solutions(int(sys.argv[1]))
n_queens_vs_ds_one_solution(int(sys.argv[1]))
# fast_ds_all_solutions(int(sys.argv[1]))
# fast_ds_one_solution(int(sys.argv[1]))