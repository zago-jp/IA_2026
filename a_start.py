from search_base import SearchProblem, SearchAlgorithm, Node, State
from util import PriorityQueue

#---------------- Busca A* (A-Star Search) ---------------#
class AStar(SearchAlgorithm):
    # Construtor
    def __init__(self):
        super().__init__()
        self.actions: list[str] = []           # Lista de ações para chegar ao estado objetivo
        self.states: list[State] = []          # Lista de estados para chegar ao estado objetivo
        self.path_cost: float = None           # Soma dos custos ao longo do caminho
        self.num_states_explored: int = 0      # Número de estados explorados

    # Implementação da busca A*
    def solve(self, search_problem: SearchProblem) -> None:
        
        # Inicializa e zera execuções anteriores(Caso já tenha sido executado anteriormente)
        self.actions = []               # Guarda a sequência de ações
        self.states = []                # Guarda todos os estados do caminho
        self.path_cost = None           # Custo total encontrado
        self.num_states_explored = 0    # Contagem do número de nós explorados
        
        # f(n) = g(n) + h(n)
        def f(n):
            return n.path_cost + search_problem.h(n.state)

        # Fila de Prioridade: usando f(n)
        frontier = PriorityQueue(key=f)
        
        # Melhor caminho encontrado para cada estado
        reached: dict[State, Node] = {}
        
        # Cria o nó inicial
        initial_node = Node(state=search_problem.get_initial_state())
        
        # Coloca o nó inicial na fronteira
        frontier.push(initial_node)
        
        # Registra o primeiro estado alcançado
        reached[initial_node.state] = initial_node
        
        # Loop principal (enquanto houver estados para explorar)
        while not frontier.is_empty():
            
            # Remove o nó com maior prioridade(menor )
            node = frontier.pop()
            
            # Otimização
            if reached.get(node.state) is not node:
                continue
            
            # Conta o número de nós explorados
            self.num_states_explored += 1
            
            # Teste de objetivo
            if search_problem.is_goal(node.state):
                self.actions = node.path_actions()
                self.states = node.path_states()
                self.path_cost = node.path_cost
                return
            
            # Expande os filhos do nó atual
            for child in node.expand(search_problem):
                
                filho = child.state
                
                # Se o estado nunca foi alcançado ou encontramos um caminho melhor
                if filho not in reached or child.path_cost < reached[filho].path_cost:
                    
                    # Atualiza o melhor caminho para o estado
                    reached[filho] = child
                    # Adiciona o filho à fronteira para exploração futura
                    frontier.push(child)
