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
        
    # ------ IMPLEMENTAÇÃO ---------------------------------------------------------

    # Implementação A-Star
    def solve(self, search_problem: SearchProblem) -> None:
        # Inicializa e zera execuções anteriores
        self.actions = []               # Guarda a sequência de ações
        self.states = []                # Guarda todos os estados do caminho
        self.path_cost = None           # Custo total encontrado
        self.num_states_explored = 0    # Contagem de número de nós expandidos(explorados)
        
        # f(n) = g(n) + h(n)
        def f(n):
            return n.path_cost + search_problem.h(n.state)

        # Fila de Prioridade: usando a f(n)
        frontier = PriorityQueue(key=f)
        
        # Melhor caminho de cada estado
        reached = {}
        
        # Cria o nó inicial
        initial_node = Node(state=search_problem.get_initial_state())
        
        # Coloca o nó na frnteira
        frontier.push(initial_node)
        
        # Registra o caminho visitado(alcançado)
        reached[initial_node.state] = initial_node
        
        # Loop principal(Enquanto houver estados a explorar)
        while not frontier.is_empty():
            node = frontier.pop()           # Remove o melhor nó(menor f(n))
            
            # Checa se esse ainda é o melhor caminho conhecido para o seue estado,
            # se não for, foi superado -> descarta e pga o próximo
            if reached.get(node.state) is not node:
                continue
            
            self.num_states_explored += 1
            
            # Teste de objetivo
            if search_problem.is_goal(node.state):
                # Recupera as ações percorrido
                self.actions = node.path_actions()
                # Recupera os estados visitados
                self.states = node.path_states()
                # Guarda o custo
                self.path_cost = node.path_cost
                # Encerra
                return
            
            # Expansão para os filhos
            for child in node.expand(search_problem):
                # Estado do filho
                s = child.state
                # Verifica se (state) nunca foi visitado ou se já foi visitado, mas esse caminho é melhor.
                if s not in reached or child.path_cost < reached[s].path_cost:
                    # Atualiza o melhor nó para chegar em (state)
                    reached[s] = child 
                    # Coloca novamente na fronteira para ser explorado futuramente
                    frontier.push(child)
            


