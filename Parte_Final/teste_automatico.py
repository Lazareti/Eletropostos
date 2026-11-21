"""
Teoria dos Grafos - Projeto Parte 2 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Testes automaticos: FCONEX no exemplo G1 dos slides, categorias
C3/C1/C0, insercao/remocao, round-trip, conexidade dos arquivos reais
e Dijkstra com autonomia (brinquedo, validacao cruzada com Floyd-Warshall).

"""

import os
from grafoListaPonderado import Grafo
from conexidade import fconex, classificaConexidade, grafoReduzido
from caracteristicas import (subgrafo, estatisticasGraus, analisaEuler,
                             subjacente, coloracaoWelshPowell, coloracaoValida,
                             cliqueGulosa, articulacoesEPontes, kruskal)
from estudo_caso import (lerMatriz, postosNovos, rotaComPostosNovos,
                         ligacaoDeComponentes, ROTAS)
from algoritmos import (dijkstra, reconstroiCaminho, autonomiaMinima,
                        buscaVertices, INFINITO)


def grafoG1():
    g = Grafo(8)
    for (v, w) in [(0, 1), (0, 2), (1, 3), (1, 5), (2, 3), (3, 2),
                   (4, 0), (4, 1), (5, 4), (6, 4), (6, 7), (7, 5),
                   (7, 6)]:
        g.insereA(v, w, 1.0)
    return g


def teste(nome, condicao):
    print(f"  [{'OK' if condicao else 'FALHOU'}] {nome}")
    return condicao


