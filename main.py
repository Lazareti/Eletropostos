"""
Teoria dos Grafos - Projeto Parte 2 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Aplicacao principal: menu de opcoes (a-j) sobre o grafo de eletropostos.

"""

from grafoListaPonderado import Grafo
from conexidade import showConexidade

ARQ_PADRAO = "dados/grafo.txt"


# opcao g: exibe o conteudo do grafo.txt na tela, com paginacao
def mostrarConteudoArquivo(nomeArq):
    try:
        with open(nomeArq, "r", encoding="utf-8") as arq:
            linhas = arq.read().splitlines()
    except FileNotFoundError:
        print(f"\nArquivo '{nomeArq}' nao encontrado.")
        return
    tipo = int(linhas[0])
    n = int(linhas[1])
    m = int(linhas[2 + n])
    print("\n=============== CONTEUDO DO ARQUIVO ===============")
    print(f"Arquivo: {nomeArq}")
    print(f"Tipo do grafo: {tipo} (orientado com peso na aresta)")
    print(f"Vertices: {n}   Arcos: {m}")
    print("\n--- Vertices (id - rotulo) ---")
    for i in range(n):
        print(f"  {linhas[2 + i]}")
    print("--- Arcos (origem -> destino, peso em km) ---")
    for i in range(m):
        v, w, p = linhas[3 + n + i].split()
        print(f"  {int(v):3d} -> {int(w):3d}   {float(p):7.1f} km", end="")
        if (i + 1) % 40 == 0 and i + 1 < m:
            resp = input(f"\n  ... {i + 1}/{m} arcos (Enter = continuar, s = sair) ")
            if resp.strip().lower() == "s":
                break
    print("\n===================================================\n")


# imprime o menu de opcoes
def mostrarMenu():
    print("=========================================================")
    print("  REDE DE ELETROPOSTOS DA REGIAO SUL")
    print("=========================================================")
    print("  a) Ler dados do arquivo grafo.txt")
    print("  b) Gravar dados no arquivo grafo.txt")
    print("  c) Inserir vertice")
    print("  d) Inserir aresta")
    print("  e) Remover vertice")
    print("  f) Remover aresta")
    print("  g) Mostrar conteudo do arquivo")
    print("  h) Mostrar grafo (lista de adjacencia)")
    print("  i) Conexidade do grafo e grafo reduzido")
    print("  j) Encerrar a aplicacao")
    print("=========================================================")


# loop principal do menu (opcoes a-j)
def main():
    g = Grafo(0)
    arqAtual = ARQ_PADRAO
    arqTentado = arqAtual
    while True:
        mostrarMenu()
        op = input("Opcao: ").strip().lower()
        try:
            if op == "a":
                nome = input(f"Arquivo [{arqAtual}]: ").strip() or arqAtual
                arqTentado = nome
                g.lerArquivo(nome)
                arqAtual = nome
                print(f"Grafo lido: {g.n} vertices, {g.m} arcos.")
            elif op == "b":
                nome = input(f"Arquivo [{arqAtual}]: ").strip() or arqAtual
                arqTentado = nome
                g.gravarArquivo(nome)
                print(f"Grafo gravado em '{nome}'.")
            elif op == "c":
                rotulo = input("Rotulo do novo vertice: ").strip()
                novo = g.insereV(rotulo)
                print(f"Vertice {novo} ('{rotulo}') inserido.")
            elif op == "d":
                v = int(input("Vertice de origem: "))
                w = int(input("Vertice de destino: "))
                peso = float(input("Peso (distancia em km): "))
                if 0 <= v < g.n and 0 <= w < g.n and v != w:
                    g.insereA(v, w, peso)
                    print(f"Arco {v} -> {w} ({peso:g} km) inserido.")
                else:
                    print("Vertices invalidos.")
            elif op == "e":
                v = int(input("Vertice a remover: "))
                if 0 <= v < g.n:
                    rotulo = g.rotulos[v]
                    g.removeV(v)
                    print(f"Vertice {v} ('{rotulo}') removido, junto com "
                          f"seus arcos. Vertices renumerados.")
                else:
                    print("Vertice invalido.")
            elif op == "f":
                v = int(input("Vertice de origem: "))
                w = int(input("Vertice de destino: "))
                if 0 <= v < g.n and 0 <= w < g.n:
                    if g.removeA(v, w):
                        print(f"Arco {v} -> {w} removido.")
                    else:
                        print("Arco inexistente.")
                else:
                    print("Vertices invalidos.")
            elif op == "g":
                mostrarConteudoArquivo(arqAtual)
            elif op == "h":
                if g.n <= 30:
                    g.show()
                else:
                    g.showMin()
                    print("(grafo grande: impressao compacta, sem os rotulos)")
            elif op == "i":
                showConexidade(g)
            elif op == "j":
                print("Encerrando a aplicacao. Ate logo!")
                break
            else:
                print("Opcao invalida.")
        except FileNotFoundError:
            print(f"Arquivo '{arqTentado}' nao encontrado. "
                  f"Use a opcao (a) com um caminho valido.")
        except (ValueError, IndexError) as erro:
            print(f"Entrada invalida: {erro}")


if __name__ == "__main__":
    main()
