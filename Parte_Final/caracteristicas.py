"""
Teoria dos Grafos - Projeto Parte 3 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Caracteristicas do problema modelado, obtidas com tecnicas da disciplina:
graus dos vertices, grafo euleriano (ciclo/trilha em grafo orientado),
coloracao de vertices (Welsh-Powell), pontos de articulacao e pontes
(conectividade) e arvore geradora minima (Kruskal).

Convencao: as analises de coloracao, articulacao e arvore geradora usam o
grafo NAO ORIENTADO subjacente (ha aresta {u,v} se existe o arco u->v ou
v->u; o peso e o menor dos dois sentidos). Graus e Euler usam o grafo
orientado. Todas aceitam uma autonomia A: so entram os arcos com peso <= A.

"""

import sys
from grafoListaPonderado import Grafo


# copia do grafo apenas com os arcos de peso <= autonomia (mesmos vertices)
def subgrafo(g, autonomia):
    h = Grafo(g.n, g.tipo)
    h.rotulos = list(g.rotulos)
    for v in range(g.n):
        for (w, peso) in g.listaAdj[v]:
            if peso <= autonomia:
                h.insereA(v, w, peso)
    return h


# graus de entrada e de saida de todos os vertices
def graus(g):
    entrada = [0] * g.n
    saida = [len(g.listaAdj[v]) for v in range(g.n)]
    for v in range(g.n):
        for (w, peso) in g.listaAdj[v]:
            entrada[w] += 1
    return (entrada, saida)


# grafo nao orientado subjacente: (vizinhos, pesos); pesos[(a, b)] com a < b
# guarda o menor peso entre os dois sentidos
def subjacente(g):
    vizinhos = [set() for i in range(g.n)]
    pesos = {}
    for v in range(g.n):
        for (w, peso) in g.listaAdj[v]:
            vizinhos[v].add(w)
            vizinhos[w].add(v)
            chave = (min(v, w), max(v, w))
            if chave not in pesos or peso < pesos[chave]:
                pesos[chave] = peso
    return (vizinhos, pesos)


# componentes conexas (ignorando sentido), ignorando os vertices em 'proibidos'
def componentesConexas(vizinhos, proibidos=()):
    visto = set(proibidos)
    componentes = []
    for ini in range(len(vizinhos)):
        if ini in visto:
            continue
        comp = [ini]
        visto.add(ini)
        pilha = [ini]
        while pilha:
            v = pilha.pop()
            for w in vizinhos[v]:
                if w not in visto:
                    visto.add(w)
                    comp.append(w)
                    pilha.append(w)
        componentes.append(sorted(comp))
    return componentes


# id e rotulo da estacao, para as mensagens
def rotuloCurto(g, v):
    return f"{v}:{g.rotulos[v]}"


# estatisticas de grau: retorna dicionario com os numeros calculados
def estatisticasGraus(g):
    (entrada, saida) = graus(g)
    n = max(g.n, 1)
    return {"entrada": entrada, "saida": saida,
            "mediaSaida": sum(saida) / n,
            "minSaida": min(saida, default=0), "maxSaida": max(saida, default=0),
            "minEntrada": min(entrada, default=0),
            "maxEntrada": max(entrada, default=0),
            "isolados": [v for v in range(g.n)
                         if entrada[v] == 0 and saida[v] == 0]}


