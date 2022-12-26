from bibgrafo.grafo_matriz_adj_dir import *
from bibgrafo.grafo_errors import *
from math import inf

class MeuGrafo(GrafoMatrizAdjacenciaDirecionado):

    def vertices_nao_adjacentes(self):
        pass

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in range(len(self.vertices)):
            if len(self.matriz[i][i]) >= 1:
                return True
        return False


    def grau(self, V=''):
        pass

    def ha_paralelas(self):
        pass

    def arestas_sobre_vertice(self, V):
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        v = self.get_vertice(V)
        indiceVertice = self.indice_do_vertice(v)
        arestas = list()

        for j in range(len(self.matriz)):
            for aresta in self.matriz[indiceVertice][j]:
                arestas.append(self.matriz[indiceVertice][j][aresta])
        for j in range(len(self.matriz)):
            for aresta in self.matriz[j][indiceVertice]:
                arestas.append(self.matriz[j][indiceVertice][aresta])
        return arestas

    def eh_completo(self):
        pass

    def warshall(self):
        E = []

        for i in range(len(self.vertices)):
            linha = []
            for j in range(len(self.vertices)):
                if len(self.matriz[i][j]) >= 1:
                    linha.append(1)
                else:
                    linha.append(0)
            E.append(linha)

        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if E[j][i] == 1:
                    for k in range(len(self.vertices)):
                        E[j][k] = E[j][k] if E[j][k] > E[i][k] else E[i][k]
        return E


    def dijkstra(self, I, F):
        beta = {}
        phi = {}
        pi = {}
        w = I
        for n in self.vertices:
            v = str(n)
            beta[v] = inf
            phi[v] = 0
            pi[v] = 0
        beta[I] = 0
        phi[I] = 1
        w = I
        while True:
            sobre = self.arestas_sobre_vertice(w)
            if w == F:
                break
            for x in sobre:
                contrario = ""
                if w == x.v1.rotulo:
                    contrario = x.v2.rotulo
                else:
                    contrario = x.v1.rotulo
                if beta[contrario] > beta[w] + x.peso and phi[contrario] == 0:
                    beta[contrario] = beta[w] + x.peso
                    pi[contrario] = w
            menor = inf
            for i in beta:
                if beta[i] < menor and phi[i] == 0:
                    menor = beta[i]
            w = list(beta.keys())[list(beta.values()).index(menor)]
            phi[w] = 1
        r = F
        caminho = []
        while True:
            caminho.append(r)
            if r == I:
                return caminho
            r = pi[r]
