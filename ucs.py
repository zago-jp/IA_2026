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
         
    def g(self, n:Node)->float:
        return n.path_cost
    
    # Implementação da UCS com tabela de estados alcançados para evitar reexploração    
    def solve(self, search_problem: SearchProblem) -> None: 
        # re-inicializa as variáveis 
        self.actions: list[str] = []
        self.states: list[State] = []           
        self.path_cost: float = None           
        self.num_states_explored: int = 0      
        
        # RAPAZ, TA MEIO CONFUSO O CODIGO MAS ACHO QUE TA CORRETO.
        # self referencia a classe não instacia da classe
        # actual_node é o nó que acabou de sair da fronteira, ou seja o nó que foi escolhido e ta sendo tratado pelo algoritmo
        # reached é a lista dos melhores nós ja escolhidos até agora.
        # Inicializa a fronteira e a tabela de estados alcançados
        frontier = PriorityQueue(key=lambda n: self.g(n))
        frontier.push(Node(state=search_problem.get_initial_state())) 
        reached = {} # Guarda o nó de menor custo para cada estado alcançado
        
        # Implementação do restante da UCS(AQUI)
        while not frontier.is_empty():
            actual_node = frontier.pop() #nó da busca que esta sendo iterado 
            self.num_states_explored +=1 #atualizando o numero de nós totais ja explorados
            if search_problem.is_goal(actual_node.state):
                self.actions = actual_node.path_actions()
                self.states = actual_node.path_states()
                self.path_cost = actual_node.path_cost
                return
                
            for child in actual_node.expand(search_problem):
                s = child.state
                if s not in reached or child.path_cost < reached[s].path_cost:
                    reached[s] = child
                    frontier.push(child)
    
        
        