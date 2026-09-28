"""
Teoria dos Grafos - Projeto Parte 2 - Rede de Eletropostos da Regiao Sul
Fellipe Jardanovski (10395847), Gabriel Lazareti Cardoso (10417353),
Joao Rocha Murgel (10410293)

Conexidade de grafo orientado: FCONEX (componentes f-conexas),
categoria C3/C2/C1/C0 e grafo reduzido.

"""


# vertices alcancados em um passo saindo do conjunto S
def sucessores(g, S):
    viz = set()
    for v in S:
        for (w, peso) in g.listaAdj[v]:
            viz.add(w)
    return viz


# vertices que chegam no conjunto S em um passo
def predecessores(g, S):
    viz = set()
    for v in range(g.n):
        for (w, peso) in g.listaAdj[v]:
            if w in S:
                viz.add(v)
                break
    return viz


# fecho transitivo direto R+ de v
def fechoDireto(g, v):
    R = {v}
    while True:
        W = sucessores(g, R) - R
        if not W:
            break
        R = R | W
    return R


# fecho transitivo inverso R- de v
def fechoInverso(g, v):
    R = {v}
    while True:
        W = predecessores(g, R) - R
        if not W:
            break
        R = R | W
    return R


# FCONEX: particiona o grafo em componentes f-conexas
def fconex(g):
    V = set(range(g.n))
    particao = []
    while V:
        s0 = min(V)
        W = fechoDireto(g, s0) & fechoInverso(g, s0)
        particao.append(W)
        V = V - W
    return particao


# classifica a conexidade do grafo em C3, C2, C1 ou C0
def classificaConexidade(g, particao):
    if g.n == 0:
        return "C0"
    if len(particao) == 1:
        return "C3"
    fechos = [fechoDireto(g, x) for x in range(g.n)]
    sfConexo = True
    for x in range(g.n):
        for y in range(x + 1, g.n):
            if (x not in fechos[y]) and (y not in fechos[x]):
                sfConexo = False
                break
        if not sfConexo:
            break
    if sfConexo:
        return "C2"
    alcancados = {0}
    fronteira = [0]
    while fronteira:
        v = fronteira.pop()
        vizinhos = set(w for (w, p) in g.listaAdj[v]) | predecessores(g, {v})
        for w in vizinhos:
            if w not in alcancados:
                alcancados.add(w)
                fronteira.append(w)
    if len(alcancados) == g.n:
        return "C1"
    return "C0"


# monta o grafo reduzido: um vertice para cada componente
def grafoReduzido(g, particao):
    compDe = {}
    componentes = []
    for i in range(len(particao)):
        componentes.append(sorted(particao[i]))
        for v in particao[i]:
            compDe[v] = i
    arcos = set()
    for v in range(g.n):
        for (w, peso) in g.listaAdj[v]:
            if compDe[v] != compDe[w]:
                arcos.add((compDe[v], compDe[w]))
    return (componentes, sorted(arcos))


# opcao i: imprime componentes, categoria e grafo reduzido
def showConexidade(g):
    particao = fconex(g)
    categoria = classificaConexidade(g, particao)
    (componentes, arcos) = grafoReduzido(g, particao)
    descricao = {"C3": "fortemente conexo (f-conexo)",
                 "C2": "semi-fortemente conexo (sf-conexo)",
                 "C1": "simplesmente conexo (s-conexo)",
                 "C0": "desconexo"}
    print("\n---------------- CONEXIDADE DO GRAFO ----------------")
    print(f"Componentes fortemente conexas (FCONEX): {len(componentes)}")
    for i in range(len(componentes)):
        rot = ", ".join(f"{v}:{g.rotulos[v]}" for v in componentes[i])
        print(f"  S{i + 1} = {{ {rot} }}")
    print(f"\nCategoria de conexidade: {categoria} ({descricao[categoria]})")
    print("\n--------------------- GRAFO REDUZIDO --------------------")
    print(f"Vertices do reduzido: {len(componentes)} (um por componente)")
    if len(arcos) == 0:
        print("Arcos do reduzido: nenhum")
    else:
        print("Arcos do reduzido:")
        for (si, sj) in arcos:
            print(f"  S{si + 1} -> S{sj + 1}")
    print("---------------------------------------------------------\n")
    return categoria
