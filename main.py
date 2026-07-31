from PySide2.QtWidgets import QApplication

from database.inicializar_banco import inicializar_banco
from views.main_view import MainView


def main():
    # Garante que o banco exista
    inicializar_banco()

    app = QApplication([])

    janela = MainView()
    janela.show()

    app.exec_()


if __name__ == "__main__":
    main()