from PySide2.QtWidgets import QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from utils.recursos import caminho_recurso
from views.clientes_view import ClientesView
from views.veiculos_view import VeiculosView
from views.pecas_view import PecasView
from views.servico_view import ServicosView
from views.ordens_servico_view import OrdensServicoView
from views.configuracoes_view import ConfiguracoesView

class MainView(QMainWindow):

    def __init__(self):
        super().__init__()

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/main_window.ui"))
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

        self.ui.btnServicos.clicked.connect(
            self.abrir_servicos
        )

        self.ui.btnOrdemServico.clicked.connect(
            self.abrir_ordens_servico
        )
        self.ui.btnConfiguracoes.clicked.connect(
            self.abrir_configuracoes
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


    def abrir_servicos(self):

        tela = ServicosView()

        tela.exec()


    def abrir_ordens_servico(self):

        tela = OrdensServicoView()

        tela.exec()

    def abrir_configuracoes(self):
        self.configuracoes_view = ConfiguracoesView()
        self.configuracoes_view.exec()