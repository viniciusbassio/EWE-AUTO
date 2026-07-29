from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)

from repositories.peca_repository import PecaRepository


class SelecionarPecaView(QDialog):

    def __init__(self, repository=None):
        super().__init__()

        self.repository = repository or PecaRepository()

        self.peca = None
        self.quantidade = 1

        self.carregar_ui()
        self.configurar_tabela()
        self.configurar_eventos()
        self.carregar()


    def carregar_ui(self):
        loader = QUiLoader()
        arquivo = QFile("ui/selecionar_peca.ui")

        if not arquivo.open(QFile.ReadOnly):
            raise RuntimeError(
                "Não foi possível abrir ui/selecionar_peca.ui"
            )

        self.janela = loader.load(arquivo)
        arquivo.close()

        if self.janela is None:
            raise RuntimeError(
                "Não foi possível carregar ui/selecionar_peca.ui"
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

        self.janela.tblPecas.doubleClicked.connect(
            self.confirmar
        )


    def configurar_tabela(self):
        tabela = self.janela.tblPecas

        tabela.setColumnCount(4)

        tabela.setHorizontalHeaderLabels([
            "ID",
            "Descrição",
            "Marca",
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
            QHeaderView.Stretch
        )

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )


    def carregar(self):
        try:
            pecas = self.repository.listar()

            self.preencher(pecas)

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
                pecas = self.repository.pesquisar(texto)
            else:
                pecas = self.repository.listar()

            self.preencher(pecas)

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro",
                str(erro)
            )


    def preencher(self, pecas):
        tabela = self.janela.tblPecas

        tabela.setSortingEnabled(False)
        tabela.setRowCount(0)

        for peca in pecas:
            linha = tabela.rowCount()
            tabela.insertRow(linha)

            valores = [
                str(peca.id_peca),
                peca.descricao or "",
                peca.marca or "",
                f"R$ {peca.valor:.2f}"
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
        tabela = self.janela.tblPecas
        linha = tabela.currentRow()

        if linha < 0:
            return None

        item_id = tabela.item(linha, 0)

        if item_id is None:
            return None

        return int(item_id.text())


    def confirmar(self, *args):
        id_peca = self.obter_selecionado()

        if id_peca is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione uma peça."
            )
            return

        self.peca = self.repository.buscar_por_id(
            id_peca
        )

        if self.peca is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "A peça selecionada não foi encontrada."
            )
            return

        self.quantidade = self.janela.spnQuantidade.value()

        self.janela.accept()


    def exec(self):
        return self.janela.exec()