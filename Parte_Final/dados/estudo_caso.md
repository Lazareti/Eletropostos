# Estudo de caso - rotas, autonomia e vaos de cobertura

Dados: grafo.txt (85 estacoes, 1.640 arcos <= 250 km, pesos por sentido) e matriz_direcional.csv (distancia rodoviaria de todos os pares, OSRM).

## 1. Rotas por autonomia na rede atual (Dijkstra)

| Rota | A = 100 km | A = 150 km | A = 200 km | A = 250 km |
|---|---|---|---|---|
| Curitiba (Curitiba Eco Elétrico) -> Florianópolis (UFSC) | sem rota | sem rota | 329.9 km, 1 recargas | 329.9 km, 1 recargas |
| Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station) | sem rota | sem rota | sem rota | 685.6 km, 3 recargas |
| Florianópolis (UFSC) -> Uruguaiana (ipiringa) | sem rota | sem rota | sem rota | 1372.5 km, 7 recargas |
| Caxias do Sul -> Curitiba (Curitiba Eco Elétrico) | sem rota | sem rota | sem rota | 631.9 km, 2 recargas |

Autonomia minima que viabiliza cada rota na rede atual:

- Curitiba (Curitiba Eco Elétrico) -> Florianópolis (UFSC): 181.9 km
- Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station): 208.4 km
- Florianópolis (UFSC) -> Uruguaiana (ipiringa): 239.0 km
- Caxias do Sul -> Curitiba (Curitiba Eco Elétrico): 211.0 km

## 2. Postos novos estimados para viabilizar cada rota

Cada celula: menor numero de postos novos / distancia total da rota (0 postos = ja viavel).

| Rota | A = 100 km | A = 150 km | A = 200 km | A = 250 km |
|---|---|---|---|---|
| Curitiba (Curitiba Eco Elétrico) -> Florianópolis (UFSC) | 2 / 303.9 km | 1 / 303.9 km | 0 / 329.9 km | 0 / 329.9 km |
| Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station) | 4 / 640.4 km | 2 / 640.8 km | 1 / 637.3 km | 0 / 685.6 km |
| Florianópolis (UFSC) -> Uruguaiana (ipiringa) | 7 / 1116.0 km | 4 / 1116.0 km | 2 / 1137.2 km | 0 / 1372.5 km |
| Caxias do Sul -> Curitiba (Curitiba Eco Elétrico) | 4 / 826.2 km | 2 / 778.7 km | 1 / 781.6 km | 0 / 631.9 km |

## 3. Onde ficam os vaos (trechos que precisam de posto novo)

**Curitiba (Curitiba Eco Elétrico) -> Florianópolis (UFSC), A = 100 km:** 2 posto(s) novo(s), 303.9 km no total
- entre Curitiba (Ecofortte Eletropostos - Mini Preço) e Florianópolis (UFSC) (295.9 km): 2 posto(s), a cerca de 99, 197 km de Curitiba (Ecofortte Eletropostos - Mini Preço)

**Curitiba (Curitiba Eco Elétrico) -> Florianópolis (UFSC), A = 150 km:** 1 posto(s) novo(s), 303.9 km no total
- entre Curitiba (Ecofortte Eletropostos - Mini Preço) e Florianópolis (UFSC) (295.9 km): 1 posto(s), a cerca de 148 km de Curitiba (Ecofortte Eletropostos - Mini Preço)

**Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station), A = 100 km:** 4 posto(s) novo(s), 640.4 km no total
- entre Irati (Copel) e Foz do Iguaçu (Phone charging station) (467.9 km): 4 posto(s), a cerca de 94, 187, 281, 374 km de Irati (Copel)

**Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station), A = 150 km:** 2 posto(s) novo(s), 640.8 km no total
- entre Candói (Eletrovia Paranaense) e Foz do Iguaçu (Phone charging station) (326.4 km): 2 posto(s), a cerca de 109, 218 km de Candói (Eletrovia Paranaense)

**Curitiba (Curitiba Eco Elétrico) -> Foz do Iguaçu (Phone charging station), A = 200 km:** 1 posto(s) novo(s), 637.3 km no total
- entre Candói (Eletrovia Paranaense) e Foz do Iguaçu (Phone charging station) (326.4 km): 1 posto(s), a cerca de 163 km de Candói (Eletrovia Paranaense)