# opcao k: imprime as estatisticas de grau de entrada e de saida
def showGraus(g):
    est = estatisticasGraus(g)
    (entrada, saida) = (est["entrada"], est["saida"])
    print("\n------------------ GRAUS DOS VERTICES ------------------")
    print(f"Vertices: {g.n}   Arcos: {g.m}")
    print(f"Grau de saida  : min {est['minSaida']}  media {est['mediaSaida']:.1f}"
          f"  max {est['maxSaida']}")
    print(f"Grau de entrada: min {est['minEntrada']}  media "
          f"{sum(entrada) / max(g.n, 1):.1f}  max {est['maxEntrada']}")
    print("\nDistribuicao do grau de saida (estacoes alcancaveis em 1 trecho):")
    faixas = [(0, 0), (1, 5), (6, 10), (11, 20), (21, 10 ** 9)]
    for (a, b) in faixas:
        qtd = sum(1 for v in range(g.n) if a <= saida[v] <= b)
        nome = f"{a}" if a == b else (f"{a}+" if b == 10 ** 9 else f"{a}-{b}")
        print(f"  grau {nome:>5}: {qtd:3d} {'#' * qtd}")
    ordem = sorted(range(g.n), key=lambda v: (-saida[v], v))
    print("\nEstacoes mais conectadas (maior grau de saida):")
    for v in ordem[:5]:
        print(f"  {rotuloCurto(g, v)}  saida {saida[v]}  entrada {entrada[v]}")
    frageis = [v for v in range(g.n) if 0 < saida[v] + entrada[v] and
               saida[v] <= 2]
    print(f"\nEstacoes frageis (grau de saida <= 2): {len(frageis)}")
    for v in frageis[:10]:
        print(f"  {rotuloCurto(g, v)}  saida {saida[v]}  entrada {entrada[v]}")
    print(f"Estacoes isoladas (sem nenhum arco): {len(est['isolados'])}")
    for v in est["isolados"]:
        print(f"  {rotuloCurto(g, v)}")
    print("---------------------------------------------------------\n")
    return est


# Condicoes para grafo orientado: ciclo euleriano <=> todo vertice com grau de
# entrada = grau de saida e os vertices com arcos formam uma so componente
# conexa; trilha euleriana <=> idem, exceto um vertice com saida-entrada = 1
# (inicio) e um com entrada-saida = 1 (fim).
def analisaEuler(g):
    (entrada, saida) = graus(g)
    desbalanceados = [v for v in range(g.n) if entrada[v] != saida[v]]
    ativos = set(v for v in range(g.n) if entrada[v] + saida[v] > 0)
    (vizinhos, pesos) = subjacente(g)
    # so contam as componentes que tem arcos (vertice sem arco e ignorado)
    comps = [c for c in componentesConexas(vizinhos)
             if any(v in ativos for v in c)]
    conexo = len(comps) <= 1
    inicios = [v for v in desbalanceados if saida[v] - entrada[v] == 1]
    fins = [v for v in desbalanceados if entrada[v] - saida[v] == 1]
    ciclo = conexo and not desbalanceados
    trilha = conexo and (not desbalanceados or
                         (len(desbalanceados) == 2 and len(inicios) == 1
                          and len(fins) == 1))
    return {"entrada": entrada, "saida": saida,
            "desbalanceados": desbalanceados, "componentes": len(comps),
            "conexo": conexo, "ciclo": ciclo, "trilha": trilha}


# opcao l: imprime se o grafo tem ciclo ou trilha euleriana
def showEuler(g):
    r = analisaEuler(g)
    (entrada, saida) = (r["entrada"], r["saida"])
    print("\n---------------- GRAFO EULERIANO (ORIENTADO) ----------------")
    print("Ciclo euleriano: todo vertice com grau de entrada = grau de saida")
    print("                 e arcos em uma unica componente conexa.")
    print(f"Componentes com arcos: {r['componentes']}"
          f" ({'conexo' if r['conexo'] else 'DESCONEXO'})")
    print(f"Vertices com entrada != saida: {len(r['desbalanceados'])}")
    for v in r["desbalanceados"][:15]:
        print(f"  {rotuloCurto(g, v)}  entrada {entrada[v]}  saida {saida[v]}"
              f"  (saida - entrada = {saida[v] - entrada[v]:+d})")
    print(f"\nTem ciclo euleriano? {'SIM' if r['ciclo'] else 'NAO'}")
    print(f"Tem trilha (percurso) euleriana? {'SIM' if r['trilha'] else 'NAO'}")
    if not r["ciclo"]:
        print("Motivo:", end=" ")
        motivos = []
        if not r["conexo"]:
            motivos.append("o grafo e desconexo")
        if r["desbalanceados"]:
            motivos.append("ha vertices com entrada != saida "
                           "(arcos de mao unica / distancias de ida e volta "
                           "diferentes)")
        print("; ".join(motivos) + ".")
    print("--------------------------------------------------------------\n")
    return r


