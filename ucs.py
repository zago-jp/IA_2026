from search_base import SearchProblem, SearchAlgorithm, Node, State
from util import PriorityQueue

#---------------- Busca com custo uniforme (Uniform-Cost Search - UCS) ---------------#
class UniformCostSearch(SearchAlgorithm):
    # Construtor
    def __init__(self):
        super().__init__()
        self.actions: list[str] = []           # Lista de ações para chegar ao estado objetivo
        self.states: list[State] = []          # Lista de estados para chegar ao estado objetivo
        self.path_cost: float = None           # Soma dos custos ao longo do caminho
        self.num_states_explored: int = 0      # Número de estados explorados
         
    # g(n) = custo acumulado do nó até o estado atual
    def g(self, n: Node) -> float:
        return n.path_cost
    
    # Implementação da UCS com tabela de estados alcançados
    def solve(self, search_problem: SearchProblem) -> None:
        
        # Inicializa e zera execuções anteriores(Caso já tenha sido executado anteriormente)
        self.actions = []               # Guarda a sequência de ações
        self.states = []                # Guarda todos os estados do caminho
        self.path_cost = None           # Custo total encontrado
        self.num_states_explored = 0    # Contagem do número de nós explorados
        
        # Fila de Prioridade: usando g(n)
        frontier = PriorityQueue(key=lambda n: self.g(n))
        
        # Cria o nó inicial
        initial_node = Node(state=search_problem.get_initial_state())
        
        # Melhor caminho encontrado para cada estado
        reached = {}
        
        # Coloca o nó inicial na fronteira
        frontier.push(initial_node)
        
        # Registra o primeiro estado alcançado
        reached[initial_node.state] = initial_node
        
        # Loop principal (enquanto houver estados para explorar)
        while not frontier.is_empty():
            
            # Remove o nó de menor custo acumulado
            actual_node = frontier.pop()
            
            # Conta o número de nós explorados
            self.num_states_explored += 1
            
            # Teste de objetivo
            if search_problem.is_goal(actual_node.state):
                
                # Recupera as ações do caminho solução
                self.actions = actual_node.path_actions()
                
                # Recupera os estados visitados
                self.states = actual_node.path_states()
                
                # Guarda o custo total da solução
                self.path_cost = actual_node.path_cost
                
                # Encerra a busca
                return
                
            # Expande os filhos do nó atual
            for child in actual_node.expand(search_problem):
                
                # Estado do filho
                s = child.state
                
                # Se o estado nunca foi alcançado ou encontramos um caminho melhor
                if s not in reached or child.path_cost < reached[s].path_cost:
                    
                    # Atualiza o melhor caminho para o estado
                    reached[s] = child
                    
                    # Adiciona o filho à fronteira para exploração futura
                    frontier.push(child)