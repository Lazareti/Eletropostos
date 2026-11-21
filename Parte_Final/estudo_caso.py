"""
Teoria dos Grafos - Projeto Parte 3 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Estudo de caso: para algumas rotas reais e varias autonomias A, mostra se a
rota existe na rede atual (Dijkstra) e, quando nao existe, estima QUANTOS
eletropostos novos seriam necessarios e ENTRE QUAIS estacoes (vaos de
cobertura). Tambem estima quantos postos novos ligariam as componentes da
rede em cada autonomia.

Modelo (estimativa, nao e otimizacao de localizacao): o trecho direto entre
duas estacoes i e j tem distancia rodoviaria d (matriz OSRM, todos os pares).
Para que o trecho caiba na autonomia A, sao necessarios ceil(d/A) - 1 postos
novos ao longo dessa estrada, igualmente espacados. A rota viavel e a que
minimiza (postos novos, distancia total). Demanda, rede eletrica e custo
NAO sao considerados.

Uso:  python estudo_caso.py        (grava tambem dados/estudo_caso.md)

"""

import heapq
import math
import os
from grafoListaPonderado import Grafo
from algoritmos import dijkstra, reconstroiCaminho, autonomiaMinima, INFINITO
from conexidade import fconex
from caracteristicas import subgrafo, raizDe

AUTONOMIAS = [100, 150, 200, 250]
ARQ_GRAFO = os.path.join("dados", "grafo.txt")
ARQ_MATRIZ = os.path.join("dados", "matriz_direcional.csv")
ARQ_SAIDA = os.path.join("dados", "estudo_caso.md")

# rotas do estudo (id da estacao de origem, id da estacao de destino)
ROTAS = [(3, 68), (3, 14), (68, 59), (28, 3)]


# le a matriz de distancias rodoviarias (km) de todos os pares de estacoes;
# linha = origem, coluna = destino; separador ';'
def lerMatriz(nomeArq):
    with open(nomeArq, "r", encoding="utf-8") as arq:
        linhas = [l.rstrip("\n").split(";") for l in arq if l.strip()]
    return [[float(x) if x.strip() != "" else INFINITO for x in lin[1:]]
            for lin in linhas[1:]]


# postos novos necessarios para um trecho de distancia d caber na autonomia A
def postosNovos(d, autonomia):
    if d == INFINITO:
        return INFINITO
    return max(0, math.ceil(d / autonomia - 1e-9) - 1)


# rota que minimiza (postos novos, km) usando a matriz completa de distancias;
# retorna (caminho, postosNovos, km, trechos) com trechos = [(i, j, d, k)]
def rotaComPostosNovos(M, origem, destino, autonomia):
    n = len(M)
    custo = [(INFINITO, INFINITO)] * n
    pred = [-1] * n
    custo[origem] = (0, 0.0)
    fila = [((0, 0.0), origem)]
    while fila:
        (c, v) = heapq.heappop(fila)
        if c > custo[v]:
            continue
        for w in range(n):
            if w == v or M[v][w] == INFINITO:
                continue
            novo = (c[0] + postosNovos(M[v][w], autonomia), c[1] + M[v][w])
            if novo < custo[w]:
                custo[w] = novo
                pred[w] = v
                heapq.heappush(fila, (novo, w))
    caminho = reconstroiCaminho(pred, origem, destino)
    trechos = [(caminho[i], caminho[i + 1], M[caminho[i]][caminho[i + 1]],
                postosNovos(M[caminho[i]][caminho[i + 1]], autonomia))
               for i in range(len(caminho) - 1)]
    return (caminho, custo[destino][0], custo[destino][1], trechos)


# estima os postos novos para ligar as componentes f-conexas da rede com
# arcos <= autonomia: arvore geradora minima sobre as componentes, onde o
# custo de ligar duas componentes e o menor numero de postos novos entre
# um par de estacoes (usa o maior dos dois sentidos, para valer nos dois)
def ligacaoDeComponentes(g, M, autonomia):
    comps = fconex(subgrafo(g, autonomia))
    comps = [sorted(c) for c in comps]
    k = len(comps)
    ligacoes = []
    for a in range(k):
        for b in range(a + 1, k):
            melhor = None
            for i in comps[a]:
                for j in comps[b]:
                    d = max(M[i][j], M[j][i])
                    cand = (postosNovos(d, autonomia), d, i, j)
                    if melhor is None or cand < melhor:
                        melhor = cand
            ligacoes.append((melhor, a, b))
    ligacoes.sort(key=lambda x: x[0][:2])
    pai = list(range(k))
    escolhidas = []
    for (cand, a, b) in ligacoes:
        if raizDe(pai, a) != raizDe(pai, b):
            pai[raizDe(pai, a)] = raizDe(pai, b)
            escolhidas.append(cand)
    total = sum(c[0] for c in escolhidas)
    return (comps, escolhidas, total)