# colore o grafo subjacente: vertices em ordem decrescente de grau, cada um
# recebe a menor cor ainda nao usada por seus vizinhos. Retorna cor[v].
def coloracaoWelshPowell(vizinhos):
    n = len(vizinhos)
    ordem = sorted(range(n), key=lambda v: (-len(vizinhos[v]), v))
    cor = {}
    for v in ordem:
        usadas = set(cor[w] for w in vizinhos[v] if w in cor)
        c = 0
        while c in usadas:
            c += 1
        cor[v] = c
    return [cor[v] for v in range(n)]


# tamanho de uma clique obtida de forma gulosa (limite inferior do numero
# cromatico: uma clique de tamanho k exige k cores)
def cliqueGulosa(vizinhos):
    melhor = []
    for ini in range(len(vizinhos)):
        clique = [ini]
        candidatos = set(vizinhos[ini])
        while candidatos:
            u = max(candidatos, key=lambda x: (len(vizinhos[x] & candidatos), -x))
            clique.append(u)
            candidatos &= vizinhos[u]
        if len(clique) > len(melhor):
            melhor = clique
    return sorted(melhor)


# confere que nenhuma aresta liga dois vertices da mesma cor
def coloracaoValida(vizinhos, cor):
    return all(cor[v] != cor[w] for v in range(len(vizinhos))
               for w in vizinhos[v])


# opcao m: imprime a coloracao de Welsh-Powell e o limite pela clique
def showColoracao(g):
    (vizinhos, pesos) = subjacente(g)
    cor = coloracaoWelshPowell(vizinhos)
    clique = cliqueGulosa(vizinhos)
    k = max(cor, default=-1) + 1
    print("\n-------------- COLORACAO DE VERTICES (WELSH-POWELL) --------------")
    print(f"Grafo nao orientado subjacente: {g.n} vertices, {len(pesos)} arestas")
    print(f"Numero de cores usadas: {k}")
    print(f"Limite inferior (clique encontrada): {len(clique)}")
    if k == len(clique):
        print(f"=> o numero cromatico e exatamente {k}.")
    else:
        print(f"=> o numero cromatico esta entre {len(clique)} e {k}.")
    print(f"Coloracao valida (nenhum vizinho com a mesma cor): "
          f"{'SIM' if coloracaoValida(vizinhos, cor) else 'NAO'}")
    print("\nClasses de cor (estacoes sem ligacao direta entre si):")
    for c in range(k):
        membros = [v for v in range(g.n) if cor[v] == c]
        print(f"  cor {c + 1:2d} ({len(membros):2d} estacoes): "
              + ", ".join(str(v) for v in membros))
    print("-------------------------------------------------------------------\n")
    return (cor, clique)


# busca em profundidade com low-link a partir de v (pai = vertice de onde veio):
# v e articulacao se remove-lo aumenta o numero de componentes; a aresta {v,w}
# e ponte se remove-la o faz
def dfsLowLink(v, pai, vizinhos, desc, low, tempo, articulacoes, pontes):
    desc[v] = low[v] = tempo[0]
    tempo[0] += 1
    filhos = 0
    for w in sorted(vizinhos[v]):
        if w == pai:
            continue
        if desc[w] != -1:
            low[v] = min(low[v], desc[w])
        else:
            filhos += 1
            dfsLowLink(w, v, vizinhos, desc, low, tempo, articulacoes, pontes)
            low[v] = min(low[v], low[w])
            if low[w] > desc[v]:
                pontes.append((min(v, w), max(v, w)))
            if pai != -1 and low[w] >= desc[v]:
                articulacoes.add(v)
    if pai == -1 and filhos > 1:
        articulacoes.add(v)


