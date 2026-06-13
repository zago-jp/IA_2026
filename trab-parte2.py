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
            case 4:
                menu.show_menu_algorithm()
                alg_choice = int(input(""))
                if alg_choice == 1:
                    menu.algorithm = "ucs"
                elif alg_choice == 2:
                    menu.algorithm = "astar"
                else:
                    print("Opção inválida")
                continue
            case 0:
                break
            case _:
                print("Selecione uma opção valida")

    if initial_state is None or len(waypoints) == 0:
        print("Rota incompleta. Configure um ponto de início e ao menos uma parada.")
        exit()

    menu.waypoints_travelling.insert(0, initial)
    if menu.algorithm == "ucs":
        solver = UniformCostSearch()
    else:
        solver = AStar()
    all_actions = []
    full_path = [initial_state] + waypoints

    for i in range(len(full_path) - 1):
        start_state = full_path[i]
        goal_state  = full_path[i + 1]
        problem = WaypointsShortestPathProblem(start_state, goal_state, waypoints, city_map)
        solver.solve(problem)
        all_actions += solver.actions


    print_path([initial_state] + all_actions, [], city_map)
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    menu.show_route()
    sleep(5)
    plot_map(city_map, [initial_state] + all_actions, waypoint_tags=[], map_name="Shortest Path Visualization")