**Florianópolis (UFSC) -> Uruguaiana (ipiringa), A = 100 km:** 7 posto(s) novo(s), 1116.0 km no total
- entre Florianópolis (UFSC) e Torres (Eletroposto) (274.8 km): 2 posto(s), a cerca de 92, 183 km de Florianópolis (UFSC)
- entre Esteio (Petrobrás) e Santa Maria (Parceria Solar) (282.0 km): 2 posto(s), a cerca de 94, 188 km de Esteio (Petrobrás)
- entre Santa Maria (Parceria Solar) e Uruguaiana (ipiringa) (380.3 km): 3 posto(s), a cerca de 95, 190, 285 km de Santa Maria (Parceria Solar)

**Florianópolis (UFSC) -> Uruguaiana (ipiringa), A = 150 km:** 4 posto(s) novo(s), 1116.0 km no total
- entre Florianópolis (UFSC) e Torres (Eletroposto) (274.8 km): 1 posto(s), a cerca de 137 km de Florianópolis (UFSC)
- entre Esteio (Petrobrás) e Santa Maria (Parceria Solar) (282.0 km): 1 posto(s), a cerca de 141 km de Esteio (Petrobrás)
- entre Santa Maria (Parceria Solar) e Uruguaiana (ipiringa) (380.3 km): 2 posto(s), a cerca de 127, 254 km de Santa Maria (Parceria Solar)

**Florianópolis (UFSC) -> Uruguaiana (ipiringa), A = 200 km:** 2 posto(s) novo(s), 1137.2 km no total
- entre Florianópolis (UFSC) e Torres (Eletroposto) (274.8 km): 1 posto(s), a cerca de 137 km de Florianópolis (UFSC)
- entre Santa Maria (Parceria Solar) e Uruguaiana (ipiringa) (380.3 km): 1 posto(s), a cerca de 190 km de Santa Maria (Parceria Solar)

**Caxias do Sul -> Curitiba (Curitiba Eco Elétrico), A = 100 km:** 4 posto(s) novo(s), 826.2 km no total
- entre Torres (Eletroposto) e Florianópolis (UFSC) (280.9 km): 2 posto(s), a cerca de 94, 187 km de Torres (Eletroposto)
- entre Florianópolis (UFSC) e Curitiba (Ecofortte Eletropostos - Mini Preço) (294.7 km): 2 posto(s), a cerca de 98, 196 km de Florianópolis (UFSC)

**Caxias do Sul -> Curitiba (Curitiba Eco Elétrico), A = 150 km:** 2 posto(s) novo(s), 778.7 km no total
- entre Torres (Eletroposto) e Florianópolis (UFSC) (280.9 km): 1 posto(s), a cerca de 140 km de Torres (Eletroposto)
- entre Florianópolis (UFSC) e Curitiba (Ecofortte Eletropostos - Mini Preço) (294.7 km): 1 posto(s), a cerca de 147 km de Florianópolis (UFSC)

**Caxias do Sul -> Curitiba (Curitiba Eco Elétrico), A = 200 km:** 1 posto(s) novo(s), 781.6 km no total
- entre Torres (Eletroposto) e Luiz Alves (Auto Posto Martendal) (390.5 km): 1 posto(s), a cerca de 195 km de Torres (Eletroposto)

## 4. Rede inteira: componentes e postos para liga-las

| Autonomia | Componentes f-conexas | Postos novos (estimativa minima para ligar todas) |
|---|---|---|
| 100 km | 21 | 25 |
| 150 km | 15 | 14 |
| 200 km | 6 | 5 |
| 250 km | 2 | 1 |