# pontos de articulacao e pontes do grafo nao orientado dado pelos vizinhos
def articulacoesEPontes(vizinhos):
    n = len(vizinhos)
    desc = [-1] * n
    low = [0] * n
    articulacoes = set()
    pontes = []
    tempo = [0]
    sys.setrecursionlimit(max(1000, 3 * n + 100))
    for v in range(n):
        if desc[v] == -1:
            dfsLowLink(v, -1, vizinhos, desc, low, tempo, articulacoes, pontes)
    return (sorted(articulacoes), sorted(pontes))


# opcao n: imprime os pontos de articulacao e as pontes
def showArticulacao(g):
    (vizinhos, pesos) = subjacente(g)
    (artic, pontes) = articulacoesEPontes(vizinhos)
    base = len(componentesConexas(vizinhos))
    print("\n------------- PONTOS DE ARTICULACAO E PONTES -------------")
    print(f"Grafo nao orientado subjacente: {g.n} vertices, {len(pesos)} arestas,"
          f" {base} componente(s)")
    print(f"\nPontos de articulacao: {len(artic)}"
          " (se a estacao sair do ar, a rede se parte)")
    for v in artic:
        pedacos = componentesConexas(vizinhos, proibidos=(v,))
        tamanhos = sorted(len(c) for c in pedacos)
        print(f"  {rotuloCurto(g, v)}")
        print(f"      sem ela a rede tem {len(pedacos)} componentes, "
              f"tamanhos {tamanhos}")
    print(f"\nPontes: {len(pontes)} (ligacoes cuja perda parte a rede)")
    for (a, b) in pontes:
        print(f"  {rotuloCurto(g, a)}  --  {rotuloCurto(g, b)}"
              f"  ({pesos[(a, b)]:g} km)")
    print("----------------------------------------------------------\n")
    return (artic, pontes)


# raiz do conjunto de x na estrutura union-find (pai[x] = pai de x)
def raizDe(pai, x):
    while pai[x] != x:
        pai[x] = pai[pai[x]]
        x = pai[x]
    return x


# Kruskal com union-find; se o grafo e desconexo devolve uma floresta
def kruskal(n, pesos):
    pai = list(range(n))
    escolhidas = []
    total = 0.0
    for ((a, b), peso) in sorted(pesos.items(), key=lambda it: (it[1], it[0])):
        ra, rb = raizDe(pai, a), raizDe(pai, b)
        if ra != rb:
            pai[ra] = rb
            escolhidas.append((a, b, peso))
            total += peso
    return (escolhidas, total)


# opcao o: imprime a arvore geradora minima (Kruskal)
def showArvoreGeradora(g):
    (vizinhos, pesos) = subjacente(g)
    (arestas, total) = kruskal(g.n, pesos)
    comps = len(componentesConexas(vizinhos))
    print("\n------------ ARVORE GERADORA MINIMA (KRUSKAL) ------------")
    print(f"Grafo nao orientado subjacente: {g.n} vertices, {len(pesos)} arestas"
          f" (peso = menor distancia entre os dois sentidos)")
    print(f"Componentes: {comps}"
          f"{' (resultado e uma floresta geradora minima)' if comps > 1 else ''}")
    print(f"Arestas escolhidas: {len(arestas)} (= vertices - componentes)")
    print(f"Peso total: {total:.1f} km")
    soma = sum(pesos.values())
    print(f"Todas as arestas somam {soma:.1f} km; a arvore usa "
          f"{100 * total / soma:.1f}% disso.")
    print("\nOs 10 maiores trechos da arvore (ligacoes mais longas "
          "indispensaveis):")
    for (a, b, peso) in sorted(arestas, key=lambda e: -e[2])[:10]:
        print(f"  {peso:6.1f} km  {rotuloCurto(g, a)}  --  {rotuloCurto(g, b)}")
    print("----------------------------------------------------------\n")
    return (arestas, total)
