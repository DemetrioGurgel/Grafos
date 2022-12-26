from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *
from collections import deque
import heapq
from copy import deepcopy
from math import inf
import math

class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        arestasGrafo = set()
        for a in self.arestas:
            arestaAtual = self.arestas[a]
            verticesAresta = f'{arestaAtual.v1}-{arestaAtual.v2}'
            arestasGrafo.add(verticesAresta)

        verticesNaoAdjacentes = set()
        for i in range(len(self.vertices)):
            for j in range(i+1, len(self.vertices)):
                novaAresta = f'{self.vertices[i]}-{self.vertices[j]}'
                if novaAresta not in arestasGrafo and novaAresta[::-1] not in arestasGrafo:
                    verticesNaoAdjacentes.add(novaAresta)

        return verticesNaoAdjacentes

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for a in self._arestas:
            if self._arestas[a].v1 == self._arestas[a].v2:
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''
        grau = 0

        if (not self.existe_rotulo_vertice(V)):
            raise VerticeInvalidoError()
        for a in self._arestas:
            if self.arestas[a].v1.rotulo == V:
                grau += 1
            if self.arestas[a].v2._rotulo == V:
                grau += 1

        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        arestas = set()
        for a in self.arestas:

            arestaAtual = self.arestas[a]
            verticesAresta = (arestaAtual.v1.rotulo, arestaAtual.v2.rotulo)

            if verticesAresta in arestas or verticesAresta[::-1] in arestas:
                return True

            arestas.add(verticesAresta)

        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        else:
            conj = set()
            for a in self.arestas:
                if self.arestas[a].v1.rotulo == V or self.arestas[a].v2.rotulo == V:
                    conj.add(a)
            return conj

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        for v in self.vertices:
            if self.grau(v.rotulo) != len(self.vertices)-1:
                return False
        return True

    def dfs(self, V=''):
        '''
        :param V: Vertice a ser utilizado como raiz
        :return: Uma chamada a função auxiliar para a busca em profundidade
        '''
        arv_dfs = MeuGrafo()
        arv_dfs.adiciona_vertice(V)
        return self.dfs_rec(V, arv_dfs)

    def dfs_rec(self, V, arv_dfs):
        '''
        Função recursiva para busca em profundidade
        :param V: Vertice a ser utilizado como raiz
        :param arv_dfs: Arvore DFS
        :return: Retorna o grafo de busca em profundidade
        '''
        if len(self.vertices) == len(arv_dfs.vertices):
            return arv_dfs
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        aux = self.arestas_sobre_vertice(V)
        rotulos = list(aux)
        rotulos.sort()
        for a in rotulos:
            if not arv_dfs.existe_rotulo_vertice(a):
                if V == self.arestas[a].v1.rotulo:
                    r = self.arestas[a].v2.rotulo
                else:
                    r = self.arestas[a].v1.rotulo

                if not arv_dfs.existe_rotulo_vertice(r):
                    arv_dfs.adiciona_vertice(r)
                    arv_dfs.adiciona_aresta(self.arestas[a])
                    self.dfs_rec(r, arv_dfs)

        return arv_dfs

    def bfs(self, V=''):
        '''
        :param V: Vertice a ser utilizado como raiz
        :return: Uma chamada a função auxiliar para a busca em largura
        '''
        arv_bfs = MeuGrafo()
        arv_bfs.adiciona_vertice(V)
        return self.bfs_rec(V, arv_bfs)

    def bfs_rec(self, V, arv_bfs):
        '''
        Função recursiva para busca em largura
        :param V: Vertice a ser utilizado como raiz
        :param arv_bfs: Árvore BFS
        :return: Retorna o grafo de busca em largura
        '''
        if len(self.vertices) == len(arv_bfs.vertices):
            return arv_bfs
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        for a in self.arestas:
            if self.arestas[a].v1.rotulo == V and self.arestas[a].v1.rotulo != self.arestas[a].v2.rotulo:
                aux = self.arestas[a].v1.rotulo
                prox = self.arestas[a].v2.rotulo
                if arv_bfs.existe_rotulo_vertice(aux) and not arv_bfs.existe_rotulo_vertice(prox):
                    arv_bfs.adiciona_vertice(prox)
                    arv_bfs.adiciona_aresta(self.arestas[a])
        self.bfs_rec(prox, arv_bfs)

        return arv_bfs

    def ha_ciclo(self):
        '''
        Verifica se o grafo possui algum ciclo.
        :return: Um valor booleano que indica se o grafo possui algum ciclo.
        '''
        for a in self.arestas:
            retorno = set()
            ciclo = MeuGrafo()
            V = self.arestas[a].v1.rotulo
            ciclo.adiciona_vertice(V)

            return self.ciclo_rec(retorno, V, ciclo)

    def ciclo_rec(self, retorno, V, ciclo):

        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError

        if len(retorno) > 0:
            return True

        if len(self.vertices) == len(ciclo.vertices):
            return False

        rotulo = self.arestas_sobre_vertice(V)
        rotulos = list(rotulo)
        rotulos.sort()

        for a in rotulos:
            if not ciclo.existe_rotulo_vertice(a):
                if V == self.arestas[a].v1.rotulo:
                    r = self.arestas[a].v2.rotulo
                else:
                    r = self.arestas[a].v1.rotulo

                if ciclo.existe_rotulo_vertice(r):
                    retorno.add(r)
                else:
                    ciclo.adiciona_vertice(r)
                    ciclo.adiciona_aresta(self.arestas[a])
                self.ciclo_rec(retorno, r, ciclo)
        return ciclo

    def caminho(self, n):
        '''
        Verifica se existe um caminho entre os vértices V1 e V2.
        :param n: quantidade
        :return: Um valor booleano que indica se existe um caminho entre os vértices V1 e V2
        '''
        V = self.vertices[0].rotulo
        arvore = self.dfs(V)
        caminho = list()
        listArestas = []
        caminho.append(V)
        result, tam = self.aux_caminho(V, arvore, caminho, n, listArestas)
        return result if tam == n else False

    def aux_caminho(self, V, arvore, caminho, n, listArestas):
        rotulos = self.arestas_sobre_vertice(V)
        arestas_no_vertice = list(rotulos)
        arestas_no_vertice.sort()
        for a in arestas_no_vertice:
            if not a in caminho:
                if V == arvore.arestas[a].v1.rotulo:
                    r = arvore.arestas[a].v2.rotulo
                else:
                    r = arvore.arestas[a].v1.rotulo

                if len(listArestas) + 1 < n:
                    if arvore.grau(r) > 1:
                        caminho.append(a)
                        caminho.append(r)
                        listArestas.append(a)
                        self.aux_caminho(r, arvore, caminho, n, listArestas)
                else:
                    caminho.append(a)
                    caminho.append(r)
                    listArestas.append(a)
                    return caminho
        return caminho, len(listArestas)

    def conexo(self):
        '''
        Verifica se o grafo é conexo.
        :return: Um valor booleano que indica se o grafo é conexo
        '''
        qtd_vertices = len(self.vertices)
        vertice = self.vertices[0]
        vertice = str(vertice)
        arvore = self.dfs(vertice)
        qtd_Vconexo = len(arvore.vertices)

        if qtd_Vconexo == qtd_vertices:
            return True
        else:
            return False

    def prim(self, ):
        prim = MeuGrafo()
        teste = self.ordena()
        test1 = teste[0]
        proximo = self.arestas[test1].v1.rotulo
        visitados = []
        prim.adiciona_vertice(proximo)
        while True:
            if len(self.vertices) == len(prim.vertices):
                break
            sobre = self.arestas_sobre_vertice(proximo)
            menor = inf
            menor_aresta = ''
            for a in sobre:
                if self.arestas[a].peso <= menor:
                    if not prim.existe_rotulo_vertice(self.oposto(proximo, self.arestas[a])):
                        menor_aresta = self.arestas[a]
                        menor = self.arestas[a].peso
            visitados.append(menor_aresta)
            if menor_aresta.v1.rotulo == proximo:
                proximo = menor_aresta.v2.rotulo
            else:
                proximo = menor_aresta.v1.rotulo
            if not prim.existe_rotulo_vertice(proximo):
                prim.adiciona_vertice(proximo)
                prim.adiciona_aresta(menor_aresta)

        return prim

    def oposto(self, V, a):
        if a.v1.rotulo == V:
            V = a.v2.rotulo
            return V
        else:
            V = a.v1.rotulo
            return V

    def Kruskall(self):
        arvore_kruskall = MeuGrafo()
        fila_prioridade = self.bucket_sort_kruskall()
        for v in self.vertices:
            arvore_kruskall.adiciona_vertice(v.rotulo)

        for i in range(len(fila_prioridade)):
            for a in fila_prioridade[i]:
                aresta = self.arestas[a]
                kruskall_dfs = arvore_kruskall.dfs(aresta.v1.rotulo)

                if kruskall_dfs.existe_rotulo_vertice(aresta.v1.rotulo) and kruskall_dfs.existe_rotulo_vertice(
                        aresta.v2.rotulo):
                    pass
                else:
                    arvore_kruskall.adiciona_aresta(aresta)

        return arvore_kruskall

    def ordena(self):
        ordenada = []
        menor = inf
        for a in self.arestas:
            if self.arestas[a].peso <= menor and not a in ordenada:
                menor = self.arestas[a].peso
        while len(ordenada) < len(self.arestas):
            for a in self.arestas:
                if self.arestas[a].peso == menor:
                    ordenada.append(a)
            menor += 1
        return ordenada

    def bucket_sort_kruskall(self):
        lista_pesos = []
        for a in self.arestas:
            if not self.arestas[a].peso in lista_pesos:
                lista_pesos.append(self.arestas[a].peso)
        lista_pesos.sort()
        bucket = list()
        for i in range(len(lista_pesos)):
            bucket.append([])
            for a in self.arestas:
                if self.arestas[a].peso == lista_pesos[i]:
                    bucket[i].append(a)
        return bucket