#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as r
import sys
import math
import functools as ft
# https://pypi.python.org/pypi/progressbar2
import progressbar
import matplotlib.pyplot as plt


class Queens:

    def __init__(self, N, iter, pSize, K, L, u, pm, pc):

        if(N<4):
            print('''
                El problema no tiene solución para n=2 o n=3.
                > E. J. Hoffman et al., "Construction for the Solutions of the m Queens Problem". Mathematics Magazine, Vol. XX (1969), pp. 66–72.
                http://penguin.ewu.edu/~trolfe/QueenLasVegas/Hoffman.pdf
                ''')
            exit()
        '''
        Parámetros básicos
        '''
        self.N = N;
        self.iter = i;
        if(K>N):
            print('El tamaño de muestra de torneo tiene que ser menor que la población')
            raise ValueError
        self.K = K;
        self.L = L;
        self.umbral = u;
        self.pm = pm;
        self.pc = pc;3

        # GRAPHICS - valores de fitness para el mejor individuo
        self.fvalues = [];

        self.fitnesses = {};   # cache de evaluaciones
        self.evaluaciones = 0; # num de evaluaciones
        self.ciclos = 0;       # num de ciclos de evaluación
        self.criterioDeParada = False;
        self.solutions = [];

        # diversity index
        self.bestValue = 9999;
        self.diversityIndex = 1

        '''
        Inicialización de la población:
        '''
        poblacion = [];
        orderedList = [i for i in range(0,N)]
        for p in range(0, pSize):
            r.shuffle(orderedList)
            poblacion.append(orderedList[:]);

        self.poblacion = poblacion;

    def main(self):
        bar = progressbar.ProgressBar(redirect_stdout=False)
        poblacion = self.poblacion;
        backup = []
        while ( self.ciclos < self.iter):
            try:
                bar.update((self.ciclos*100)/self.iter)

                '''
                1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
                Padres siempre es un número par, de tamaño L*2, donde L es el número de hijos.
                '''
                padres = [self.seleccion(poblacion, i%2==0) for i in range(0,2*self.L)]
                '''
                2. Hacemos cruce con reemplazo, los padres vuelven a la poblacion
                porque K=4 pero L=2 (perdemos 2 individuos).
                self.cruce nos devuelve 4 individuos, 2 padres y 2 hijos.
                '''
                # nuevaPoblacion = self.cruzar(padres);
                nuevaPoblacion = self.cruce_SCX(padres);
                '''
                3. Mutamos la nueva poblacion.
                Politica opcional: if son has clone in poblacion, do not add.
                '''
                nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
                # nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), padres));
                poblacion += nuevaPoblacion;
                self.ciclos += 1;
                '''
                4. Calculamos fitness de la poblacion para revisar el criterio
                de parada
                '''
                for individuo in poblacion:
                    self.check_exit(individuo)

                # GRAPHICS - mejor fitness de toda la población
                bestValue = max(self.fitnesses.values())
                if(bestValue==1):
                    print('\nsolution found!', self.criterioDeParada)
                    break;
                if(bestValue == self.bestValue):
                    self.diversityIndex += 0.01
                    # print(self.diversityIndex, bestValue)
                    if(self.diversityIndex>50):
                        poblacion = backup[:]
                    else:
                        backup = poblacion[:]
                        
                else:
                    print(self.diversityIndex, bestValue)
                    self.diversityIndex = 1;
                    self.bestValue = bestValue;
                
                self.fvalues.append(bestValue)
                
                if(self.criterioDeParada):
                    break;

            except KeyboardInterrupt:
                print('RTL+C. Parando.')
                break

        if(len(self.solutions) == 0):
            print('\nNo solution found. ', self.evaluaciones, 'evaluaciones')
        else:
            print(len(self.solutions), 'soluciones encontradas')

        plt.plot(self.fvalues)
        title = 'N={}, K={}, L={}, p. de mutación={}, p. de cruce={}'.format(self.N, self.K, self.L, self.pm, self.pc)
        plt.title(title)
        plt.ylabel('fitness')
        plt.xlabel('iteraciones')
        plt.show()

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

    def seleccion(self, poblacion, reemplazo):
        K = self.K;
        L = self.L;
        return self.torneo2(poblacion, K, reemplazo);

    def torneo(self, poblacion, K, L):
        muestra = []
        # taken = []
        reverse = False;
        '''
        Construimos la muestra K a partir de poblacion
        '''
        for i in range(0,K):
            sel = r.randrange(0,len(poblacion))
            # while(sel in taken):
            #     sel = r.randrange(0,len(poblacion));
            muestra.append(poblacion.pop(sel));
            # taken.append(sel);

        muestra.sort(key=self.getFitness, reverse=reverse)
        return muestra[0:L]

    def torneo2(self, poblacion, K, reemplazo):
        muestra = []
        taken = []
        luck = 0.75;

        for i in range(0,K):
            sel = r.randrange(0,len(poblacion))
            # print(sel, poblacion[sel])
            while(sel in taken):
                sel = r.randrange(0,len(poblacion));
            muestra.append(poblacion[sel]);
            taken.append(sel);

        # muestra de tamaño K, ordenada de mayor a menor fitness
        muestra.sort(key=self.getFitness, reverse=True)
        # quitamos el peor individuo de K que reemplazaremos con el hijo de los 2 padres
        if(reemplazo):
            poblacion.pop(poblacion.index(muestra.pop()))

        if(r.uniform(0, 1) < luck):
            return muestra[0]
        else:
            return muestra[1]

    def cruzar(self, padres):
        print(padres)
        pc = self.pc; # crossover probability
        # para cada bit: coger 1 u otro del padre, o random (0,N)
        size = len(padres[0]);
        if(size != len(padres[1])):
            raise ValueError('La longitud de los padres difiere.')

        for i in range(0, len(padres)):
            if(r.uniform(0,1) < pc):
                offspring = [];

                for j in range(0, size):
                    # adaptar para más de 2 padres
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
        print(padres)
        print(list(map(lambda i: self.getFitness(i), padres)))
        return padres;

    def cruce_SCX(self, padres):
        offspring = []

        for i in range(0, int(len(padres)/2)):
            # para cada par de padres:
            p1 = padres[i*2]
            p2 = padres[(i*2)+1]
            hijo = []

            if(len(p1) != len(p2) or len(p1) != N):
                raise ValueError('La longitud de los padres difiere.')

            for bit in range(0,self.N):
                if(bit==0):
                    # inicializamos el primer locus del hijo
                    hijo.append(p2[bit])
                else:
                    # (x, y) = (hijo[bit-1], bit-1) # coordenadas de la reina anterior
                    try:
                        # opt1_x es el valor siguiente al valor actual del hijo, en el padre1
                        (opt1_x, opt1_y) = (p1[p1.index(hijo[bit-1])+1], bit)
                    except IndexError as e:
                        (opt1_x, opt1_y) = (bit, bit)

                    try:
                        # opt2_x es el valor siguiente al valor actual del hijo, en el padre2
                        (opt2_x, opt2_y) = (p2[p2.index(hijo[bit-1])+1], bit)
                    except IndexError as e:
                        (opt2_x, opt2_y) = (bit, bit)

                    (opt3_x, opt3_y) = (bit, bit)
                    (eval1, eval2, eval3) = (0, 0, 0)

                    # son incidentes las reinas propuestas por el padre 1, el padre 2, y la lista ordenada?
                    for (y, x) in enumerate(hijo):
                        if(opt1_x==x or opt1_y==y or opt1_x-opt1_y == x-y or opt1_x+opt1_y == x+y):
                            eval1 += 1;

                        if(opt2_x==x or opt2_y==y or opt2_x-opt2_y == x-y or opt2_x+opt2_y == x+y):
                            eval2 += 1;

                        if(opt3_x==x or opt3_y==y or opt3_x-opt3_y == x-y or opt3_x+opt3_y == x+y):
                            eval3 += 1;

                    bestEval = ['eval1', 'eval2', 'eval3'][[eval1, eval2, eval3].index(min([eval1, eval2, eval3]))]
                    if(bestEval=='eval1' and opt1_x not in hijo):
                        hijo.append(opt1_x)
                    elif(bestEval=='eval2' and opt2_x not in hijo):
                        hijo.append(opt2_x)
                    elif(bestEval=='eval3' and opt3_x not in hijo):
                        hijo.append(opt3_x)
                    else:
                        n = r.randrange(0,self.N)
                        while(n in hijo):
                            n = r.randrange(0,self.N)
                        hijo.append(n)

            offspring.append(hijo)

        # añadimos primero los hijos para que a igual fitness devuelva hijos, no padres
        familia = offspring+padres;
        familia.sort(key=self.getFitness, reverse=True)

        # devolvemos los hijos excepto cuando su valor es peor que el de los padres
        return familia[:len(offspring)]
        # return offspring


    def mutacion(self, individuo):
        p = self.diversityIndex*self.pm*self.N;     # probabilidad de mutación
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
        if(fitness == 1):#  and individuo not in self.solutions):
            self.solutions.append(individuo);

            # STATS
            print('''
                SOLUTION FOUND: {}
                {} evaluaciones,
                {} ciclos
                '''.format(individuo, self.evaluaciones, self.ciclos))

            # BOARD
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

python3 AG_N_reinas.py 8 10000 100 4 2 0.001 0.2 0.5
'''

N = int(sys.argv[1])
i = int(sys.argv[2])
P = int(sys.argv[3])
K = int(sys.argv[4])
L = int(sys.argv[5])

u  = float(sys.argv[6])
pm = float(sys.argv[7])
pc = float(sys.argv[8])

queens = Queens(N, i, P, K, L, u, pm, pc)
queens.main()

# except:
    # print('Wrong number of arguments')
    # print('Try -h to view full list of arguments')


