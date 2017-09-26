import random as r
import sys

class Queens:

    def __init__(self, N):
        self.fitnesses = [];

        poblacion = [];
        for p in range(0, 100):
            poblacion.append([r.randrange(0,N) for i in range(0,N)]);

        self.poblacion = poblacion;

    def main(self):
        poblacion = self.poblacion;
        while ( not criteriodeparada ):
            padres = seleccion(poblacion);
            nuevaPoblacion = cruzar(padres);
            # mutacion, reemplazo?
            # generacion despues de cruce: si hijo ya en poblacion, do not add
            reinas = nuevaPoblacion;

    def getFitness(poblacion):
        N = len(poblacion)
        bad = 0;
        for (y, reina) in enumerate(poblacion):
            break;

        # return (n/N - bad/n)
        return (1 - bad/N)

    def seleccion(poblacion):
        K = 4;
        L = 2;
        return torneo(poblacion, K, L);

    def torneo(poblacion, K, L):
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

        muestra.sort(key=getFitness)
        
        pass;

    def cruzar(poblacion):
        pass;


a = Queens(int(sys.argv[1]))
