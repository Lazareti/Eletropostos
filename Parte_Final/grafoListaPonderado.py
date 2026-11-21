"""
Teoria dos Grafos - Projeto Parte 2 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Grafo orientado com peso na aresta (tipo 6) como lista de adjacencia,
derivado de grafoLista.py, com pesos, rotulos, insereV/removeV
e leitura/gravacao do grafo.txt.

"""


class Grafo:
    TAM_MAX_DEFAULT = 100

    #cria o grafo vazio com n vertices
    def __init__(self, n=TAM_MAX_DEFAULT, tipo=6):
        self.n = n
        self.m = 0
        self.tipo = tipo
        self.listaAdj = [[] for i in range(self.n)]  # listaAdj[v] = [(w, peso), ...]
        self.rotulos = [str(i) for i in range(self.n)]

    # verifica se ja existe o arco v -> w
    def existeA(self, v, w):
        for (dest, peso) in self.listaAdj[v]:
            if dest == w:
                return True
        return False

    # insere o arco v -> w com peso, atualiza se ja existir
    def insereA(self, v, w, peso=1.0):
        for i in range(len(self.listaAdj[v])):
            if self.listaAdj[v][i][0] == w:
                self.listaAdj[v][i] = (w, peso)
                return
        self.listaAdj[v].append((w, peso))
        self.m += 1

    # remove o arco v -> w, retorna True se ele existia
    def removeA(self, v, w):
        for i in range(len(self.listaAdj[v])):
            if self.listaAdj[v][i][0] == w:
                self.listaAdj[v].pop(i)
                self.m -= 1
                return True
        return False

    # insere um vertice com rotulo e retorna o id dele
    def insereV(self, rotulo=""):
        self.listaAdj.append([])
        if rotulo == "":
            rotulo = str(self.n)
        self.rotulos.append(rotulo)
        self.n += 1
        return self.n - 1

    # remove o vertice v junto com seus arcos e renumera os demais
    def removeV(self, v):
        self.m -= len(self.listaAdj[v])
        self.listaAdj.pop(v)
        self.rotulos.pop(v)
        for i in range(len(self.listaAdj)):
            novaLista = []
            for (w, peso) in self.listaAdj[i]:
                if w == v:
                    self.m -= 1
                elif w > v:
                    novaLista.append((w - 1, peso))
                else:
                    novaLista.append((w, peso))
            self.listaAdj[i] = novaLista
        self.n -= 1

    # le o grafo.txt para a memoria
    def lerArquivo(self, nomeArq):
        with open(nomeArq, "r", encoding="utf-8") as arq:
            tipo = int(arq.readline())
            if tipo != 6:
                raise ValueError(f"Tipo {tipo} nao suportado (esperado 6).")
            n = int(arq.readline())
            rotulos = []
            for i in range(n):
                linha = arq.readline().strip()
                ini = linha.find('"')
                fim = linha.rfind('"')
                if ini != -1 and fim > ini:
                    rotulos.append(linha[ini + 1:fim])
                else:
                    rotulos.append(linha.split()[-1])
            m = int(arq.readline())
            self.n = n
            self.m = 0
            self.tipo = tipo
            self.listaAdj = [[] for i in range(n)]
            self.rotulos = rotulos
            for i in range(m):
                v, w, p = arq.readline().split()
                self.insereA(int(v), int(w), float(p))

    # grava o grafo no arquivo, no formato do enunciado
    def gravarArquivo(self, nomeArq):
        with open(nomeArq, "w", encoding="utf-8") as arq:
            arq.write(f"{self.tipo}\n{self.n}\n")
            for i in range(self.n):
                arq.write(f'{i} "{self.rotulos[i]}"\n')
            arq.write(f"{self.m}\n")
            for v in range(self.n):
                for (w, peso) in self.listaAdj[v]:
                    arq.write(f"{v} {w} {peso:g}\n")

    # imprime a lista de adjacencia com rotulos
    def show(self):
        print(f"\n n: {self.n:2d} ", end="")
        print(f"m: {self.m:2d}")
        for i in range(self.n):
            print(f"\n{i:2d} ({self.rotulos[i]}): ", end="")
            for w in range(len(self.listaAdj[i])):
                (dest, peso) = self.listaAdj[i][w]
                print(f"({dest:2d}, {peso:6.1f} km)", end=" ")
        print("\n\nfim da impressao do grafo.")

    # impressao compacta, sem rotulos
    def showMin(self):
        print(f"\n n: {self.n:2d} ", end="")
        print(f"m: {self.m:2d}\n")
        for i in range(self.n):
            print(f"{i:2d}: ", end="")
            for w in range(len(self.listaAdj[i])):
                (dest, peso) = self.listaAdj[i][w]
                print(f"{dest:2d}({peso:g})", end=" ")
            print()
        print("\nfim da impressao do grafo.")
