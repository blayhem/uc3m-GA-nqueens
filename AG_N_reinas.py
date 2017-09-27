import random as r
import sys
import math
import functools as ft

class Queens:

    def __init__(self, N):
        self.N = N;
        self.fitnesses = [];

        poblacion = [];
        for p in range(0, 100):
            poblacion.append([r.randrange(0,N) for i in range(0,N)]);

        self.poblacion = poblacion;

    def main(self):
        poblacion = self.poblacion;
        criteriodeparada = False;
        while ( not criteriodeparada ):
            '''
            1. Seleccionamos los padres. Los quitamos de la poblacion para hacer cruce.
            '''
            print('\npoblacion inicial:', len(poblacion))
            padres = self.seleccion(poblacion);
            print('padres:', padres)
            # map(lambda p: poblacion.pop(poblacion.index(p)), padres);
            # for p in padres:
            #     poblacion.pop(poblacion.index(p))
            print('poblacion sin padres: ', len(poblacion))

            '''
            2. Hacemos cruce con reemplazo, los padres vuelven a la poblacion
            porque K=4 pero L=2 (perdemos 2 individuos).
            self.cruce nos devuelve 4 individuos, 2 padres y 2 hijos.
            '''
            nuevaPoblacion = self.cruzar(padres);
            print('despues de cruce: \t', nuevaPoblacion)

            '''
            3. Mutamos la nueva poblacion.
            Politica opcional: if son has clone in poblacion, do not add.
            '''
            nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
            print('con mutacion: \t\t', nuevaPoblacion)
            poblacion += nuevaPoblacion;
            criteriodeparada = True;

    def getFitness(self, individuo):
        bad = 0;
        reinas = []
        for (y, x) in enumerate(individuo): # tuplas de posiciones de reinas
            reinas.append([x, y]);
            # if(r[0]==x or r[1]==y or r[0]-r[1] == x-y or r[1]+r[0] == y+x):
            #     bad += 1;

            break;

        # return (n/N - bad/n)
        return (1 - bad/self.N)

    def seleccion(self, poblacion):
        K = 4;
        L = 2;
        return self.torneo(poblacion, K, L);

    def torneo(self, poblacion, K, L):
        muestra = []
        taken = []
        '''
        Construimos la muestra K a partir de poblacion
        '''
        for i in range(0,K):
            sel = r.randrange(0,len(poblacion))
            while(sel in taken):
                sel = r.randrange(0,len(poblacion));
            muestra.append(poblacion.pop(sel));
            taken.append(sel);

        muestra.sort(key=self.getFitness)
        return muestra[0:L]

    def cruzar(self, poblacion):
        pc = 0.2; # crossover probability

        for i in range(0, 2):
            if(r.uniform(0,1) < pc):
                corte = math.floor(r.uniform(0, self.N));
                new = poblacion[0][0:corte] + poblacion[1][corte:self.N];
                poblacion.append(new)
            else:
                poblacion.append(poblacion[i]);

        return poblacion;

    def mutacion(self, individuo):
        p = 0.001; # probabilidad de mutar
        for i in range(0, len(individuo)):
            if(r.uniform(0, 1) < p):
                individuo[i] = r.randrange(0,self.N);

        return individuo;



queens = Queens(int(sys.argv[1]))
queens.main()
