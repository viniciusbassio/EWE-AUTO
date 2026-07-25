from PySide6.QtWidgets import QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from views.clientes_view import ClientesView
from views.veiculos_view import VeiculosView
from views.pecas_view import PecasView

class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        arquivo = QFile("ui/main_window.ui")
        arquivo.open(QFile.ReadOnly)

        self.ui = loader.load(arquivo, self)

        arquivo.close()

        self.setCentralWidget(
            self.ui.centralWidget()
        )

        self.setWindowTitle(
            "EWE Auto - Sistema para Oficinas"
        )

        self.ui.btnClientes.clicked.connect(
            self.abrir_clientes
        )

        self.ui.btnVeiculos.clicked.connect(
            self.abrir_veiculos
        )

        self.ui.btnPecas.clicked.connect(
            self.abrir_pecas
        )


    def abrir_clientes(self):

        tela = ClientesView()

        tela.exec()


    def abrir_veiculos(self):

        tela = VeiculosView()

        tela.exec()

    def abrir_pecas(self):
        tela = PecasView()

        tela.exec()