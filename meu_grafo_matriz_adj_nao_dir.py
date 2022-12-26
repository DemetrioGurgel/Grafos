from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoMatrizAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        verticesNaoAdjacentes = set()
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                novaAresta = f'{self.vertices[i]}-{self.vertices[j]}'
                if len(self.matriz[i][j]) == 0:
                    verticesNaoAdjacentes.add(novaAresta)

        return verticesNaoAdjacentes

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in range(len(self.vertices)):
            if len(self.matriz[i][i]) > 0:
                return True

        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        v = self.get_vertice(V)
        indiceVertice = self.indice_do_vertice(v)
        grau = 0

        for j in range(indiceVertice, len(self.vertices)):
            if j == indiceVertice:
                grau += 2 * len(self.matriz[indiceVertice][j])
            else:
                grau += len(self.matriz[indiceVertice][j])

        for i in range(indiceVertice):
            grau += len(self.matriz[i][indiceVertice])

        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for i in range(len(self.vertices)):
            for j in range(i, len(self.vertices)):
                if len(self.matriz[i][j]) > 1:
                    return True

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

        v = self.get_vertice(V)
        indiceVertice = self.indice_do_vertice(v)
        arestas = set()

        for j in range(indiceVertice, len(self.vertices)):
            parAtual = self.matriz[indiceVertice][j]
            for aresta in parAtual:
                arestas.add(aresta)

        for i in range(indiceVertice):
            parAtual = self.matriz[i][indiceVertice]
            for aresta in parAtual:
                arestas.add(aresta)
        return arestas

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''
        if self.ha_laco():
            return False

        for i in range(len(self.vertices)):
            for j in range(i+1, len(self.vertices)):
                if len(self.matriz[i][j]) == 0:
                    return False

        return True
