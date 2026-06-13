import json

class Menu:
    def __init__(self, option_saved:int = -1) -> None:
        self.option = option_saved
        self.waypoints_travelling = []
        self.algorithm = "ucs"
        return
    """
    @param inicio: Ponto de partida da rota, Deve ser criado antes e passado conforme é a funçao é chamada
    """
    def show_menu(self) -> None:
        print("Selecione uma das seguintes opções:")

        ponto_atual = "Sem ponto de largada." if self.option == -1 else self.option
        algoritmo_atual = "UCS" if self.algorithm == "ucs" else "A*"
        print(f"1 - Adicionar inicio: {ponto_atual}")
        print(f"2 - Adicionar parada:")
        print(f"3 - Remover parada:")
        print(f"4 - Algoritmo de busca: {algoritmo_atual}")
        print("0 - Realizar Rota: ")

    """
    Não utiliza parâmetros, toda a logica deve ser implementada fora.
    funçao de propósito unico!!! Qualquer reutilização solicitara manutenção
    """
    
    def show_menu_algorithm(self) -> None:
        print("\nSelecione o algoritmo de busca:")
        print("1 - UCS (Uniform Cost Search)")
        print("2 - A* (A-Star)")
        
    def show_menu_dot(self) -> None:
        with open("data/bg-landmarks.json") as file:
            landmarks = json.load(file)

        print("\n\nSelecione um dos seguintes pontos de interesse:")
        i = 1
        print(f"0 - Cancelar adição")
        for i , dot in enumerate(landmarks, start=1):
            print(f"{i} - "+ dot["landmark"])


    def show_route(self) -> None:
        print("Ver a rota atual")
        for i, waypoint in enumerate(self.waypoints_travelling, start=1):
            print(f"{i}º - {waypoint}")

if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()
    menu.show_menu_dot()