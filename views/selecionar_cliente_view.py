from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)

from repositories.cliente_repository import ClienteRepository


class SelecionarClienteView(QDialog):

    def __init__(self):
        super().__init__()

        self.repository = ClienteRepository()
        self.cliente = None

        self.carregar_ui()
        self.configurar_tabela()
        self.configurar_eventos()
        self.carregar_clientes()


    def carregar_ui(self):
        loader = QUiLoader()
        arquivo = QFile("ui/selecionar_cliente.ui")

        if not arquivo.open(QFile.ReadOnly):
            raise RuntimeError(
                "Não foi possível abrir ui/selecionar_cliente.ui"
            )

        self.janela = loader.load(arquivo)
        arquivo.close()

        if self.janela is None:
            raise RuntimeError(
                "Não foi possível carregar ui/selecionar_cliente.ui"
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

        self.janela.tblClientes.doubleClicked.connect(
            self.confirmar
        )


    def configurar_tabela(self):
        tabela = self.janela.tblClientes

        tabela.setColumnCount(4)

        tabela.setHorizontalHeaderLabels([
            "ID",
            "Nome",
            "Telefone",
            "CPF"
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
            QHeaderView.Stretch
        )

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )


    def carregar_clientes(self):
        clientes = self.repository.listar()

        self.preencher_tabela(clientes)


    def pesquisar(self, texto=""):
        texto = texto.strip()

        if texto:
            clientes = self.repository.pesquisar(texto)
        else:
            clientes = self.repository.listar()

        self.preencher_tabela(clientes)


    def preencher_tabela(self, clientes):
        tabela = self.janela.tblClientes

        tabela.setRowCount(0)

        for cliente in clientes:
            linha = tabela.rowCount()
            tabela.insertRow(linha)

            valores = [
                str(cliente.id_cliente),
                cliente.nome or "",
                cliente.telefone or "",
                cliente.cpf or ""
            ]

            for coluna, valor in enumerate(valores):
                tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )


    def confirmar(self, *args):
        tabela = self.janela.tblClientes
        linha = tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um cliente."
            )
            return

        item_id = tabela.item(linha, 0)

        if item_id is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Não foi possível identificar o cliente selecionado."
            )
            return

        id_cliente = int(item_id.text())

        self.cliente = self.repository.buscar_por_id(
            id_cliente
        )

        if self.cliente is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "O cliente selecionado não foi encontrado."
            )
            return

        self.janela.accept()


    def exec(self):
        return self.janela.exec()