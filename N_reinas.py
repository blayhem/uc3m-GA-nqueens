import random as r


'''
def init2(N):
    size = N*N
    matrix = []
    for n in range(0, size):
        # Inicializamos la matriz con posiciones aleatorias
        matrix.append(r.randint(0, 1))
    return matrix

tablero = init2(3)
'''

def validate(reinas, x, y):
    for r in reinas:
        if(r[0]==x or r[1]==y or r[0]-r[1] == x-y or r[1]+r[0] == y+x):
            return False;
    for n in notavailable:
        if(n[0]==x and n[1]==y):
            return False;
    return True

def position(reinas):
    x, y = (0, 0)
    while(not validate(reinas, x, y)):
        if(y >= size-1):
            return ("Error", "Error")
        if(x >= size-1):
            y+=1
            x = 0
        else:
            x+=1
    return (x, y)


def populate(reinas):
    if(len(reinas) == 0):
        reinas.append([0 ,0])
    else:
        x, y = position(reinas)
        while x=='Error':
            notavailable.append(reinas.pop());
            x, y = position(reinas)
        reinas.append([x, y])

def init(N):
    # N reinas, coord
    reinas = []
    while len(reinas)!=N:
        print(reinas);
        populate(reinas)
    return reinas;

size      = 3
notavailable = []
positions = init(size)

print(positions)


