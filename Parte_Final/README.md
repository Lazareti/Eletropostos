# Rede de Eletropostos da Região Sul

Projeto da disciplina de Teoria dos Grafos, Universidade Presbiteriana Mackenzie, curso de Ciência da Computação. Professor: Dr. Ivan Carlos Alcântara de Oliveira.

Integrantes:

- João Rocha Murgel, RA 10410293
- Fellipe Jardanovski, RA 10395847
- Gabriel Lazareti Cardoso, RA 10417353

## O projeto

A rede de estações de recarga para veículos elétricos da Região Sul é modelada como um grafo orientado com peso nos arcos (tipo 6). Os vértices são 85 estações do OpenStreetMap, e os 1.640 arcos são trajetos rodoviários de até 250 km, com a distância calculada pelo OSRM em cada sentido.

A aplicação em Python lê, grava e edita o grafo, classifica a conexidade (FCONEX e grafo reduzido), calcula a rota de menor distância para a autonomia que o usuário informa (Dijkstra) e analisa a rede com graus, grafo euleriano, coloração, pontos de articulação e pontes, e árvore geradora mínima.

## Como usar

Basta o Python 3, sem bibliotecas externas:

```
python3 main.py
```

O menu tem as opções:

- a) Ler dados do arquivo grafo.txt
- b) Gravar dados no arquivo grafo.txt
- c) Inserir vértice
- d) Inserir aresta
- e) Remover vértice
- f) Remover aresta
- g) Mostrar conteúdo do arquivo
- h) Mostrar grafo
- i) Conexidade do grafo e grafo reduzido
- j) Rota com restrição de autonomia (Dijkstra)
- k) Graus dos vértices
- l) Grafo euleriano
- m) Coloração de vértices
- n) Pontos de articulação e pontes
- o) Árvore geradora mínima
- p) Encerrar a aplicação

Para ver a rota, use a opção `a` para ler o grafo e depois a `j`, informando origem, destino e autonomia. Exemplo: origem 28 (Caxias do Sul), destino 55 (São Francisco de Paula), autonomia 250 e depois 100.

Outros comandos:

```
python3 teste_automatico.py   # testes automáticos
python3 estudo_caso.py        # tabelas do estudo de caso (grava dados/estudo_caso.md)
```

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `main.py` | menu e título da aplicação |
| `grafoListaPonderado.py` | classe `Grafo` (lista de adjacência com peso), derivada da classe vista em aula |
| `conexidade.py` | FCONEX, categorias C3 a C0 e grafo reduzido |
| `algoritmos.py` | Dijkstra com autonomia |
| `caracteristicas.py` | graus, Euler, coloração, articulação e pontes, árvore geradora mínima |
| `estudo_caso.py` | rotas por autonomia e estimativa de postos novos |
| `teste_automatico.py` | testes automáticos |

## Dados

| Arquivo | Conteúdo |
|---|---|
| `dados/grafo.txt` | grafo oficial: tipo 6, 85 vértices e 1.640 arcos, com a distância de cada sentido |
| `dados/grafo_pequeno.txt` | grafo de teste com 10 estações de Curitiba (fortemente conexo), usado nos testes automáticos |
| `dados/matriz_direcional.csv` | distância rodoviária entre todos os pares de estações, em km |
| `dados/estudo_caso.md` | resultado do estudo de caso |

## Relatório, apresentação e vídeo

- Relatório: `Relatorio_TG_Eletropostos_Sul_Parte3.pdf`
- Apresentação: `Apresentacao_TG_Eletropostos_Parte3.pptx`
- Vídeo: [inserir o link do vídeo no YouTube]
