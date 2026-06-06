# Descrição dos Testes — Parte 1

## Configuração do Ambiente de Teste

Os testes da Parte 1 utilizam o mapa real da cidade de Barra do Garças (MT), carregado a partir do arquivo `barra-do-garcas.pbf` com pontos de interesse definidos em `bg-landmarks.json`. O mapa é construído pela função `create_bg_map()`, que processa a malha viária e as distâncias entre nós adjacentes. O par de localidades utilizado nos testes foi:

- **Origem:** `landmark=ufmt-biblioteca` — Biblioteca da UFMT, campus Barra do Garças
- **Destino:** `landmark=madre-marta` — Colégio Madre Marta

Ambos os pontos são recuperados via `location_from_tag()`, que mapeia as tags de landmarks para os identificadores internos de nós do grafo.

---

## Algoritmos Testados

### 1. Busca de Custo Uniforme (UCS)

A UCS foi testada como linha de base. Ela expande os nós em ordem crescente de custo acumulado `g(n)`, sem qualquer estimativa heurística do custo restante até o objetivo. A fila de prioridade usa exclusivamente `g(n)` como critério de ordenação.

**Característica:** garante a solução de custo mínimo, mas pode explorar um número elevado de nós, pois não possui informação sobre a direção do objetivo.

### 2. Busca A* (A-Star)

O A* foi testado como algoritmo informado, usando a função de avaliação `f(n) = g(n) + h(n)`, onde:

- `g(n)` é o custo acumulado do caminho da origem até o nó `n`
- `h(n)` é a heurística admissível: distância geográfica em linha reta entre a posição atual e o destino, calculada por `compute_distance()` com base nas coordenadas `GeoLocation` de cada nó

**Característica:** ao combinar custo real com estimativa heurística, o A* direciona a busca para regiões promissoras do grafo, reduzindo o número de nós expandidos em relação à UCS, mantendo a garantia de otimalidade desde que `h(n)` seja admissível (nunca superestime o custo real).

---

## Implementação da Função Sucessora

O método `successors()` da classe `ShortestPathProblem` itera sobre todos os vizinhos do nó atual a partir do dicionário `city_map.distances`, retornando para cada vizinho uma tripla `(novo_estado, ação, custo)`. A ação corresponde ao identificador do nó vizinho e o custo é a distância viária entre os dois nós.

```python
def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
    for neighbor, distance in self.city_map.distances[state.location].items():
        yield State(location=neighbor), neighbor, distance
```

---

## Heurística Utilizada

A heurística `h(n)` calcula a distância em linha reta (distância geodésica) entre a localização atual e o destino:

```python
def h(self, state: State) -> float:
    geo_actual = self.city_map.geo_locations[state.location]
    geo_goal   = self.city_map.geo_locations[self.goal_state.location]
    return compute_distance(geo_actual, geo_goal)
```

Esta heurística é **admissível**, pois a distância em linha reta nunca é maior que a distância real pelo caminho viário. Isso garante que o A* encontre sempre a solução ótima.

---

## Resultados Esperados

Ambos os algoritmos devem encontrar o mesmo caminho de custo mínimo entre a Biblioteca da UFMT e o Colégio Madre Marta. A diferença esperada está na **eficiência da busca**: o A* deve expandir menos nós que a UCS por guiar a exploração na direção do objetivo, enquanto a UCS explora de forma mais uniforme pelo grafo. O caminho encontrado é exibido no terminal via `print_path()` e visualizado interativamente no mapa com `plot_map()`.