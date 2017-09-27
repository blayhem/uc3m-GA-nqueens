import random as r
import sys

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
            padres = self.seleccion(poblacion);
            nuevaPoblacion = self.cruzar(padres);
            # mutamos la nueva poblacion
            nuevaPoblacion = list(map(lambda ind: self.mutacion(ind), nuevaPoblacion));
            # reemplazo?
            # nuevaPoblacion: si hijo ya en poblacion, do not add
            poblacion = nuevaPoblacion;
            criteriodeparada = True;

    def getFitness(self, poblacion):
        bad = 0;
        for (y, reina) in enumerate(poblacion):
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
            muestra.append(poblacion[sel])
            taken.append(sel)

        muestra.sort(key=self.getFitness)
        return muestra[0:L]

    def cruzar(self, poblacion):
        return poblacion;

    def mutacion(self, individuo):
        p = 0.001; # probabilidad de mutar
        for i in range(0, len(individuo)):
            if(r.uniform(0, 1) < p):
                individuo[i] = r.randrange(0,N);

        return individuo;



queens = Queens(int(sys.argv[1]))
queens.main()
