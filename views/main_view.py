from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.clientes_view import ClientesView


class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        arquivo = QFile("ui/main_window.ui")
        arquivo.open(QFile.ReadOnly)

        self.ui = loader.load(arquivo, self)

        arquivo.close()

        self.setCentralWidget(self.ui.centralWidget())
        self.setWindowTitle("EWE Auto - Sistema para Oficinas")

        self.ui.btnClientes.clicked.connect(self.abrir_clientes)

    def abrir_clientes(self):
        tela = ClientesView()
        tela.exec()