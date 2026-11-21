"""
Teoria dos Grafos - Projeto Parte 3 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Algoritmos sobre o grafo orientado com peso (tipo 6): caminho minimo de
Dijkstra com restricao de autonomia (rota entre duas estacoes em que
nenhum trecho entre recargas ultrapassa A km).

"""

import heapq
import unicodedata

INFINITO = float("inf")


# Dijkstra a partir de 'origem', usando apenas arcos com peso <= autonomia.
# Retorna (dist, pred): dist[v] = menor distancia ate v (INFINITO se v nao
# e alcancavel) e pred[v] = vertice anterior no caminho minimo.
def dijkstra(g, origem, autonomia):
    dist = [INFINITO] * g.n
    pred = [-1] * g.n
    dist[origem] = 0.0
    fila = [(0.0, origem)]  # heap de pares (distancia, vertice)
    while fila:
        (d, v) = heapq.heappop(fila)
        if d > dist[v]:  # entrada antiga: v ja foi fechado com distancia menor
            continue
        for (w, peso) in g.listaAdj[v]:
            if peso > autonomia:  # trecho maior que a autonomia: arco proibido
                continue
            if d + peso < dist[w]:  # relaxamento do arco v -> w
                dist[w] = d + peso
                pred[w] = v
                heapq.heappush(fila, (dist[w], w))
    return (dist, pred)


# reconstroi a sequencia de vertices origem -> destino a partir de pred;
# retorna lista vazia se o destino nao foi alcancado
def reconstroiCaminho(pred, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        anterior = pred[caminho[-1]]
        if anterior == -1:
            return []
        caminho.append(anterior)
    caminho.reverse()
    return caminho


# menor autonomia (km) que torna a rota possivel, ou None se nao existe
# rota nem usando todos os arcos. Busca binaria sobre os pesos distintos
# dos arcos: a rota existe se e somente se A >= esse valor (gargalo).
def autonomiaMinima(g, origem, destino):
    pesos = sorted(set(p for v in range(g.n) for (w, p) in g.listaAdj[v]))
    if not pesos:
        return None
    (dist, pred) = dijkstra(g, origem, pesos[-1])
    if dist[destino] == INFINITO:
        return None
    ini, fim = 0, len(pesos) - 1
    while ini < fim:
        meio = (ini + fim) // 2
        (dist, pred) = dijkstra(g, origem, pesos[meio])
        if dist[destino] == INFINITO:
            ini = meio + 1
        else:
            fim = meio
    return pesos[ini]


# remove acentos e maiusculas, para a busca de estacao por texto
def normaliza(texto):
    sem = unicodedata.normalize("NFD", texto)
    return "".join(c for c in sem if unicodedata.category(c) != "Mn").lower()


# lista os vertices cujo rotulo contem o texto (sem acento/maiuscula)
def buscaVertices(g, texto):
    chave = normaliza(texto)
    return [v for v in range(g.n) if chave in normaliza(g.rotulos[v])]


# opcao j: imprime a rota de menor distancia respeitando a autonomia
def showRota(g, origem, destino, autonomia):
    print("\n------------ ROTA COM RESTRICAO DE AUTONOMIA ------------")
    print(f"Origem : {origem} - {g.rotulos[origem]}")
    print(f"Destino: {destino} - {g.rotulos[destino]}")
    print(f"Autonomia: {autonomia:g} km (maior trecho permitido entre recargas)")
    (dist, pred) = dijkstra(g, origem, autonomia)
    caminho = reconstroiCaminho(pred, origem, destino)
    if not caminho:
        print("\nNao existe rota com essa autonomia.")
        minima = autonomiaMinima(g, origem, destino)
        if minima is None:
            print("Nao ha rota entre as duas estacoes nem usando todos os "
                  "arcos do grafo (estacoes em partes desconectadas da rede).")
        else:
            print(f"Autonomia minima que viabiliza a rota: {minima:g} km.")
        print("---------------------------------------------------------\n")
        return None
    print(f"\nDistancia total: {dist[destino]:.1f} km")
    print(f"Estacoes no percurso: {len(caminho)}   "
          f"Paradas intermediarias para recarga: {max(len(caminho) - 2, 0)}")
    print("\nPercurso:")
    for i in range(len(caminho)):
        v = caminho[i]
        if i == 0:
            print(f"  {v:3d}  {g.rotulos[v]}   (partida)")
        else:
            trecho = dist[v] - dist[caminho[i - 1]]
            marca = "(chegada)" if i == len(caminho) - 1 else "(recarga)"
            print(f"  {v:3d}  {g.rotulos[v]}   +{trecho:.1f} km {marca}")
    print("---------------------------------------------------------\n")
    return caminho
