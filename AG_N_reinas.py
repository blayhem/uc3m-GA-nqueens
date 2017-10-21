#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as r
import sys
import math
import functools as ft
# https://pypi.python.org/pypi/progressbar2
# import progressbar
# import matplotlib.pyplot as plt
import requests
import multiprocessing
import concurrent.futures

import time
import csv


class Queens_ordered:

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
        # bar = progressbar.ProgressBar(redirect_stdout=False)
        poblacion = self.poblacion;
        # backup = []
        while ( self.ciclos < self.iter):
            try:
                # bar.update((self.ciclos*100)/self.iter)

                '''
                1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
                Padres siempre es un número par, de tamaño L*2, donde L es el número de hijos.
                '''
                t1 = time.time()
                padres = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                    # print(future.result())
                    sel = [executor.submit(self.seleccion, poblacion, i%2==0, True) for i in range(0,2*self.L)]
                    for future in concurrent.futures.as_completed(sel):
                        padres.append(future.result())

                '''
                2. Hacemos cruce con reemplazo L o L*2. Obtenemos L hijos o L*2 (según cruce)
                self.cruce nos devuelve los hijos, L para SCX y L*2 para OC1.
                '''
                # nuevaPoblacion = self.cruce_SCX(padres);
                t2 = time.time()
                # print('Tiempo de selección: ', (t2 - t1)*1000)
                nuevaPoblacion = self.cruce_OC1(padres);
                # REEMPLAZO:
                # poblacion = poblacion[self.L:]
                poblacion = poblacion[self.L*2:]
                '''
                3. Mutamos la nueva poblacion.
                Politica opcional: if son has clone in poblacion, do not add.
                '''
                t3 = time.time()
                # print('Tiempo de cruce y reemplazo: ', (t3 - t2)*1000)
                nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
                # nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), padres));
                poblacion += nuevaPoblacion;
                self.ciclos += 1;
                '''
                4. Calculamos fitness de la poblacion para revisar el criterio
                de parada
                '''
                t4 = time.time()
                # print('Tiempo de mutación: ', (t4 - t3)*1000)
                
                # with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                # with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
                for individuo in poblacion:
                    self.check_exit(individuo)
                        # executor.submit(self.check_exit, individuo)
                        # p.map(self.check_exit, [individuo])

                t5 = time.time()
                # print('Tiempo de evaluación: ', (t5 - t4)*1000)

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


                t6 = time.time()
                # print('Tiempo criterio de parada: ', (t6 - t5)*1000, '\n')
                # if(self.ciclos>8): break;

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
            print(len(self.solutions), 'soluciones encontradas para N=', self.N)
        
        plt.plot(self.fvalues)
        title = 'N={}, K={}, L={}, p. de mutación={}, p. de cruce={}'.format(self.N, self.K, self.L, self.pm, self.pc)
        plt.title(title)
        plt.ylabel('fitness')
        plt.xlabel('iteraciones')
        plt.show()

        return (self.evaluaciones, self.ciclos)

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
                    elif(# r_x==ind_x or
                      # r_y==ind_y or
                      r_x-r_y == ind_x-ind_y or
                      r_x+r_y == ind_x+ind_y):
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

    def seleccion(self, poblacion, reemplazo, reverse):
        K = self.K;
        L = self.L;
        return self.torneo2(poblacion, K, reemplazo, reverse);

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

        muestra.sort(key=self.getFitness, reverse=True)
        return muestra[0:L]

    def torneo2(self, poblacion, K, reemplazo, reverse):
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
        muestra.sort(key=self.getFitness, reverse=reverse)

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
            if(size != len(p2) or size != self.N):
                raise ValueError('La longitud de los padres difiere.')

            cut1 = r.randrange(0,int(size/2))
            cut2 = r.randrange(0,int(size/2))

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

        # swap 1 individuo solo
        # for i in range(0, size):
        if(r.uniform(0, 1) < p):
            i = r.randrange(0, size);
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
        n = self.N
        self.print_line(n)
        for i in range(0,n):
            print('\t\t|',end='')
            for j in range(0,n):
                try:
                    test = list(filter(lambda pos: pos==(i,j), board))[0]
                    print(' R |',end='')
                except:
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

