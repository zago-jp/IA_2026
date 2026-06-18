from search_base import SearchProblem, SearchAlgorithm, State
from map_util import CityMap, GeoLocation, create_bg_map, location_from_tag, read_map, print_path, compute_distance
from visualization import plot_map
from typing import Iterator
from ucs import UniformCostSearch
from a_start import AStar

from time import perf_counter

#---------------- Problema de menor caminho entre duas localizações ---------------#
class ShortestPathProblem(SearchProblem):
    # Construtor
    def __init__(self, start_location: str, end_location: str, city_map: CityMap):
        # Inicializa o problema com estado inicial e estado objetivo
        super().__init__(initial_state=State(start_location), goal_state=State(end_location))
        self.city_map = city_map        # Mapa com distâncias e coordenadas geográficas

    # Gera os sucessores do estado atual
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
        # Percorre todos os vizinhos conectados ao local atual
        for neighbor, distance in self.city_map.distances[state.location].items():
            
            # Retorna o próximo estado, a ação e o custo do deslocamento
            yield State(location=neighbor), neighbor, distance
        
    # h(n) = distância em linha reta entre o estado atual e o objetivo
    def h(self, state: State) -> float:
        # Coordenadas do estado atual
        geo_actual = self.city_map.geo_locations[state.location]
        
        # Coordenadas do estado objetivo
        geo_goal  = self.city_map.geo_locations[self.goal_state.location]
        
        # Estimativa heurística baseada na distância geográfica
        return compute_distance(geo_actual, geo_goal)

#---------------- Testes e visualização dos resultados ---------------#
if __name__ == "__main__":
    
    # Cria o mapa de Barra do Garças
    city_map = create_bg_map()
    
    # Define os pontos inicial e final do exemplo
    start = location_from_tag("landmark=ufmt-biblioteca", city_map)
    end = location_from_tag("landmark=madre-marta", city_map)
    
    # Cria o problema de menor caminho
    problem = ShortestPathProblem(start_location=start, end_location=end, city_map=city_map)
    
    Algoritmo = 1
    
    match Algoritmo:
        case 1:
            # Executa a busca com UCS
            ucs = UniformCostSearch()
            ucs.solve(problem)
            
            # Exibe e plota o caminho encontrado pela UCS
            print_path([start] + ucs.actions, [], city_map)
            plot_map(city_map, [start] + ucs.actions, waypoint_tags=[], map_name="Shortest Path Visualization")
            
        case 2:
            # Executa a busca com A*
            astar = AStar()
            astar.solve(problem)
            
            # Exibe e plota o caminho encontrado pelo A*
            print_path([start] + astar.actions, [], city_map)
            plot_map(city_map, [start] + astar.actions, waypoint_tags=[], map_name="Shortest Path Visualization")
            
        case _:
            print("Valor inválido")
        
