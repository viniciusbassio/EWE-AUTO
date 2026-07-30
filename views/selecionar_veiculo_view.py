from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)
from utils.recursos import caminho_recurso
from repositories.veiculo_repository import VeiculoRepository


class SelecionarVeiculoView(QDialog):

    def __init__(self, cliente_id):
        super().__init__()

        self.repository = VeiculoRepository()
        self.cliente_id = cliente_id
        self.veiculo = None

        self.carregar_ui()
        self.configurar_tabela()
        self.configurar_eventos()
        self.carregar()


    def carregar_ui(self):
        loader = QUiLoader()
        arquivo = QFile(caminho_recurso("ui/selecionar_veiculo.ui"))

        if not arquivo.open(QFile.ReadOnly):
            raise RuntimeError(
                "Não foi possível abrir ui/selecionar_veiculo.ui"
            )

        self.janela = loader.load(arquivo)
        arquivo.close()

        if self.janela is None:
            raise RuntimeError(
                "Não foi possível carregar ui/selecionar_veiculo.ui"
            )


    def configurar_eventos(self):
        self.janela.btnCancelar.clicked.connect(
            self.janela.reject
        )

        self.janela.btnSelecionar.clicked.connect(
            self.confirmar
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar
        )

        self.janela.tblVeiculos.doubleClicked.connect(
            self.confirmar
        )


    def configurar_tabela(self):
        tabela = self.janela.tblVeiculos

        tabela.setColumnCount(5)

        tabela.setHorizontalHeaderLabels([
            "ID",
            "Placa",
            "Marca",
            "Modelo",
            "Ano"
        ])

        tabela.setColumnHidden(0, True)

        tabela.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        tabela.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        tabela.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        tabela.setAlternatingRowColors(True)

        tabela.verticalHeader().setVisible(False)

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        tabela.horizontalHeader().setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )


    def carregar(self):
        veiculos = self.repository.listar_por_cliente(
            self.cliente_id
        )

        self.preencher(veiculos)


    def pesquisar(self, texto=""):
        texto = texto.strip()

        if texto:
            veiculos = self.repository.pesquisar_por_cliente(
                self.cliente_id,
                texto
            )
        else:
            veiculos = self.repository.listar_por_cliente(
                self.cliente_id
            )

        self.preencher(veiculos)


    def preencher(self, veiculos):
        tabela = self.janela.tblVeiculos

        tabela.setRowCount(0)

        for veiculo in veiculos:
            linha = tabela.rowCount()
            tabela.insertRow(linha)

            valores = [
                str(veiculo.id_veiculo),
                veiculo.placa or "",
                veiculo.marca or "",
                veiculo.modelo or "",
                str(veiculo.ano or "")
            ]

            for coluna, valor in enumerate(valores):
                tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )


    def confirmar(self, *args):
        tabela = self.janela.tblVeiculos
        linha = tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um veículo."
            )
            return

        item_id = tabela.item(linha, 0)

        if item_id is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Não foi possível identificar o veículo selecionado."
            )
            return

        id_veiculo = int(item_id.text())

        self.veiculo = self.repository.buscar_por_id(
            id_veiculo
        )

        if self.veiculo is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "O veículo selecionado não foi encontrado."
            )
            return

        self.janela.accept()


    def exec(self):
        return self.janela.exec()