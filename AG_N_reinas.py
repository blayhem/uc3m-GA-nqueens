#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as r
import sys
import math
import functools as ft

class Queens:

    def __init__(self, N, iter, pSize):
 
        self.N = N;
        self.iter = i;

        self.fitnesses = {};   # cache de evaluaciones
        self.evaluaciones = 0; # num de evaluaciones
        self.ciclos = 0;
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
        poblacion = self.poblacion;
        while ( self.ciclos < self.iter): # and not self.criterioDeParada ):
        # for i in range(0, self.iter):
            try:
                '''
                0. Calculamos fitness de la poblacion para revisar el criterio
                de parada
                '''
                for individuo in poblacion:
                    self.check_exit(individuo)

                if(self.criterioDeParada):
                    break;

                '''
                1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
                '''
                padres = self.seleccion(poblacion);
                # 2 torneos mejor que 1 torneo doble?
                padres += padres;
                # for p in padres:
                #     poblacion.pop(poblacion.index(p))

                '''
                2. Hacemos cruce con reemplazo, los padres vuelven a la poblacion
                porque K=4 pero L=2 (perdemos 2 individuos).
                self.cruce nos devuelve 4 individuos, 2 padres y 2 hijos.
                '''
                    # nuevaPoblacion = self.cruzar(padres);
                # print('despues de cruce: \t', nuevaPoblacion)

                '''
                3. Mutamos la nueva poblacion.
                Politica opcional: if son has clone in poblacion, do not add.
                '''
                # nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
                nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), padres));
                # print('con mutacion: \t', nuevaPoblacion)
                poblacion += nuevaPoblacion;
                self.ciclos += 1;

            except KeyboardInterrupt:
                print('okay')
                break

        if(len(self.solutions) == 0):
            print('No solution found. ', self.evaluaciones, 'evaluaciones')

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
                    elif(r_x==ind_x or r_y==ind_y or r_x-r_y == ind_x-ind_y or r_x+r_y == ind_x+ind_y):
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
        K = 4;
        L = 2;
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

    def cruzar(self, poblacion):
        pc = 0.2; # crossover probability
        # para cada bit: coger 1 u otro del padre, o random (0,N)

        for i in range(0, 2):
            if(r.uniform(0,1) < pc):
                corte = math.floor(r.uniform(0, self.N));
                new = poblacion[0][0:corte] + poblacion[1][corte:self.N];
                poblacion.append(new)
            else:
                poblacion.append(poblacion[i]);

        return poblacion;

    def mutacion(self, individuo):
        p = 0.5*(1/self.N); # probabilidad de mutar
        size = len(individuo)

        for i in range(0, size):
            if(r.uniform(0, 1) < p):
                j = r.randrange(0, size);
                prev = individuo[i]
                individuo[i] = individuo[j]
                individuo[j] = prev;

        return individuo;

    def print_line(self, n):
        print('|',end='')
        for i in range(0,n):
            print('---|', end='')
        print('')

    def print_board(self, board):
        n = len(board)
        self.print_line(n)
        for i in range(0,n):
            print('|',end='')
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
            print('\n SOLUTION FOUND: ', individuo, '\n')
            print(self.evaluaciones, ' evaluaciones')
            print(self.ciclos, 'ciclos')
            board = [(y, x) for (y, x) in enumerate(individuo)]
            self.print_board(board);

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

'''

N = int(sys.argv[1])
i = int(sys.argv[2])
P = int(sys.argv[3])
K = int(sys.argv[4])
L = int(sys.argv[5])

u = int(sys.argv[6])
pm = int(sys.argv[7])
pc = int(sys.argv[8])

queens = Queens(N, i, P)
queens.main()

# except:
    # print('Wrong number of arguments')
    # print('Try -h to view full list of arguments')


