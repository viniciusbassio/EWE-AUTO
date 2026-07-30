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
from repositories.servico_repository import ServicoRepository


class SelecionarServicoView(QDialog):

    def __init__(self, repository=None):
        super().__init__()

        self.repository = repository or ServicoRepository()

        self.servico = None
        self.quantidade = 1

        self.carregar_ui()
        self.configurar_tabela()
        self.configurar_eventos()
        self.carregar()


    def carregar_ui(self):
        loader = QUiLoader()
        arquivo = QFile(caminho_recurso("ui/selecionar_servico.ui"))

        if not arquivo.open(QFile.ReadOnly):
            raise RuntimeError(
                "Não foi possível abrir ui/selecionar_servico.ui"
            )

        self.janela = loader.load(arquivo)
        arquivo.close()

        if self.janela is None:
            raise RuntimeError(
                "Não foi possível carregar ui/selecionar_servico.ui"
            )


    def configurar_eventos(self):
        self.janela.btnCancelar.clicked.connect(
            self.janela.reject
        )

        self.janela.btnAdicionar.clicked.connect(
            self.confirmar
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar
        )

        self.janela.tblServicos.doubleClicked.connect(
            self.confirmar
        )


    def configurar_tabela(self):
        tabela = self.janela.tblServicos

        tabela.setColumnCount(3)

        tabela.setHorizontalHeaderLabels([
            "ID",
            "Descrição",
            "Valor"
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
        tabela.setSortingEnabled(True)

        tabela.verticalHeader().setVisible(False)

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )


    def carregar(self):
        try:
            servicos = self.repository.listar()

            self.preencher(servicos)

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro",
                str(erro)
            )


    def pesquisar(self, texto=""):
        texto = texto.strip()

        try:
            if texto:
                servicos = self.repository.pesquisar(texto)
            else:
                servicos = self.repository.listar()

            self.preencher(servicos)

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro",
                str(erro)
            )


    def preencher(self, servicos):
        tabela = self.janela.tblServicos

        tabela.setSortingEnabled(False)
        tabela.setRowCount(0)

        for servico in servicos:
            linha = tabela.rowCount()
            tabela.insertRow(linha)

            valores = [
                str(servico.id_servico),
                servico.descricao or "",
                f"R$ {servico.valor_padrao:.2f}"
            ]

            for coluna, valor in enumerate(valores):
                tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )

        tabela.setSortingEnabled(True)
        tabela.sortItems(1)


    def obter_selecionado(self):
        tabela = self.janela.tblServicos
        linha = tabela.currentRow()

        if linha < 0:
            return None

        item_id = tabela.item(linha, 0)

        if item_id is None:
            return None

        return int(item_id.text())


    def confirmar(self, *args):
        id_servico = self.obter_selecionado()

        if id_servico is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um serviço."
            )
            return

        self.servico = self.repository.buscar_por_id(
            id_servico
        )

        if self.servico is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "O serviço selecionado não foi encontrado."
            )
            return

        self.quantidade = self.janela.spnQuantidade.value()

        self.janela.accept()


    def exec(self):
        return self.janela.exec()