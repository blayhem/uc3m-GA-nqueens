#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as r
import sys
import math
import functools as ft

class Queens:

    def __init__(self, N):
        '''
        Posibles paramametros:
        N: numero de reinas, dimension del tablero
        K: tamaño de muestra de selección
        L: número de ganadores del torneo (padres)
        '''
        self.N = N;
        self.fitnesses = [];
        self.solutions = [];
        self.evaluaciones = 0;
        self.criterioDeParada = False;

        poblacion = [];
        orderedList = [i for i in range(0,N)]
        for p in range(0, 200):
            r.shuffle(orderedList)
            poblacion.append(orderedList);

        self.poblacion = poblacion;

    def main(self):
        poblacion = self.poblacion;
        while ( not self.criterioDeParada ):
        # for i in range(0, 200):
            '''
            0. Calculamos fitness de la poblacion para revisar el criterio
            de parada
            '''
            for individuo in poblacion:
                self.check_exit(individuo)


            '''
            1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
            '''
            # print('\npoblacion inicial:', len(poblacion))
            padres = self.seleccion(poblacion);
            # 2 torneos mejor que 1 torneo doble?
            padres += padres;
            # print('padres:', padres)
            # map(lambda p: poblacion.pop(poblacion.index(p)), padres);
            # for p in padres:
            #     poblacion.pop(poblacion.index(p))
            # print('poblacion sin padres: ', len(poblacion))

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
            # print('con mutacion: \t\t', nuevaPoblacion)
            poblacion += nuevaPoblacion;
            # criteriodeparada = True;
            break;

    def getFitness(self, individuo):
        try:
            i = self.fitnesses.index(individuo);
            return self.fitnesses[i];
        except:
            self.evaluaciones += 1;
            bad = 0;
            for (ind_y, ind_x) in enumerate(individuo): # posiciones de reinas
                for (r_y, r_x) in enumerate(individuo): # resto de reinas
                    if(r_x == ind_x):
                        continue; # mismo individuo
                    elif(r_x==ind_x or r_y==ind_y or r_x-r_y == ind_x-ind_y or r_x+r_y == ind_x+ind_y):
                        bad += 1;

        # return (n/N - bad/n)
        # print("adjacent queens: ", bad)
        if(bad == 0):
            fitness = 1;
        else:
            fitness = (1 - bad/self.N)
        self.fitnesses.append(fitness)
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
        p = 1; # probabilidad de mutar
        # p dependiente de N
        # for i in range(0, len(individuo)):
        if(r.uniform(0, 1) < p):
            # mejor: swap de 2 valores
            r.shuffle(individuo)
                # individuo[i] = r.randrange(0,self.N);

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
        if(fitness >= 1-umbral ): #and individuo not in self.solutions):
            # self.solutions.append(individuo);
            print('\n SOLUTION FOUND: ', individuo, '\n')
            print(self.evaluaciones, ' evaluaciones')
            board = [(y, x) for (y, x) in enumerate(individuo)]
            self.print_board(board);

            exit()
            # self.criterioDeParada = True;

queens = Queens(int(sys.argv[1]))
queens.main()
