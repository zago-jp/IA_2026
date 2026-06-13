from search_base import SearchProblem, SearchAlgorithm, State
from map_util import CityMap, GeoLocation, create_bg_map, location_from_tag, read_map, print_path, compute_distance
from visualization import plot_map
from typing import Iterator
from ucs import UniformCostSearch
from a_start import AStar

from time import perf_counter

# Modela o problema de encontrar o caminho mais curto entre duas localizações em um mapa da cidade
class ShortestPathProblem(SearchProblem):
    def __init__(self, start_location: str, end_location: str, city_map: CityMap):
        super().__init__(initial_state=State(start_location), goal_state=State(end_location))
        self.city_map = city_map

    # IMPLEMENTAÇÃO DA FUNÇÃO SUCESSORA COM HEURISTICA
    
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
        for neighbor, distance in self.city_map.distances[state.location].items():
            yield State(location=neighbor), neighbor, distance
        
    def h(self, state: State) -> float:
        geo_actual = self.city_map.geo_locations[state.location]
        geo_goal  = self.city_map.geo_locations[self.goal_state.location]
        return compute_distance(geo_actual, geo_goal)    
      
# Realiza testes e visualiza os resultados
if __name__ == "__main__":
    # Exemplo de uso
    city_map = create_bg_map()  # criar um mapa de bg
    start = location_from_tag("landmark=ufmt-biblioteca", city_map)
    end = location_from_tag("landmark=madre-marta", city_map)
    
    problem = ShortestPathProblem(start_location=start, end_location=end, city_map=city_map)
    
    # Para testar a UCS descomente o codigo abaixo:
    
    ucs = UniformCostSearch()
    ucs.solve(problem)
    print_path([start] + ucs.actions, [], city_map) 
    plot_map(city_map, [start] + ucs.actions, waypoint_tags=[], map_name="Shortest Path Visualization")
    
    # Para testar o A-Star:
    astar = AStar()
    astar.solve(problem)
    print_path([start] + astar.actions, [], city_map)
    plot_map(city_map, [start] + astar.actions, waypoint_tags=[], map_name="Shortest Path Visualization")

