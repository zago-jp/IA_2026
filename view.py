import json

class Menu:
    def __init__(self, option_saved:int = -1) -> None:
        self.option = option_saved
        return
    """
    @param inicio: Ponto de partida da rota, Deve ser criado antes e passado conforme é a funçao é chamada
    """
    def show_menu(self) -> None:
        print("Selecione uma das seguintes opções:")

        print(f"1 - Adicionar inicio: {"Sem ponto de largada." if self.option == -1 else self.option}")
        print(f"2 - Adicionar parada:")

        print("0 - Realizar Rota: ")

    """
    Não utiliza parâmetros, toda a logica deve ser implementada fora.
    funçao de propósito unico!!! Qualquer reutilização solicitara manutenção
    """
    def show_menu_dot(self) -> None:
        with open("data/bg-landmarks.json") as file:
            landmarks = json.load(file)

        print("\n\nSelecione um dos seguintes pontos de interesse:")
        i = 1
        print(f"0 - Cancelar adição")
        for i , dot in enumerate(landmarks, start=1):
            print(f"{i} - "+ dot["landmark"])

if __name__ == "__main__":
    Menu = Menu()
    Menu.show_menu()
    Menu.show_menu_dot()