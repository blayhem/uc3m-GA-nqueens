#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as r
import sys
import math
import functools as ft
# https://pypi.python.org/pypi/progressbar2
import progressbar

class Queens:

    def __init__(self, N, iter, pSize, K, L):
 
        if(N<4):
            print('''
                El problema no tiene solución para n=2 o n=3.
                > E. J. Hoffman et al., "Construction for the Solutions of the m Queens Problem". Mathematics Magazine, Vol. XX (1969), pp. 66–72.
                http://penguin.ewu.edu/~trolfe/QueenLasVegas/Hoffman.pdf
                ''')
            exit()
        self.N = N;
        self.iter = i;
        self.K = K;
        self.L = L;

        self.fitnesses = {};   # cache de evaluaciones
        self.evaluaciones = 0; # num de evaluaciones
        self.ciclos = 0;       # num de ciclos de evaluación
        self.criterioDeParada = False;

        self.solutions = [];

        '''
        Inicialización de la población:
        '''
        poblacion = [];
        orderedList = [i for i in range(0,N)]
        for p in range(0, pSize):
            r.shuffle(orderedList)
            poblacion.append(orderedList);

        self.poblacion = poblacion;

    def main(self):
        bar = progressbar.ProgressBar(redirect_stdout=False)
        poblacion = self.poblacion;
        while ( self.ciclos < self.iter): # and not self.criterioDeParada ):
        # for i in range(0, self.iter):
            try:
                bar.update((self.ciclos*100)/self.iter)
                '''
                0. Calculamos fitness de la poblacion para revisar el criterio
                de parada
                '''
                for individuo in poblacion:
                    self.check_exit(individuo)

                # if(self.criterioDeParada):
                    # break;

                '''
                1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
                '''
                padres = self.seleccion(poblacion);
                # 2 torneos mejor que 1 torneo doble?
                # padres += padres;

                '''
                2. Hacemos cruce con reemplazo, los padres vuelven a la poblacion
                porque K=4 pero L=2 (perdemos 2 individuos).
                self.cruce nos devuelve 4 individuos, 2 padres y 2 hijos.
                '''
                nuevaPoblacion = self.cruzar(padres);
                # print('despues de cruce: \t', nuevaPoblacion)

                '''
                3. Mutamos la nueva poblacion.
                Politica opcional: if son has clone in poblacion, do not add.
                '''
                nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
                # nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), padres));
                # print('con mutacion: \t', nuevaPoblacion)
                poblacion += nuevaPoblacion;
                self.ciclos += 1;

            except KeyboardInterrupt:
                print('RTL+C. Parando.')
                break

        if(len(self.solutions) == 0):
            print('\nNo solution found. ', self.evaluaciones, 'evaluaciones')
        else:
            print(len(self.solutions), 'soluciones encontradas')

    def getFitness(self, individuo):
        # self.print_board([(y, x) for (y, x) in enumerate(individuo)]);

        key = ''.join(str(n) for n in individuo)
        try:
            fitness = self.fitnesses[key];
            # print('CACHED!')
            return fitness;
        except:
            # print('Calculating fitness...')
            evaluable = individuo[:] # copia por valor
            self.evaluaciones += 1;
            bad = 0;
            for (ind_y, ind_x) in enumerate(evaluable): # posiciones de reinas
                for (r_y, r_x) in enumerate(evaluable): # resto de reinas
                    if(r_x == ind_x):
                        continue; # mismo individuo
                    elif(r_x==ind_x 
                      or r_y==ind_y 
                      or r_x-r_y == ind_x-ind_y 
                      or r_x+r_y == ind_x+ind_y):
                        bad  += 1;
                        index = evaluable.index(ind_x)
                        evaluable.pop(index); # quitamos 1 reina adyacente para tener solo 1 arista
                        break

        # return (n/N - bad/n)
        if(bad == 0):
            fitness = 1;
        else:
            fitness = (1 - bad/self.N)
        self.fitnesses[key] = fitness
        return fitness;

    def seleccion(self, poblacion):
        K = self.K;
        L = self.L;
        return self.torneo(poblacion, K, L);

    def torneo(self, poblacion, K, L):
        muestra = []
        taken = []
        reverse = False;
        '''
        Construimos la muestra K a partir de poblacion
        '''
        for i in range(0,K):
            sel = r.randrange(0,len(poblacion))
            while(sel in taken):
                sel = r.randrange(0,len(poblacion));
            muestra.append(poblacion.pop(sel));
            taken.append(sel);

        muestra.sort(key=self.getFitness, reverse=reverse)
        return muestra[0:L]

    def cruzar(self, padres):
        pc = 0.2; # crossover probability
        # para cada bit: coger 1 u otro del padre, o random (0,N)
        size = len(padres[0]);
        if(size != len(padres[1])):
            raise ValueError('La longitud de los padres difiere.')

        for i in range(0, 2):
            if(r.uniform(0,1) < pc):
                offspring = [];

                for j in range(0, size):
                    sel = r.randrange(0, 2);
                    number = padres[sel][j];

                    if(number in offspring):    # si el valor se repite
                        opt = [0,1]
                        opt.pop(opt.index(sel)) # quitamos el anterior
                        sel = opt[0]            # actualizamos sel con el otro valor
                        number = padres[sel][j] # cogemos el valor del otro padre

                        while(number in offspring): # caso raro: ambos valores repetidos
                            number = r.randrange(0, self.N);
                    offspring.append(number)

            else:
                offspring = padres[i]

            padres.append(offspring)

        return padres;

    def mutacion(self, individuo):
        p = 0.5*(1/self.N);     # probabilidad de mutación
        size = len(individuo)

        for i in range(0, size):
            if(r.uniform(0, 1) < p):
                j = r.randrange(0, size);
                prev = individuo[i]
                individuo[i] = individuo[j]
                individuo[j] = prev;

        return individuo;

    def print_line(self, n):
        print('\t\t|',end='')
        for i in range(0,n):
            print('---|', end='')
        print('')

    def print_board(self, board):
        n = len(board)
        self.print_line(n)
        for i in range(0,n):
            print('\t\t|',end='')
            for j in range(0,n):
                if(board[i]==(i,j)):
                    print(' R |',end='')
                else:
                    print('   |',end='')
            print('')
            self.print_line(n)

    def check_exit(self, individuo):
        umbral = 0.001
        fitness = self.getFitness(individuo);
        if(fitness >= 1-umbral and individuo not in self.solutions):
            self.solutions.append(individuo);

            # STATS
            print('''
                SOLUTION FOUND: {}
                {} evaluaciones,
                {} ciclos
                '''.format(individuo, self.evaluaciones, self.ciclos))

            # BOARD
            # board = [(y, x) for (y, x) in enumerate(individuo)]
            # self.print_board(board);

            self.criterioDeParada = True;


'''

  _ __     __ _ _   _  ___  ___ _ __  ___
 | '_ \   / _` | | | |/ _ \/ _ \ '_ \/ __|
 | | | | | (_| | |_| |  __/  __/ | | \__ \
 |_| |_|  \__, |\__,_|\___|\___|_| |_|___/
             | |
             |_|

'''

# try:

'''
Posibles paramametros:
N: numero de reinas, dimension del tablero
i: iteraciones del AG
P: tamaño de población
K: tamaño de muestra de selección
L: número de ganadores del torneo (padres)

u: umbral de fitness evaluation
pm: probabilidad de mutación
pc: probabilidad de cruce

python3 AG_N_reinas.py 8 10000 100 4 2 1 1 1
'''

N = int(sys.argv[1])
i = int(sys.argv[2])
P = int(sys.argv[3])
K = int(sys.argv[4])
L = int(sys.argv[5])

u = int(sys.argv[6])
pm = int(sys.argv[7])
pc = int(sys.argv[8])

queens = Queens(N, i, P, K, L)
queens.main()

# except:
    # print('Wrong number of arguments')
    # print('Try -h to view full list of arguments')