# rotulo da estacao v
def nome(g, v):
    return g.rotulos[v]


# monta o texto do estudo de caso (tabelas e vaos de cobertura)
def relatorio(g, M):
    saida = []
    p = saida.append
    p("# Estudo de caso - rotas, autonomia e vaos de cobertura\n")
    p("Dados: grafo.txt (85 estacoes, 1.640 arcos <= 250 km, pesos por "
      "sentido) e matriz_direcional.csv (distancia rodoviaria de todos os "
      "pares, OSRM).\n")

    p("## 1. Rotas por autonomia na rede atual (Dijkstra)\n")
    p("| Rota | " + " | ".join(f"A = {a} km" for a in AUTONOMIAS) + " |")
    p("|---|" + "---|" * len(AUTONOMIAS))
    for (o, d) in ROTAS:
        celulas = []
        for A in AUTONOMIAS:
            (dist, pred) = dijkstra(g, o, A)
            cam = reconstroiCaminho(pred, o, d)
            if cam:
                celulas.append(f"{dist[d]:.1f} km, {len(cam) - 2} recargas")
            else:
                celulas.append("sem rota")
        p(f"| {nome(g, o)} -> {nome(g, d)} | " + " | ".join(celulas) + " |")
    p("")
    p("Autonomia minima que viabiliza cada rota na rede atual:\n")
    for (o, d) in ROTAS:
        am = autonomiaMinima(g, o, d)
        p(f"- {nome(g, o)} -> {nome(g, d)}: "
          f"{'%.1f km' % am if am is not None else 'nao existe rota'}")
    p("")

    p("## 2. Postos novos estimados para viabilizar cada rota\n")
    p("Cada celula: menor numero de postos novos / distancia total da rota "
      "(0 postos = ja viavel).\n")
    p("| Rota | " + " | ".join(f"A = {a} km" for a in AUTONOMIAS) + " |")
    p("|---|" + "---|" * len(AUTONOMIAS))
    detalhes = []
    for (o, d) in ROTAS:
        celulas = []
        for A in AUTONOMIAS:
            (cam, novos, km, trechos) = rotaComPostosNovos(M, o, d, A)
            celulas.append(f"{novos} / {km:.1f} km")
            if novos > 0:
                detalhes.append((o, d, A, novos, km, trechos))
        p(f"| {nome(g, o)} -> {nome(g, d)} | " + " | ".join(celulas) + " |")
    p("")

    p("## 3. Onde ficam os vaos (trechos que precisam de posto novo)\n")
    for (o, d, A, novos, km, trechos) in detalhes:
        p(f"**{nome(g, o)} -> {nome(g, d)}, A = {A} km:** {novos} posto(s) "
          f"novo(s), {km:.1f} km no total")
        for (i, j, dist, k) in trechos:
            if k > 0:
                pos = ", ".join(f"{(t * dist / (k + 1)):.0f}"
                                for t in range(1, k + 1))
                p(f"- entre {nome(g, i)} e {nome(g, j)} ({dist:.1f} km): "
                  f"{k} posto(s), a cerca de {pos} km de {nome(g, i)}")
        p("")

    p("## 4. Rede inteira: componentes e postos para liga-las\n")
    p("| Autonomia | Componentes f-conexas | Postos novos (estimativa minima "
      "para ligar todas) |")
    p("|---|---|---|")
    ligacoes = {}
    for A in AUTONOMIAS:
        (comps, esc, total) = ligacaoDeComponentes(g, M, A)
        ligacoes[A] = esc
        p(f"| {A} km | {len(comps)} | {total} |")
    p("")
    for A in AUTONOMIAS:
        if not ligacoes[A]:
            continue
        p(f"Ligacoes escolhidas para A = {A} km (postos novos, km, "
          f"estacoes extremas):")
        for (k, d, i, j) in ligacoes[A]:
            if k > 0:
                p(f"- {k} posto(s) entre {nome(g, i)} e {nome(g, j)} "
                  f"({d:.1f} km)")
        p("")
    p("Limites: estimativa por trecho rodoviario direto entre estacoes "
      "existentes, com postos igualmente espacados; nao considera demanda, "
      "capacidade da rede eletrica, custo nem a posicao exata de "
      "cidades/postos de combustivel ao longo da via. Serve para "
      "dimensionar os vaos de cobertura, nao para decidir localizacoes.")
    return "\n".join(saida)


# executa o estudo de caso, mostra na tela e grava em dados/estudo_caso.md
def main():
    g = Grafo(0)
    g.lerArquivo(ARQ_GRAFO)
    M = lerMatriz(ARQ_MATRIZ)
    texto = relatorio(g, M)
    print(texto)
    with open(ARQ_SAIDA, "w", encoding="utf-8") as arq:
        arq.write(texto + "\n")


if __name__ == "__main__":
    main()
