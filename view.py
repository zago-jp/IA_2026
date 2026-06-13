import json

#---------------- Menu de interação com o usuário ---------------#
class Menu:
    # Construtor
    def __init__(self, option_saved:int = -1) -> None:
        self.option = option_saved             # Ponto inicial selecionado
        self.waypoints_travelling = []         # Lista de paradas exibidas no menu
        self.algorithm = "ucs"                 # Algoritmo padrão de busca
        return
    
    # Exibe o menu principal
    def show_menu(self) -> None:
        print("Selecione uma das seguintes opções:")

        # Define os textos de status da rota e do algoritmo
        ponto_atual = "Sem ponto de largada." if self.option == -1 else self.option
        algoritmo_atual = "UCS" if self.algorithm == "ucs" else "A*"
        
        # Lista as opções disponíveis
        print(f"1 - Adicionar inicio: {ponto_atual}")
        print(f"2 - Adicionar parada:")
        print(f"3 - Remover parada:")
        print(f"4 - Algoritmo de busca: {algoritmo_atual}")
        print("0 - Realizar Rota: ")

    # Exibe o menu de escolha do algoritmo
    def show_menu_algorithm(self) -> None:
        print("\nSelecione o algoritmo de busca:")
        print("1 - UCS (Uniform Cost Search)")
        print("2 - A* (A-Star)")
    
    # Exibe os pontos de interesse disponíveis
    def show_menu_dot(self) -> None:
        # Carrega os landmarks do arquivo JSON
        with open("data/bg-landmarks.json") as file:
            landmarks = json.load(file)

        # Lista todos os pontos para seleção
        print("\n\nSelecione um dos seguintes pontos de interesse:")
        i = 1
        print(f"0 - Cancelar adição")
        for i , dot in enumerate(landmarks, start=1):
            print(f"{i} - "+ dot["landmark"])


    # Exibe a rota configurada até o momento
    def show_route(self) -> None:
        print("Ver a rota atual")
        
        # Lista os pontos na ordem de visita
        for i, waypoint in enumerate(self.waypoints_travelling, start=1):
            print(f"{i}º - {waypoint}")

#---------------- Teste local do menu ---------------#
if __name__ == "__main__":
    # Cria o menu
    menu = Menu()
    
    # Exibe o menu principal e a lista de pontos
    menu.show_menu()
    menu.show_menu_dot()
