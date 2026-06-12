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

'''
if __name__ == "__main__":

    city_map = create_bg_map()
    
    print("\nLANDMARKS DISPONÍVEIS:\n")

    for tag in city_map.tags:
        if tag.startswith("landmark="):
            print(tag)
    tests = [
        ("landmark=ufmt-biblioteca", "landmark=madre-marta"),
        ("landmark=ufmt-biblioteca", "landmark=aguas_quentes"),
        ("landmark=ufmt-biblioteca", "landmark=forum"),
        ("landmark=ufmt-biblioteca", "landmark=prefeitura"),
        ("landmark=ufmt-biblioteca", "landmark=banco_brasil"),

        ("landmark=madre-marta", "landmark=aguas_quentes"),
        ("landmark=madre-marta", "landmark=forum"),
        ("landmark=madre-marta", "landmark=prefeitura"),

        ("landmark=forum", "landmark=banco_brasil"),
        ("landmark=forum", "landmark=mirante_cristo"),

        ("landmark=prefeitura", "landmark=aguas_quentes"),
        ("landmark=prefeitura", "landmark=cachoeira_usina"),

        ("landmark=banco_brasil", "landmark=mirante_cristo"),
        ("landmark=banco_brasil", "landmark=cachoeira_usina"),

        ("landmark=mirante_cristo", "landmark=aguas_quentes")
    ]

    print("\n" + "=" * 120)
    print(f"{'ORIGEM':25} {'DESTINO':25} {'UCS NÓS':10} {'A* NÓS':10} {'UCS(s)':12} {'A*(s)':12} {'CUSTO':12}")
    print("=" * 120)

    total_ucs_nodes = 0
    total_astar_nodes = 0

    total_ucs_time = 0
    total_astar_time = 0

    for origin_tag, destination_tag in tests:

        start = location_from_tag(origin_tag, city_map)
        end = location_from_tag(destination_tag, city_map)
        
        problem = ShortestPathProblem(
            start_location=start,
            end_location=end,
            city_map=city_map
        )

        # UCS
        ucs = UniformCostSearch()

        t0 = perf_counter()
        ucs.solve(problem)
        ucs_time = perf_counter() - t0

        # A*
        astar = AStar()

        t0 = perf_counter()
        astar.solve(problem)
        astar_time = perf_counter() - t0

        total_ucs_nodes += ucs.num_states_explored
        total_astar_nodes += astar.num_states_explored

        total_ucs_time += ucs_time
        total_astar_time += astar_time

        print(
            f"{origin_tag.replace('landmark=',''):25} "
            f"{destination_tag.replace('landmark=',''):25} "
            f"{ucs.num_states_explored:<10} "
            f"{astar.num_states_explored:<10} "
            f"{ucs_time:<12.6f} "
            f"{astar_time:<12.6f} "
            f"{ucs.path_cost:<12.2f}"
        )

    print("=" * 120)

    print("\nMÉDIAS:")

    print(
        f"UCS  -> Nós explorados: {total_ucs_nodes/len(tests):.2f} | "
        f"Tempo médio: {total_ucs_time/len(tests):.6f}s"
    )

    print(
        f"A*   -> Nós explorados: {total_astar_nodes/len(tests):.2f} | "
        f"Tempo médio: {total_astar_time/len(tests):.6f}s"
    )

    reduction = (
        (total_ucs_nodes - total_astar_nodes)
        / total_ucs_nodes
    ) * 100

    print(
        f"\nRedução média de nós explorados pelo A*: {reduction:.2f}%"
    )
'''