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

    # Implementação A-Star
    def solve(self, search_problem: SearchProblem) -> None:
        self.actions = []
        self.states = []
        self.path_cost = None
        self.num_states_explored = 0

        # Prioridade: f(n) = g(n) + h(n)
        frontier = PriorityQueue(key=lambda n: n.path_cost + search_problem.h(n.state))
        reached = {}
