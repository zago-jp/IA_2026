import json
import os
from time import sleep

from map_util import create_bg_map, location_from_tag, location_from_tag_id, print_path, CityMap, compute_distance
from search_base import SearchProblem, State
from typing import Iterator
from view import Menu
from ucs import UniformCostSearch
from visualization import plot_map
from time import perf_counter
from a_start import AStar


class WaypointsShortestPathProblem(SearchProblem):
    # IMPLEMENTE AQUI: Defina o construtor e o método de sucessores
    def __init__(self, start_state:str|None, goal_state:str, waypoints: list[set[str]], city_map:CityMap):
        super().__init__(initial_state=State(start_state), goal_state = State(goal_state))
        self.waypoints = waypoints
        self.city_map = city_map

    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
        for neighbor, distance in self.city_map.distances[state.location].items():
            yield State(location=neighbor), neighbor, distance
            
    def h(self, state: State) -> float:
        geo_actual = self.city_map.geo_locations[state.location]
        geo_goal   = self.city_map.geo_locations[self.goal_state.location]
        return compute_distance(geo_actual, geo_goal)

# Realize testes e visualiza os resultados
'''
if __name__ == "__main__":
    city_map = create_bg_map()
    menu = Menu()
    initial_state = None
    waypoints = []
    op = -1
    initial = None

    while op != 0:
        menu.show_menu()
        op = int(input(""))
        match op:
            case 1:
                menu.show_menu_dot()
                new_start = int(input(""))
                landmark = location_from_tag_id(new_start, city_map)["landmark"]
                initial_state = location_from_tag(f"landmark={landmark}", city_map)
                initial = landmark
                menu.option = new_start
                continue
            case 2:
                menu.show_menu_dot()
                new_end = int(input(""))
                if new_end == 0:
                    continue
                landmark = location_from_tag_id(new_end, city_map)["landmark"]
                menu.waypoints_travelling.append(landmark)
                waypoints.append(location_from_tag(f"landmark={landmark}", city_map))
                continue
            case 3:
                menu.show_route()
                print("Deseja remover um ponto? (0 para cancelar)")
                delete = int(input(""))
                if delete == 0 or delete > len(waypoints):
                    continue
                waypoints.pop(delete - 1)
                menu.waypoints_travelling.pop(delete - 1)
                print("Ponto removido com sucesso")
                continue
            case 0:
                break
            case _:
                print("Selecione uma opção valida")

    if initial_state is None or len(waypoints) == 0:
        print("Rota incompleta. Configure um ponto de início e ao menos uma parada.")
        exit()

    menu.waypoints_travelling.insert(0, initial)
    ucs = UniformCostSearch()
    all_actions = []
    full_path = [initial_state] + waypoints


    for i in range(len(full_path) - 1):
        start_state = full_path[i]
        goal_state = full_path[i + 1]
        problem = WaypointsShortestPathProblem(start_state, goal_state, waypoints, city_map)
        ucs.solve(problem)
        all_actions += ucs.actions
        total_explorados += ucs.num_states_explored


    print_path([initial_state] + all_actions, [], city_map)
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu.show_route()
    sleep(5)
    plot_map(city_map, [initial_state] + all_actions, waypoint_tags=[], map_name="Shortest Path Visualization")
'''
if __name__ == "__main__":

    city_map = create_bg_map()

    tests = [
        ("landmark=ufmt-biblioteca", ["landmark=banco_brasil"],                                          "landmark=madre-marta"),
        ("landmark=ufmt-biblioteca", ["landmark=prefeitura"],                                            "landmark=aguas_quentes"),
        ("landmark=ufmt-biblioteca", ["landmark=banco_brasil", "landmark=prefeitura"],                   "landmark=madre-marta"),
        ("landmark=ufmt-biblioteca", ["landmark=banco_brasil", "landmark=prefeitura"],                   "landmark=aguas_quentes"),
        ("landmark=ufmt-biblioteca", ["landmark=banco_brasil", "landmark=prefeitura", "landmark=forum"], "landmark=aguas_quentes"),
        ("landmark=madre-marta",     ["landmark=prefeitura"],                                            "landmark=aguas_quentes"),
        ("landmark=madre-marta",     ["landmark=forum", "landmark=banco_brasil"],                        "landmark=mirante_cristo"),
        ("landmark=forum",           ["landmark=prefeitura"],                                            "landmark=cachoeira_usina"),
        ("landmark=prefeitura",      ["landmark=banco_brasil", "landmark=forum"],                        "landmark=aguas_quentes"),
        ("landmark=banco_brasil",    ["landmark=mirante_cristo"],                                        "landmark=cachoeira_usina"),
    ]

    print("\n" + "=" * 150)
    print(f"{'ORIGEM':22} {'WAYPOINTS':38} {'DESTINO':22} {'UCS NÓS':10} {'A* NÓS':10} {'UCS(s)':12} {'A*(s)':12} {'CUSTO(m)':10}")
    print("=" * 150)

    total_ucs_nodes = 0
    total_astar_nodes = 0
    total_ucs_time = 0
    total_astar_time = 0

    for origin_tag, waypoint_tags, destination_tag in tests:
        start     = location_from_tag(origin_tag,      city_map)
        waypoints = [location_from_tag(w, city_map) for w in waypoint_tags]
        end       = location_from_tag(destination_tag, city_map)
        full_path = [start] + waypoints + [end]

        # UCS
        ucs        = UniformCostSearch()
        ucs_nodes  = 0
        ucs_cost   = 0.0
        t0 = perf_counter()
        for i in range(len(full_path) - 1):
            problem = WaypointsShortestPathProblem(full_path[i], full_path[i + 1], waypoints, city_map)
            ucs.solve(problem)
            ucs_nodes += ucs.num_states_explored
            ucs_cost  += ucs.path_cost
        ucs_time = perf_counter() - t0

        # A*
        astar       = AStar()
        astar_nodes = 0
        t0 = perf_counter()
        for i in range(len(full_path) - 1):
            problem = WaypointsShortestPathProblem(full_path[i], full_path[i + 1], waypoints, city_map)
            astar.solve(problem)
            astar_nodes += astar.num_states_explored
        astar_time = perf_counter() - t0

        total_ucs_nodes   += ucs_nodes
        total_astar_nodes += astar_nodes
        total_ucs_time    += ucs_time
        total_astar_time  += astar_time

        wp_str = " → ".join(w.replace("landmark=", "") for w in waypoint_tags)
        print(
            f"{origin_tag.replace('landmark=',''):22} "
            f"{wp_str:38} "
            f"{destination_tag.replace('landmark=',''):22} "
            f"{ucs_nodes:<10} "
            f"{astar_nodes:<10} "
            f"{ucs_time:<12.6f} "
            f"{astar_time:<12.6f} "
            f"{ucs_cost:<10.2f}"
        )

    n = len(tests)
    reduction = ((total_ucs_nodes - total_astar_nodes) / total_ucs_nodes) * 100

    print("=" * 150)
    print(f"\nMÉDIAS:")
    print(f"  UCS  -> Nós explorados: {total_ucs_nodes/n:.2f}  | Tempo médio: {total_ucs_time/n:.6f}s")
    print(f"  A*   -> Nós explorados: {total_astar_nodes/n:.2f}  | Tempo médio: {total_astar_time/n:.6f}s")
    print(f"\n  Redução média de nós explorados pelo A*: {reduction:.2f}%")