class Queens_binary(Queens_ordered):

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

        # Parámetros básicos
        self.N = N;
        self.iter = i;
        
        self.K = K;
        self.L = L;
        self.pm = pm;
        self.pc = pc;
        
        # Parámetros internos
        self.fitnesses = {};   # cache de evaluaciones
        self.evaluaciones = 0; # num de evaluaciones
        self.ciclos = 0;       # num de ciclos de evaluación
        self.criterioDeParada = False;
        self.solutions = [];

        # diversity index
        self.bestValue = 9999;
        self.diversityIndex = 1

        # INIT
        poblacion = [];
        size = N*N;
        for p in range(0, pSize):
            individuo = [0 for i in range(0,size)]
            for queens in range(0, N):
                individuo[r.randrange(0,size)] = 1
            poblacion.append(individuo);

        self.poblacion = poblacion;

    def main(self):
        # bar = progressbar.ProgressBar(redirect_stdout=False)
        poblacion = self.poblacion;
        # backup = []
        while ( self.ciclos < self.iter):
            try:
                # print(poblacion,'\n')
                # bar.update((self.ciclos*100)/self.iter)
                # selección
                padres = [Queens_ordered.seleccion(self, poblacion, i%2==0, False) for i in range(0,2*self.L)]
                # cruce + reemplazo
                nuevaPoblacion = self.cruce_SP(padres);
                poblacion = poblacion[self.L*2:]
                # mutación
                nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
                poblacion += nuevaPoblacion;
                self.ciclos += 1;

                for individuo in poblacion:
                    self.check_exit(individuo)

                bestValue = min(self.fitnesses.values())
                # print('Best individual fitness: ', bestValue, 'worst individual fitness: ', max(self.fitnesses.values()), 'diversityIndex: ', int(self.diversityIndex))
                if(bestValue == self.bestValue):
                    self.diversityIndex += 0.01
                    if(self.diversityIndex>10):
                        self.diversityIndex = 1;

                else:
                    self.diversityIndex = 1;
                    self.bestValue = bestValue;
                
                if(self.criterioDeParada):
                    break;

                if(bestValue==0.0):
                    # forzamos
                    for individuo in poblacion:
                        self.check_exit(individuo)
                # print(poblacion,'\n')
                # if(self.ciclos > 4): break;

            except KeyboardInterrupt:
                print('RTL+C. Parando.')
                break
        '''
        if(len(self.solutions) == 0):
            print('\nNo solution found. ', self.evaluaciones, 'evaluaciones', 'máximo fitness: ', self.bestValue, 'en ', self.ciclos, 'iteraciones')
        else:
            print(len(self.solutions), 'soluciones encontradas')
        '''
        return (self.evaluaciones, self.ciclos)

    def getFitnessWithURL(self, individuo):
        key = ''.join(str(n) for n in individuo)
        try:
            fitness = self.fitnesses[key];
            return fitness;
        except:
            cadena = ft.reduce(lambda s,c: s+str(c), individuo, '')
            self.evaluaciones += 1;
            try:
                r = requests.get('http://memento.evannai.inf.uc3m.es/age/test?c='+cadena)
                fitness = float(r.text)
                self.fitnesses[key] = fitness
            except:
                fitness = 9999
            return fitness;

    def getFitness(self, individuo):
        key = ''.join(str(n) for n in individuo)
        try:
            fitness = self.fitnesses[key];
            return fitness;
        except:
            # print('Calculating fitness...')
            evaluable = individuo[:]
            self.evaluaciones += 1;
            bad = 0;
            queens = 0;
            for (i, value) in enumerate(individuo): # posiciones de reinas
                if(value==0):
                    continue;
                else:
                    queens += 1;
                    (ind_x) = i%self.N
                    (ind_y) = int(i/self.N)
                for j in range(i+1, len(individuo)):
                    value = individuo[j]
                    if(value==0):
                        continue;
                    else: 
                        (r_x) = j%self.N
                        (r_y) = int(j/self.N)

                    if(r_x==ind_x or
                      r_y==ind_y or
                      r_x-r_y == ind_x-ind_y or
                      r_x+r_y == ind_x+ind_y):
                        bad  += 1;

                # index = evaluable.index(ind_x)
                # evaluable.pop(index); # quitamos 1 reina adyacente para tener solo 1 arista

        # return (n/N - bad/n)
        # if(bad == 0):
            # return bad;
        # else:
            # best = 0
        fitness = (abs(self.N-queens) + bad)
        # print('bad: ', bad)
        self.fitnesses[key] = fitness

        '''
        board = []
        for (i, valor) in enumerate(individuo):
            if(valor==1):
                board.append((int(i/self.N), i%self.N))
        self.print_board(board);
        print(fitness)
        exit()
        '''

        return fitness;

    def cruce_SP(self, padres):
        offspring = []

        for i in range(0, int(len(padres)/2)):
            # para cada par de padres:
            p1 = padres[i*2]
            p2 = padres[(i*2)+1]
            size = len(p1)
            if(size != len(p2) or size != self.N*self.N):
                raise ValueError('La longitud de los padres difiere.')

            cut = r.randrange(0,size)

            hijo1 = p1[:cut] + p2[cut:]
            offspring.append(hijo1)

            hijo2 = p2[:cut] + p1[cut:]
            offspring.append(hijo2)

        return offspring

    def mutacion(self, individuo):
        p = self.diversityIndex*self.pm #*self.N;     # probabilidad de mutación
        size = len(individuo)

        # swap 1 individuo solo
        # for i in range(0, size):
        if(r.uniform(0, 1) < p):
            i = r.randrange(0, size);
            flip = list(filter(lambda n: n!= individuo[i], [0,1]))[0]
            individuo[i] = flip

        return individuo;

    def check_exit(self, individuo):
        fitness = self.getFitness(individuo);
        if(fitness == 0 and individuo not in self.solutions):
            self.solutions.append(individuo);

            # STATS
            '''
            print(
                PARA N = {}
                SOLUTION FOUND: {}
                {} evaluaciones,
                {} ciclos
                .format(self.N, individuo, self.evaluaciones, self.ciclos))

            # BOARD
            board = []
            for (i, valor) in enumerate(individuo):
                if(valor==1):
                    board.append((int(i/self.N), i%self.N))
            # print(board)
            self.print_board(board);
            '''

            self.criterioDeParada = True;

