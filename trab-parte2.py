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


#---------------- Problema de menor caminho com pontos de parada ---------------#
class WaypointsShortestPathProblem(SearchProblem):
    # Construtor
    def __init__(self, start_state:str|None, goal_state:str, waypoints: list[set[str]], city_map:CityMap):
        # Inicializa o problema com estado inicial e estado objetivo
        super().__init__(initial_state=State(start_state), goal_state = State(goal_state))
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
        geo_goal   = self.city_map.geo_locations[self.goal_state.location]
        
        # Estimativa heurística baseada na distância geográfica
        return compute_distance(geo_actual, geo_goal)

#---------------- Execução interativa e visualização dos resultados ---------------#
if __name__ == "__main__":
    
    # Cria o mapa de Barra do Garças
    city_map = create_bg_map()
    
    # Inicializa o menu e as estruturas da rota
    menu = Menu()
    initial_state = None       # Estado inicial escolhido pelo usuário
    waypoints = []             # Lista de paradas intermediárias
    op = -1                    # Opção atual do menu
    initial = None             # Nome do ponto inicial para exibição

    # Loop principal do menu
    while op != 0:
        
        # Exibe as opções disponíveis
        menu.show_menu()
        
        # Lê a opção escolhida pelo usuário
        op = int(input(""))
        
        match op:
            case 1:
                # Seleciona o ponto inicial
                menu.show_menu_dot()
                new_start = int(input(""))
                
                # Converte a opção escolhida em landmark
                landmark = location_from_tag_id(new_start, city_map)["landmark"]
                
                # Busca o estado inicial no mapa
                initial_state = location_from_tag(f"landmark={landmark}", city_map)
                initial = landmark
                
                # Guarda a opção selecionada no menu
                menu.option = new_start
                continue
            case 2:
                # Adiciona uma nova parada intermediária
                menu.show_menu_dot()
                new_end = int(input(""))
                
                # Cancela a seleção da parada
                if new_end == 0:
                    continue
                
                # Converte a opção escolhida em landmark
                landmark = location_from_tag_id(new_end, city_map)["landmark"]
                
                # Registra a parada no menu e na lista de estados
                menu.waypoints_travelling.append(landmark)
                waypoints.append(location_from_tag(f"landmark={landmark}", city_map))
                continue
            case 3:
                # Exibe a rota configurada
                menu.show_route()
                print("Deseja remover um ponto? (0 para cancelar)")
                delete = int(input(""))
                
                # Cancela se a opção for inválida ou zero
                if delete == 0 or delete > len(waypoints):
                    continue
                
                # Remove a parada selecionada
                waypoints.pop(delete - 1)
                menu.waypoints_travelling.pop(delete - 1)
                print("Ponto removido com sucesso")
                continue
            case 4:
                # Seleciona o algoritmo de busca
                menu.show_menu_algorithm()
                alg_choice = int(input(""))
                
                # Define UCS como algoritmo
                if alg_choice == 1:
                    menu.algorithm = "ucs"
                    
                # Define A* como algoritmo
                elif alg_choice == 2:
                    menu.algorithm = "astar"
                else:
                    print("Opção inválida")
                continue
            case 0:
                # Encerra o menu
                break
            case _:
                # Trata opções não reconhecidas
                print("Selecione uma opção valida")

    # Valida se a rota possui início e ao menos uma parada
    if initial_state is None or len(waypoints) == 0:
        print("Rota incompleta. Configure um ponto de início e ao menos uma parada.")
        exit()

    # Inclui o ponto inicial na lista de exibição da rota
    menu.waypoints_travelling.insert(0, initial)
    
    # Instancia o algoritmo escolhido
    if menu.algorithm == "ucs":
        solver = UniformCostSearch()
    else:
        solver = AStar()
        
    all_actions = []                   # Caminho completo calculado entre todas as paradas
    full_path = [initial_state] + waypoints

    # Calcula o menor caminho entre cada par consecutivo da rota
    for i in range(len(full_path) - 1):
        start_state = full_path[i]
        goal_state  = full_path[i + 1]
        
        # Cria o problema para o trecho atual
        problem = WaypointsShortestPathProblem(start_state, goal_state, waypoints, city_map)
        
        # Executa a busca no trecho
        solver.solve(problem)
        
        # Acumula as ações encontradas
        all_actions += solver.actions


    # Imprime o caminho textual no terminal
    print_path([initial_state] + all_actions, [], city_map)
    sleep(2)
    
    # Limpa o terminal antes de exibir a rota final
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Exibe a rota escolhida no menu
    menu.show_route()
    sleep(5)
    
    # Gera a visualização gráfica do caminho encontrado
    plot_map(city_map, [initial_state] + all_actions, waypoint_tags=[], map_name="Shortest Path Visualization")
