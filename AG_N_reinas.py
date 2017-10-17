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

    def __init__(self, N, iter, pSize, K, L, pm, pc):

        if(N<4):
            print('''
                El problema no tiene solución para n=2 o n=3.
                > E. J. Hoffman et al., "Construction for the Solutions of the m Queens Problem". Mathematics Magazine, Vol. XX (1969), pp. 66–72.
                http://penguin.ewu.edu/~trolfe/QueenLasVegas/Hoffman.pdf
                ''')
            exit()

        elif(K>pSize):
            print('El tamaño de muestra de torneo (', K,')tiene que ser menor que el tamaño de población (', pSize, ')')
            exit()

        '''
        Parámetros básicos
        '''
        self.N = N;
        self.iter = i;
        
        self.K = K;
        self.L = L;
        self.pm = pm;
        self.pc = pc;

        # GRAPHICS - valores de fitness para el mejor individuo
        self.fvalues = [];

        '''
        Parámetros internos
        '''
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
        # print(min(list(map(lambda i: self.getFitness(i), poblacion))))

    def main(self):
        bar = progressbar.ProgressBar(redirect_stdout=False)
        poblacion = self.poblacion;
        # backup = []
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
                # nuevaPoblacion = self.cruce_SCX(padres);
                nuevaPoblacion = self.cruce_OC1(padres);
                # REEMPLAZO:
                # poblacion = poblacion[self.L:]
                poblacion = poblacion[self.L*2:]
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
                # print('Best individual fitness: ', bestValue, 'worst individual fitness: ', min(self.fitnesses.values()), 'diversityIndex: ', int(self.diversityIndex))
                if(bestValue == self.bestValue):
                    self.diversityIndex += 0.01
                    if(self.diversityIndex>10):
                        # poblacion = backup[:]
                        self.diversityIndex = 1;
                    # else:
                        # backup = poblacion[:]
                    # TODO: pseudo-backtracking

                else:
                    self.diversityIndex = 1;
                    self.bestValue = bestValue;
                
                self.fvalues.append(bestValue)
                
                if(self.criterioDeParada):
                    break;

                if(bestValue==1):
                    for individuo in poblacion:
                        self.check_exit(individuo)
                    # print('\nsolution found!', self.criterioDeParada)

            except KeyboardInterrupt:
                print('RTL+C. Parando.')
                break

        if(len(self.solutions) == 0):
            print('\nNo solution found. ', self.evaluaciones, 'evaluaciones', 'máximo fitness: ', self.bestValue, 'en ', self.ciclos, 'iteraciones')
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
            for (ind_y, ind_x) in enumerate(individuo): # posiciones de reinas
                # for (r_y, r_x) in enumerate(individuo): # resto de reinas
                for(r_y) in range(ind_y+1, len(individuo)):
                    r_x = individuo[r_y]
                    if(r_y == ind_y):
                        continue; # mismo individuo
                    elif(r_x==ind_x
                      or r_y==ind_y
                      or r_x-r_y == ind_x-ind_y
                      or r_x+r_y == ind_x+ind_y):
                        bad  += 1;
                        
                index = evaluable.index(ind_x)
                evaluable.pop(index); # quitamos 1 reina adyacente para tener solo 1 arista

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
            while(sel in taken):
                sel = r.randrange(0,len(poblacion));
            muestra.append(poblacion[sel]);
            taken.append(sel);

        # muestra de tamaño K, ordenada de mayor a menor fitness
        muestra.sort(key=self.getFitness, reverse=True)

        if(r.uniform(0, 1) < luck):
            return muestra[0]
        else:
            return muestra[1]

    def cruce_SCX_random(self, padres):
        hijos = []
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
                    sel = r.randrange(0, len(padres));
                    number = padres[sel][j];

                    opt = [i for i in range(0,len(padres))]
                    while(number in offspring):    # si el valor se repite
                        opt.pop(opt.index(sel)) # quitamos el anterior
                        sel = opt[r.randrange(0, len(opt))]
                        number = padres[sel][j] # cogemos el valor del otro padre
                        if(len(opt)==1):
                            number = r.randrange(0, self.N);
                            break;
                    offspring.append(number)

            else:
                offspring = padres[i]
            hijos.append(offspring)
        return hijos[:self.L]
        # return padres;

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
                    hijo.append(p2[bit])
                else:
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
        # return familia[:len(offspring)]
        return offspring

    def cruce_OC1(self, padres):
        offspring = []

        for i in range(0, int(len(padres)/2)):
            # para cada par de padres:
            p1 = padres[i*2]
            p2 = padres[(i*2)+1]
            size = len(p1)
            if(size != len(p2) or size != N):
                raise ValueError('La longitud de los padres difiere.')

            cut1 = r.randrange(0,size/2)
            cut2 = r.randrange(0,size/2)

            cSection = p1[cut1:cut1+int(size/2)]
            other    = list(filter(lambda n: n not in cSection, p2))
            hijo1 = other[:cut1] + cSection + other[cut1:]
            offspring.append(hijo1)

            cSection = p2[cut2:cut2+int(size/2)]
            other    = list(filter(lambda n: n not in cSection, p1))
            hijo2 = other[:cut2] + cSection + other[cut2:]
            offspring.append(hijo2)

        return offspring


    def mutacion(self, individuo):
        p = self.diversityIndex*self.pm #*self.N;     # probabilidad de mutación
        size = len(individuo)

        if(r.uniform(0, 1) < p):
            for i in range(0, size):
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
        fitness = self.getFitness(individuo);
        if(fitness == 1 and individuo not in self.solutions):
            self.solutions.append(individuo);

            # STATS
            print('''
                PARA N = {}
                SOLUTION FOUND: {}
                {} evaluaciones,
                {} ciclos
                '''.format(self.N, individuo, self.evaluaciones, self.ciclos))

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

python3 AG_N_reinas.py 8 20000 100 20 10 0.1 0.9
'''

N = int(sys.argv[1])
i = int(sys.argv[2])
P = int(sys.argv[3])
K = int(sys.argv[4])
L = int(sys.argv[5])

pm = float(sys.argv[6])
pc = float(sys.argv[7])

queens = Queens(N, i, P, K, L, pm, pc)
queens.main()

# except:
    # print('Wrong number of arguments')
    # print('Try -h to view full list of arguments')


