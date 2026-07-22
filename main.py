from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from database.inicializar_banco import inicializar_banco


def main():
    # Garante que o banco exista
    inicializar_banco()

    app = QApplication([])

    arquivo = QFile("ui/main_window.ui")
    arquivo.open(QFile.ReadOnly)

    loader = QUiLoader()
    janela = loader.load(arquivo)

    arquivo.close()

    janela.show()

    app.exec()


if __name__ == "__main__":
    main()