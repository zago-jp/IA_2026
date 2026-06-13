# IA 2026 — Trabalho 1: Planejamento de Rotas em Barra do Garças

## Requisitos

- Python 3.12+
- Dependências: instale com `pip install -r requirements.txt` (se houver) ou manualmente conforme os imports dos arquivos

---

## Estrutura do Projeto

```
trabalho/
├── data/
│   ├── barra-do-garcas.pbf       # Mapa OSM da cidade
│   └── bg-landmarks.json         # Pontos de interesse
├── a_start.py                    # Implementação do A*
├── ucs.py                        # Implementação do UCS
├── search_base.py                # Classes base (SearchProblem, Node, State...)
├── map_util.py                   # Utilitários do mapa
├── util.py                       # PriorityQueue e utilitários gerais
├── visualization.py              # Visualização no navegador
├── view.py                       # Menu interativo (parte 2)
├── trab-parte1.py                # Problema 1: caminho mínimo A → B
└── trab-parte2.py                # Problema 2: rota com waypoints
```

---

## Parte 1 — Caminho Mínimo entre Dois Pontos

### O que foi implementado

- **`ShortestPathProblem`** (`trab-parte1.py`): define o problema de busca concreto com origem, destino e mapa
- **`successors()`**: itera sobre os vizinhos do nó atual no grafo via `city_map.distances`
- **`h()`**: heurística de distância em linha reta entre o estado atual e o objetivo via `compute_distance()`
- **`ucs.py`**: Uniform Cost Search completo com fila de prioridade por `g(n)`
- **`a_start.py`**: A* completo com fila de prioridade por `f(n) = g(n) + h(n)`

### Como usar

Edite o `trab-parte1.py` e defina origem e destino:

```python
start = location_from_tag("landmark=ufmt-biblioteca", city_map)
end   = location_from_tag("landmark=madre-marta",     city_map)
```

Para rodar com **A\***:
```cmd
python trab-parte1.py
```

Para rodar com **UCS**, descomente o bloco da UCS e comente o do A* no `__main__`.

O mapa abre automaticamente no navegador em `http://127.0.0.1:<porta>`.

> **Windows:** se o mapa não abrir, libere o Python no Firewall:
> ```cmd
> netsh advfirewall firewall add rule name="Python314" dir=in action=allow program="C:\Python314\python.exe" enable=yes
> ```

---

## Parte 2 — Rota com Waypoints Intermediários

### O que foi implementado

- **`WaypointsShortestPathProblem`** (`trab-parte2.py`): estende `SearchProblem` para rotas com múltiplas paradas, resolve trecho a trecho
- **`successors()`**: mesma lógica da parte 1
- **`h()`**: mesma heurística de linha reta da parte 1
- **`map_util.py`**: adicionada `location_from_tag_id()` para buscar landmark por índice numérico
- **`view.py`**: classe `Menu` com interface interativa para montar a rota
- Suporte a escolha de algoritmo (**UCS** ou **A\***) direto no menu

### Como usar — Modo Interativo

```cmd
python trab-parte2.py
```

O menu apresenta as opções:

```
1 - Adicionar inicio: <ponto atual>
2 - Adicionar parada
3 - Remover parada
4 - Algoritmo de busca: UCS | A*
0 - Realizar Rota
```

1. Escolha **1** para definir o ponto de partida
2. Escolha **2** para adicionar paradas (a última parada adicionada é o destino final)
3. Escolha **4** para alternar entre UCS e A* (padrão: UCS)
4. Escolha **0** para executar a rota

### Como usar — Modo Testes

No final do `trab-parte2.py` existe um bloco de testes que roda automaticamente várias rotas comparando UCS e A*, sem abrir o mapa:

```cmd
python trab-parte2.py
```

A saída mostra uma tabela com origem, waypoints, destino, nós explorados por cada algoritmo, tempo e custo total, e ao final as médias e a redução percentual de nós do A* em relação à UCS.

---

## Pontos de Interesse Disponíveis

Para ver todos os landmarks disponíveis no mapa, rode no Python:

```python
from map_util import create_bg_map
city_map = create_bg_map()
for tag in city_map.tags:
    if tag.startswith("landmark="):
        print(tag)
```