Ligacoes escolhidas para A = 100 km (postos novos, km, estacoes extremas):
- 1 posto(s) entre Caxias do Sul e Lajeado (Certel) (103.4 km)
- 1 posto(s) entre Quaraí (Ipiranga) e Uruguaiana (ipiringa) (117.2 km)
- 1 posto(s) entre Cruz Alta (Posto Ipiranga) e Santa Maria (Parceria Solar) (128.7 km)
- 1 posto(s) entre Gaspar (Fazzenda Park Resort) e Florianópolis (UFSC) (130.1 km)
- 1 posto(s) entre Cruz Alta (Posto Paizão) e Santa Rosa (138.9 km)
- 1 posto(s) entre Candói (Eletrovia Paranaense) e Irati (Copel) (141.9 km)
- 1 posto(s) entre Camargo e Lajeado (Certel) (154.2 km)
- 1 posto(s) entre Chapecó (Estação de Carregamento de Carros Elétricos ou Híbridos) e Joaçaba (coulomb) (156.7 km)
- 1 posto(s) entre Corbélia e Foz do Iguaçu (Phone charging station) (166.3 km)
- 1 posto(s) entre Lages (Restaurante Cansian Zamban) e Joaçaba (coulomb) (170.8 km)
- 1 posto(s) entre Irati (Copel) e União da Vitória (Usina hidrelétrica Salto do Vau) (180.3 km)
- 1 posto(s) entre Curitiba (Ecofortte Eletropostos - Mini Preço) e Pomerode (182.0 km)
- 1 posto(s) entre União da Vitória (Usina hidrelétrica Salto do Vau) e Joaçaba (coulomb) (188.3 km)
- 1 posto(s) entre Dom Pedrito (Eletroposto) e Quaraí (193.8 km)
- 1 posto(s) entre Camargo e Condor (194.8 km)
- 2 posto(s) entre Apucarana e Santo Antônio da Platina (Ipiranga) (204.7 km)
- 2 posto(s) entre Candói (Eletrovia Paranaense) e Corbélia (209.0 km)
- 2 posto(s) entre Condor e Chapecó (Estação de Carregamento de Carros Elétricos ou Híbridos) (211.2 km)
- 2 posto(s) entre Bagé (Estação de carregamento de veículos elétricos) e Santa Maria (Parceria Solar) (239.8 km)
- 2 posto(s) entre Apucarana e Palmeira (Petrobras) (293.6 km)

Ligacoes escolhidas para A = 150 km (postos novos, km, estacoes extremas):
- 1 posto(s) entre Lajeado (Certel) e Camargo (154.2 km)
- 1 posto(s) entre Chapecó (Estação de Carregamento de Carros Elétricos ou Híbridos) e Joaçaba (coulomb) (156.7 km)
- 1 posto(s) entre Corbélia e Foz do Iguaçu (Phone charging station) (166.3 km)
- 1 posto(s) entre Lages (Restaurante Cansian Zamban) e Joaçaba (coulomb) (170.8 km)
- 1 posto(s) entre Irati (Copel) e União da Vitória (Usina hidrelétrica Salto do Vau) (180.3 km)
- 1 posto(s) entre Curitiba (Ecofortte Eletropostos - Mini Preço) e Pomerode (182.0 km)
- 1 posto(s) entre União da Vitória (Usina hidrelétrica Salto do Vau) e Joaçaba (coulomb) (188.3 km)
- 1 posto(s) entre Dom Pedrito (Eletroposto) e Quaraí (193.8 km)
- 1 posto(s) entre Camargo e Condor (194.8 km)
- 1 posto(s) entre Apucarana e Santo Antônio da Platina (Ipiranga) (204.7 km)
- 1 posto(s) entre Candói (Eletrovia Paranaense) e Corbélia (209.0 km)
- 1 posto(s) entre Condor e Chapecó (Estação de Carregamento de Carros Elétricos ou Híbridos) (211.2 km)
- 1 posto(s) entre Bagé (Estação de carregamento de veículos elétricos) e Santa Maria (Parceria Solar) (239.8 km)
- 1 posto(s) entre Apucarana e Palmeira (Petrobras) (293.6 km)

Ligacoes escolhidas para A = 200 km (postos novos, km, estacoes extremas):
- 1 posto(s) entre Apucarana e Santo Antônio da Platina (Ipiranga) (204.7 km)
- 1 posto(s) entre Candói (Eletrovia Paranaense) e Corbélia (209.0 km)
- 1 posto(s) entre Chapecó (Estação de Carregamento de Carros Elétricos ou Híbridos) e Condor (211.2 km)
- 1 posto(s) entre Bagé (Estação de carregamento de veículos elétricos) e Santa Maria (Parceria Solar) (239.8 km)
- 1 posto(s) entre Apucarana e Palmeira (Petrobras) (293.6 km)

Ligacoes escolhidas para A = 250 km (postos novos, km, estacoes extremas):
- 1 posto(s) entre Apucarana e Palmeira (Petrobras) (293.6 km)

Limites: estimativa por trecho rodoviario direto entre estacoes existentes, com postos igualmente espacados; nao considera demanda, capacidade da rede eletrica, custo nem a posicao exata de cidades/postos de combustivel ao longo da via. Serve para dimensionar os vaos de cobertura, nao para decidir localizacoes.