# distancias minimas entre todos os pares (Floyd-Warshall) usando apenas
# arcos com peso <= autonomia; serve para conferir o Dijkstra
def floydWarshall(g, autonomia):
    d = [[INFINITO] * g.n for i in range(g.n)]
    for v in range(g.n):
        d[v][v] = 0.0
        for (w, peso) in g.listaAdj[v]:
            if peso <= autonomia:
                d[v][w] = min(d[v][w], peso)
    for k in range(g.n):
        for i in range(g.n):
            for j in range(g.n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def main():
    ok = True

    print("== 1) FCONEX no exemplo G1 dos slides ==")
    g = grafoG1()
    particao = fconex(g)
    esperado = [{0, 1, 4, 5}, {2, 3}, {6, 7}]
    ok &= teste("particao de G1 = {1,2,5,6},{3,4},{7,8} (1-based)",
                sorted(sorted(p) for p in particao) ==
                sorted(sorted(p) for p in esperado))
    ok &= teste("G1 e C2 (sf-conexo, nao f-conexo)",
                classificaConexidade(g, particao) == "C2")
    (comps, arcos) = grafoReduzido(g, particao)
    ok &= teste("grafo reduzido de G1 tem 3 vertices", len(comps) == 3)
    ok &= teste("reduzido de G1: arcos S1->S2 e S3->S1",
                arcos == [(0, 1), (2, 0)])

    print("== 2) Classificacao C3/C1/C0 em grafos de brinquedo ==")
    g3 = Grafo(3)
    g3.insereA(0, 1, 1.0); g3.insereA(1, 2, 1.0); g3.insereA(2, 0, 1.0)
    ok &= teste("ciclo orientado e C3",
                classificaConexidade(g3, fconex(g3)) == "C3")
    g1 = Grafo(3)
    g1.insereA(0, 1, 1.0); g1.insereA(0, 2, 1.0)
    ok &= teste("grafo em 'V' e C1",
                classificaConexidade(g1, fconex(g1)) == "C1")
    g0 = Grafo(4)
    g0.insereA(0, 1, 1.0); g0.insereA(2, 3, 1.0)
    ok &= teste("dois pares isolados e C0",
                classificaConexidade(g0, fconex(g0)) == "C0")

    print("== 3) Insercao/remocao de vertices e arcos ==")
    g = Grafo(0)
    g.insereV("A"); g.insereV("B"); g.insereV("C")
    g.insereA(0, 1, 10.0); g.insereA(1, 2, 20.0); g.insereA(2, 0, 30.0)
    ok &= teste("3 vertices e 3 arcos inseridos", g.n == 3 and g.m == 3)
    g.insereA(0, 1, 99.0)
    ok &= teste("inserir arco repetido atualiza o peso",
                g.m == 3 and g.listaAdj[0][0] == (1, 99.0))
    g.removeA(2, 0)
    ok &= teste("remocao de arco", g.m == 2 and not g.existeA(2, 0))
    g.removeV(0)
    ok &= teste("remocao de vertice com renumeracao",
                g.n == 2 and g.rotulos == ["B", "C"] and
                g.listaAdj[0] == [(1, 20.0)])
    ok &= teste("contagem de arcos apos removeV", g.m == 1)

    print("== 4) Round-trip ler/gravar grafo.txt ==")
    g = Grafo(0)
    g.lerArquivo(os.path.join("dados", "grafo_pequeno.txt"))
    g.gravarArquivo(os.path.join("dados", "tmp_roundtrip.txt"))
    g2 = Grafo(0)
    g2.lerArquivo(os.path.join("dados", "tmp_roundtrip.txt"))
    ok &= teste("mesmo n e m apos round-trip",
                g.n == g2.n and g.m == g2.m)
    ok &= teste("mesmas listas de adjacencia apos round-trip",
                g.listaAdj == g2.listaAdj and g.rotulos == g2.rotulos)
    os.remove(os.path.join("dados", "tmp_roundtrip.txt"))

    print("== 5) Conexidade dos arquivos reais da base ==")
    # mesmo a 250 km a base do OSM tem um componente separado de 4
    # estacoes no norte do PR -> mestre tambem e C0; C3 aparece no
    # grafo_pequeno (regiao de Curitiba)
    for nome, esperado in (("grafo_pequeno.txt", "C3"),
                           ("grafo.txt", "C0")):
        g = Grafo(0)
        g.lerArquivo(os.path.join("dados", nome))
        cat = classificaConexidade(g, fconex(g))
        ok &= teste(f"{nome}: {g.n} vertices, {g.m} arcos, {cat}",
                    cat == esperado)

    print("== 6) Dijkstra com autonomia em grafo de brinquedo ==")
    # 0 -> 1 (60), 1 -> 2 (60), 0 -> 2 (150), 2 -> 3 (40); 3 e isolado de volta
    gd = Grafo(4)
    gd.insereA(0, 1, 60.0); gd.insereA(1, 2, 60.0)
    gd.insereA(0, 2, 150.0); gd.insereA(2, 3, 40.0)
    (dist, pred) = dijkstra(gd, 0, 200)
    ok &= teste("autonomia 200: 0->2 pelo caminho 0-1-2 (120 km)",
                dist[2] == 120.0 and
                reconstroiCaminho(pred, 0, 2) == [0, 1, 2])
    (dist, pred) = dijkstra(gd, 0, 100)
    ok &= teste("autonomia 100: arco de 150 km e proibido, 0->3 = 160 km",
                dist[3] == 160.0 and
                reconstroiCaminho(pred, 0, 3) == [0, 1, 2, 3])
    (dist, pred) = dijkstra(gd, 0, 50)
    ok &= teste("autonomia 50: sem rota (lista vazia, distancia infinita)",
                dist[1] == INFINITO and
                reconstroiCaminho(pred, 0, 1) == [])
    (dist, pred) = dijkstra(gd, 3, 200)
    ok &= teste("grafo orientado: 3 nao alcanca 0 (so existe 2 -> 3)",
                dist[0] == INFINITO)
    ok &= teste("autonomia minima 0->3 = 60 km (gargalo do melhor caminho)",
                autonomiaMinima(gd, 0, 3) == 60.0)
    ok &= teste("autonomia minima 3->0 = None (sem rota nenhuma)",
                autonomiaMinima(gd, 3, 0) is None)

    print("== 7) Dijkstra no grafo real (grafo.txt direcional) ==")
    g = Grafo(0)
    g.lerArquivo(os.path.join("dados", "grafo.txt"))
    assimetricos = sum(1 for v in range(g.n) for (w, p) in g.listaAdj[v]
                       if not any(x == v and q == p for (x, q) in g.listaAdj[w]))
    ok &= teste(f"grafo.txt e direcional ({assimetricos} arcos sem volta de "
                f"mesmo peso)", assimetricos > 1000)
    for A in (100, 150, 250):
        d = floydWarshall(g, A)
        iguais = True
        for origem in range(0, g.n, 7):
            (dist, pred) = dijkstra(g, origem, A)
            for destino in range(g.n):
                if abs(dist[destino] - d[origem][destino]) > 1e-6 and \
                        not (dist[destino] == INFINITO and
                             d[origem][destino] == INFINITO):
                    iguais = False
        ok &= teste(f"autonomia {A} km: Dijkstra = Floyd-Warshall "
                    f"(origens 0,7,14,...)", iguais)
    ok &= teste("rota Curitiba(3) -> Foz(14) com 250 km = 685,6 km",
                abs(dijkstra(g, 3, 250)[0][14] - 685.6) < 0.05)
    ok &= teste("rota Curitiba(3) -> Foz(14) com 200 km nao existe",
                dijkstra(g, 3, 200)[0][14] == INFINITO)
    ok &= teste("autonomia minima Curitiba(3) -> Foz(14) = 208,4 km",
                autonomiaMinima(g, 3, 14) == 208.4)
    ok &= teste("Apucarana(0) -> Curitiba(3): sem rota nem com todos os arcos",
                autonomiaMinima(g, 0, 3) is None)
    ok &= teste("busca de estacao sem acento: 'florianopolis' acha 2",
                len(buscaVertices(g, "florianopolis")) == 2)

    print("== 8) Caracteristicas: graus, Euler, coloracao, articulacao, AGM ==")
    tri = Grafo(3)  # ciclo orientado 0->1->2->0
    tri.insereA(0, 1, 1.0); tri.insereA(1, 2, 1.0); tri.insereA(2, 0, 1.0)
    r = analisaEuler(tri)
    ok &= teste("ciclo orientado de 3 vertices: tem ciclo euleriano",
                r["ciclo"] and r["trilha"])
    cam = Grafo(3)  # caminho 0->1->2
    cam.insereA(0, 1, 1.0); cam.insereA(1, 2, 1.0)
    r = analisaEuler(cam)
    ok &= teste("caminho 0->1->2: tem trilha euleriana, mas nao ciclo",
                r["trilha"] and not r["ciclo"])
    est = Grafo(4)  # estrela orientada saindo de 0: nao tem trilha
    est.insereA(0, 1, 1.0); est.insereA(0, 2, 1.0); est.insereA(0, 3, 1.0)
    ok &= teste("estrela saindo de 0: nao e euleriano",
                not analisaEuler(est)["trilha"])
    (viz, pes) = subjacente(tri)
    cor = coloracaoWelshPowell(viz)
    ok &= teste("triangulo precisa de 3 cores (clique = 3)",
                max(cor) + 1 == 3 and len(cliqueGulosa(viz)) == 3 and
                coloracaoValida(viz, cor))
    ciclo4 = Grafo(4)
    for (a, b) in ((0, 1), (1, 2), (2, 3), (3, 0)):
        ciclo4.insereA(a, b, 1.0)
    (viz4, pes4) = subjacente(ciclo4)
    ok &= teste("ciclo de 4 vertices e bipartido: 2 cores",
                max(coloracaoWelshPowell(viz4)) + 1 == 2)
    ok &= teste("triangulo: sem articulacao e sem ponte",
                articulacoesEPontes(viz) == ([], []))
    (viz3, pes3) = subjacente(cam)
    ok &= teste("caminho 0-1-2: articulacao {1}; pontes (0,1) e (1,2)",
                articulacoesEPontes(viz3) == ([1], [(0, 1), (1, 2)]))
    pg = Grafo(4)  # AGM: pesos 1, 2, 3, 10 -> arvore usa 1+2+3 = 6
    pg.insereA(0, 1, 1.0); pg.insereA(1, 2, 2.0); pg.insereA(2, 3, 3.0)
    pg.insereA(0, 3, 10.0); pg.insereA(0, 2, 5.0)
    (v4, p4) = subjacente(pg)
    (arv, total) = kruskal(4, p4)
    ok &= teste("Kruskal: 3 arestas, peso total 6", len(arv) == 3 and total == 6.0)
    g = Grafo(0)
    g.lerArquivo(os.path.join("dados", "grafo.txt"))
    e = estatisticasGraus(g)
    ok &= teste("grafo.txt: soma dos graus de saida = soma dos de entrada = m",
                sum(e["saida"]) == g.m == sum(e["entrada"]))
    ok &= teste("grafo.txt: 6 vertices com entrada != saida, nao euleriano",
                len(analisaEuler(g)["desbalanceados"]) == 6 and
                not analisaEuler(g)["trilha"])
    (viz, pes) = subjacente(g)
    cor = coloracaoWelshPowell(viz)
    ok &= teste("grafo.txt: coloracao valida com 25 cores (= clique 25)",
                coloracaoValida(viz, cor) and max(cor) + 1 == 25 and
                len(cliqueGulosa(viz)) == 25)
    (artic, pontes) = articulacoesEPontes(viz)
    ok &= teste("grafo.txt: 5 articulacoes e 4 pontes",
                len(artic) == 5 and len(pontes) == 4)
    (arv, total) = kruskal(g.n, pes)
    ok &= teste("grafo.txt: floresta com 83 arestas e 4347 km",
                len(arv) == 83 and abs(total - 4347.0) < 0.05)
    h = subgrafo(g, 100)
    ok &= teste("subgrafo(100): so arcos <= 100 km e menos arcos que o original",
                h.n == g.n and h.m < g.m and
                all(p <= 100 for v in range(h.n) for (w, p) in h.listaAdj[v]))

    print("== 9) Estudo de caso: postos novos necessarios ==")
    ok &= teste("trecho de 100 km com A = 100: 0 postos novos",
                postosNovos(100.0, 100) == 0)
    ok &= teste("trecho de 100,1 km com A = 100: 1 posto novo",
                postosNovos(100.1, 100) == 1)
    ok &= teste("trecho de 250 km com A = 100: 2 postos novos",
                postosNovos(250.0, 100) == 2)
    # matriz de brinquedo: 0 -> 2 direto = 300 km; 0 -> 1 = 120, 1 -> 2 = 120
    inf = INFINITO
    Mb = [[0, 120, 300], [120, 0, 120], [300, 120, 0]]
    (cam, novos, km, trechos) = rotaComPostosNovos(Mb, 0, 2, 100)
    ok &= teste("A = 100: melhor caminho 0-1-2 (1+1 postos) ou direto (2); "
                "escolhe o de menos postos e menos km",
                novos == 2 and km == 240.0 and cam == [0, 1, 2])
    (cam, novos, km, trechos) = rotaComPostosNovos(Mb, 0, 2, 150)
    ok &= teste("A = 150: 0-1-2 nao precisa de posto novo",
                novos == 0 and km == 240.0)
    g = Grafo(0)
    g.lerArquivo(os.path.join("dados", "grafo.txt"))
    M = lerMatriz(os.path.join("dados", "matriz_direcional.csv"))
    ok &= teste("matriz 85 x 85 e coerente com o grafo.txt (arcos <= 250)",
                len(M) == 85 and len(M[0]) == 85 and
                all(M[v][w] == p for v in range(g.n)
                    for (w, p) in g.listaAdj[v]))
    iguais = True
    for (o, d) in ROTAS:
        (cam, novos, km, trechos) = rotaComPostosNovos(M, o, d, 250)
        dist = dijkstra(g, o, 250)[0][d]
        if novos != 0 or abs(km - dist) > 0.05:
            iguais = False
    ok &= teste("A = 250: 0 postos novos e mesma distancia do Dijkstra "
                "nas 4 rotas do estudo", iguais)
    ok &= teste("Curitiba -> Florianopolis com A = 100: 2 postos novos",
                rotaComPostosNovos(M, 3, 68, 100)[1] == 2)
    ok &= teste("rede inteira: 2 componentes a 250 km -> 1 posto novo",
                ligacaoDeComponentes(g, M, 250)[2] == 1)

    print("\nRESULTADO GERAL:", "TUDO OK" if ok else "HA FALHAS")


if __name__ == "__main__":
    main()
