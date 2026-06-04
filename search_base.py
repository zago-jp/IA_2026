from typing import Iterator  # Importa o tipo Iterator, usado para indicar que uma função retorna valores um a um (como um gerador)

#----------------- Classe que define estados (State) ----------------------#
class State:
    """
    Um estado consiste em uma string `location` e `memory` (possivelmente null).
    Note que `memory` deve ser um tipo de dado "Hashable" (porque implementamos 
    o algoritmo de busca usando um dict e usamos instâncias da classe `State` 
    como chaves para os valores). Por exemplo:
        - qualquer primitivo não mutável (str, int, float, etc.)
        - tuplas
        - combinações aninhadas dos itens acima
    A medida que você implementa diferentes tipos de problemas de busca ao longo
    da tarefa, pense no que `memory` deve conter para permitir uma busca eficiente!

    Uso:
        state = State(location="A", memory=("some_hashable_data_type", 123))
    """         

    def __init__(self, location: str, memory: frozenset=None):  # Construtor: chamado ao criar um novo State; recebe localização (str) e memória (frozenset ou None)
        self.location = location    # Armazena a localização atual do agente (ex: nome de um nó no grafo)
        self.memory = memory if memory is not None else frozenset()  # Armazena a memória; se não fornecida, usa frozenset vazio (imutável e hashable)

    def __hash__(self):  # Define como calcular o "hash" do objeto — necessário para usar State como chave em dicionários ou conjuntos (set/dict)
        return hash((self.location, self.memory))  # Gera o hash a partir de uma tupla com os dois atributos (ambos precisam ser hashable)
    
    def __repr__(self):  # Define como o objeto é exibido como string (ex: no terminal ou no print)
        return f"State(location={self.location!r}, memory={self.memory!r})"  # Retorna uma string legível mostrando localização e memória
    
    def __eq__(self, other):  # Define o critério de igualdade entre dois States — usado ao comparar estados
        return (self.location, self.memory) == (other.location, other.memory)  # Dois estados são iguais se tiverem a mesma localização E a mesma memória
    
#----------Classe base para problemas de busca (SearchProblem) -------------#
class SearchProblem:
    def __init__(self, initial_state: State, goal_state: State):  # Construtor: recebe o estado inicial e o estado objetivo do problema
        self.initial_state = initial_state  # Armazena o estado de onde a busca começa
        self.goal_state = goal_state        # Armazena o estado que queremos alcançar
    
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:  # Deve retornar os estados vizinhos (sucessores) de um estado, com a ação tomada e o custo
        raise NotImplementedError("Override me")  # Método abstrato: obriga subclasses a implementarem; lança erro se chamado diretamente

    def get_initial_state(self) -> State:  # Retorna o estado inicial do problema
        return self.initial_state          # Simplesmente devolve o atributo armazenado no construtor
    
    def is_goal(self, state: State) -> bool:  # Verifica se um estado fornecido é o estado objetivo
        return state == self.goal_state       # Compara o estado com o objetivo usando o __eq__ definido em State
    
    def h(self, state: State) -> float:           # Heurística h(n): estima o custo restante do estado atual até o objetivo (usada em A*)
        raise NotImplementedError("Override me")  # Método abstrato: cada problema concreto deve definir sua própria heurística
    
    def __repr__(self) -> str:  # Define a representação em string do problema
        return f"Problem(initial={self.initial_state!r}, goal={self.goal_state!r})"  # Exibe o estado inicial e o objetivo de forma legível
    
#-------------Classe que define nós da árvore de busca (Node) ---------------#
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0.0):  # Construtor: cria um nó com seu estado, referência ao pai, ação que o gerou e custo acumulado
        self.state = state          # Estado associado a este nó na árvore de busca
        self.parent = parent        # Referência para o nó pai; None indica que é a raiz da árvore
        self.action = action        # Ação executada para chegar a este nó a partir do pai; None na raiz
        self.path_cost = path_cost  # Custo g(n): soma dos custos de todas as ações do caminho da raiz até este nó
    
    def path_actions(self) -> list[str]:  # Reconstrói e retorna a lista de ações tomadas da raiz até este nó
       actions = []   # Lista vazia que vai acumular as ações
       node = self    # Começa pelo nó atual e vai subindo até a raiz
       
       while node.parent is not None:   # Continua enquanto houver um nó pai (para quando chega à raiz)
          actions.append(node.action)   # Adiciona a ação que levou a este nó
          node = node.parent            # Sobe um nível na árvore (vai para o nó pai)
       
       actions.reverse()  # Inverte a lista, pois foi construída de trás para frente (do nó até a raiz)
       return actions      # Retorna a sequência de ações na ordem correta (da raiz até o nó)
        
    def path_states(self) -> list[State]:  # Reconstrói e retorna a lista de estados visitados da raiz até este nó
        node = self   # Começa pelo nó atual
        states = []   # Lista vazia que vai acumular os estados

        while node is not None:          # Continua enquanto houver nó (inclui a raiz, que tem parent=None)
            states.append(node.state)    # Adiciona o estado do nó atual à lista
            node = node.parent           # Sobe um nível na árvore
        
        states.reverse()  # Inverte a lista, pois foi construída de trás para frente
        return states      # Retorna os estados na ordem correta (do estado inicial até o atual)
   
    def depth(self) -> int:  # Calcula e retorna a profundidade do nó na árvore (quantos níveis abaixo da raiz)
        node = self   # Começa pelo nó atual
        d = 0         # Contador de profundidade, começa em 0
        while node.parent is not None:  # Sobe pela árvore enquanto houver pai
            d += 1           # Incrementa a profundidade a cada nível subido
            node = node.parent  # Move para o nó pai
        return d  # Retorna a profundidade total

    def expand(self, problem: SearchProblem):  # Expande o nó gerando todos os nós filhos com base nos sucessores do problema
        for state, action, cost in problem.successors(self.state):  # Itera sobre cada sucessor: (novo estado, ação, custo da ação)
            yield Node(state, self, action, self.path_cost + cost)  # Cria e entrega (yield) um novo nó filho com custo acumulado atualizado
    
    def __repr__(self):  # Define como o nó é exibido como string
        return f"Node({self.state!r})"  # Exibe apenas o estado contido no nó
    
#-------------Classe base para algoritmos de busca (SearchAlgorithm) ---------------#
class SearchAlgorithm:    
    def solve(self, search_problem: SearchProblem) -> None:  # Método que deve ser implementado por cada algoritmo concreto (BFS, DFS, A*, etc.)
        raise NotImplementedError("Override me")  # Método abstrato: lança erro se chamado sem ser sobrescrito por uma subclasse