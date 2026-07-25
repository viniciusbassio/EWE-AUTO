from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)

from repositories.peca_repository import PecaRepository
from views.peca_form_view import PecaFormView


class PecasView:

    def __init__(self):

        loader = QUiLoader()

        arquivo = QFile("ui/pecas.ui")
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.configurar_tabela()

        self.janela.btnFechar.clicked.connect(
            self.janela.close
        )

        self.janela.btnNovo.clicked.connect(
            self.abrir_nova_peca
        )

        self.janela.btnEditar.clicked.connect(
            self.editar_peca
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar_pecas
        )

        self.janela.btnExcluir.clicked.connect(
            self.excluir_peca
        )

        self.carregar_pecas()


    def configurar_tabela(self):

        tabela = self.janela.tblPecas

        tabela.setColumnHidden(0, True)

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )  # Descrição

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )  # Marca

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )  # Valor


    def abrir_nova_peca(self):

        self.form_peca = PecaFormView()

        self.form_peca.exec()

        self.carregar_pecas()


    def carregar_pecas(self):

        repository = PecaRepository()

        pecas = repository.listar()

        self.preencher_tabela(pecas)


    def pesquisar_pecas(self):

        texto = self.janela.txtPesquisar.text()

        repository = PecaRepository()

        pecas = repository.pesquisar(texto)

        self.preencher_tabela(pecas)


    def preencher_tabela(self, pecas):

        tabela = self.janela.tblPecas

        tabela.setRowCount(0)

        for peca in pecas:

            linha = tabela.rowCount()

            tabela.insertRow(linha)

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(peca.id_peca)
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    peca.descricao
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    peca.marca or ""
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    f"R$ {peca.valor:.2f}"
                )
            )


    def editar_peca(self):

        linha = self.janela.tblPecas.currentRow()

        if linha < 0:
            return

        id_peca = self.janela.tblPecas.item(
            linha,
            0
        ).text()

        repository = PecaRepository()

        peca = repository.buscar_por_id(
            int(id_peca)
        )

        if peca:

            self.form_peca = PecaFormView(peca)

            self.form_peca.exec()

            self.carregar_pecas()


    def excluir_peca(self):

        linha = self.janela.tblPecas.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione uma peça para excluir."
            )
            return

        id_peca = self.janela.tblPecas.item(
            linha,
            0
        ).text()

        descricao = self.janela.tblPecas.item(
            linha,
            1
        ).text()

        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja realmente excluir a peça '{descricao}'?"
        )

        if resposta == QMessageBox.Yes:

            repository = PecaRepository()

            repository.excluir(
                int(id_peca)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Peça excluída com sucesso!"
            )

            self.carregar_pecas()


    def exec(self):
  
        self.janela.exec()