class Queens_bruteforce(Queens_ordered):

    def __init__(self, N):
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

        self.N = N
        self.reinas = 0
        self.coords = [(None, None) for i in range(0,self.N)]

        # Ampliación: todas las soluciones
        self.solutions = 0

    def main(self):
        ciclos = 0
        (x, y) = (0, 0)

        # Ampliación
        criterioDeParada = True;
        # criterioDeParada = (x<self.N);

        while(criterioDeParada):
            ciclos += 1

            if(self.validate(self.coords,x,y,)):
                self.coords[self.reinas] = (x,y)
                self.reinas += 1
                x, y = x+1, 0

                if(self.reinas == self.N):
                    self.solutions += 1
                    '''
                    print(
                        PARA N = {}
                        SOLUTION FOUND: {}
                        {} ciclos
                        .format(self.N, self.coords, ciclos))
                    '''

                    # Queens_ordered.print_board(self, self.coords);
                    # Ampliación: break para 1 solución
                    break;

            elif(y == self.N-1):
                # Backtracking
                (x, y) = self.coords[self.reinas-1]
                y += 1
                # Eliminamos la reina actual
                self.coords[self.reinas-1] = (None,None)
                self.reinas -= 1

                if(y >= self.N):
                    # Doble salto de backtracking
                    (x, y) = self.coords[self.reinas-1]
                    if(y == None): break

                    y += 1
                    self.coords[self.reinas-1] = (None,None)
                    self.reinas = self.reinas-1

            else:
                y += 1

        # if(self.solutions == 0):
            # print('\nNo se ha encontrado solución en ', self.ciclos, 'iteraciones')
        # else:
            # print(self.solutions, 'soluciones encontradas para N =', self.N)

        return ciclos

    def validate(self, reinas, x, y):
        size = len(list(filter(lambda r: r != (None, None), reinas)))

        for i in range(0, size):
            (r_x, r_y) = reinas[i]
            if(r_x==x or
              r_y==y or
              r_x-r_y == x-y or
              r_x+r_y == x+y):
                return False
        return True


def meta_test():
    for i in range(8, 12):
        N = i*2
        queens = Queens_ordered(N, i, P, K, L, pm, pc)
        queens.main()

def ods_writer():
    with open('detail.csv', 'w', newline='') as detail, open('mini.csv', 'w', newline='') as mini:
        detailWriter = csv.writer(detail)
        miniWriter  = csv.writer(mini)

        for i in range(4,12):
            N = i
            evaluaciones_sum = [];
            ciclos_sum = []

            for j in range(0,10):
                queens = Queens_binary(N, i, P, K, L, pm, pc)
                (evaluaciones, ciclos) = queens.main()
                print('N=',N,' en ', evaluaciones,'evaluaciones y', ciclos, 'ciclos')
                evaluaciones_sum.append(evaluaciones)
                ciclos_sum.append(ciclos)
                row = [N, evaluaciones, ciclos]
                detailWriter.writerow(row)

            meaneval = ft.reduce(lambda a,b: a+b, evaluaciones_sum)/10
            meanciclos = ft.reduce(lambda a,b: a+b, ciclos_sum)/10
            miniWriter.writerow([N, meaneval, meanciclos])

def ods_writer_bf():
    with open('detail.csv', 'w', newline='') as detail, open('mini.csv', 'w', newline='') as mini:
        detailWriter = csv.writer(detail)
        miniWriter  = csv.writer(mini)

        for i in range(21,25):
            N = i
            ciclos_sum = []

            queens = Queens_bruteforce(N)
            ciclos = queens.main()
            print('N=',N,' en ', ciclos, 'ciclos')
            miniWriter.writerow([N, ciclos])


'''

  _ __     __ _ _   _  ___  ___ _ __  ___
 | '_ \   / _` | | | |/ _ \/ _ \ '_ \/ __|
 | | | | | (_| | |_| |  __/  __/ | | \__ \
 |_| |_|  \__, |\__,_|\___|\___|_| |_|___/
             | |
             |_|

Posibles paramametros:
N: numero de reinas, dimension del tablero
i: iteraciones del AG
P: tamaño de población
K: tamaño de muestra de selección
L: número de ganadores del torneo (padres)

pm: probabilidad de mutación
pc: probabilidad de cruce

Ejemplo:
python3 AG_N_reinas.py 8 20000 100 20 10 0.1 0.9
'''

# def_N = int(sys.argv[1])
'''
i = int(sys.argv[2])
P = int(sys.argv[3])
K = int(sys.argv[4])
L = int(sys.argv[5])

pm = float(sys.argv[6])
pc = float(sys.argv[7])
'''

#meta_test()
ods_writer_bf()
# queens = Queens_binary(def_N, i, P, K, L, pm, pc)
# queens = Queens_bruteforce(def_N)
# queens.main()
