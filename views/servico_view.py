from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import (
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from utils.recursos import caminho_recurso
from repositories.servico_repository import ServicoRepository
from views.servico_form_view import ServicoFormView


class ServicosView:

    def __init__(self):

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/servicos.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.configurar_tabela()

        self.janela.btnFechar.clicked.connect(
            self.janela.close
        )

        self.janela.btnNovo.clicked.connect(
            self.abrir_novo_servico
        )

        self.janela.btnEditar.clicked.connect(
            self.editar_servico
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar_servicos
        )

        self.janela.btnExcluir.clicked.connect(
            self.excluir_servico
        )

        self.carregar_servicos()


    def configurar_tabela(self):

        tabela = self.janela.tblServicos

        # Esconde coluna ID
        tabela.setColumnHidden(0, True)

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )  # Descrição

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )  # Valor

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )  # Observações


    def abrir_novo_servico(self):

        self.form_servico = ServicoFormView()

        self.form_servico.exec()

        self.carregar_servicos()


    def carregar_servicos(self):

        repository = ServicoRepository()

        servicos = repository.listar()

        self.preencher_tabela(servicos)


    def pesquisar_servicos(self):

        texto = self.janela.txtPesquisar.text()

        repository = ServicoRepository()

        servicos = repository.pesquisar(texto)

        self.preencher_tabela(servicos)


    def preencher_tabela(self, servicos):

        tabela = self.janela.tblServicos

        tabela.setRowCount(0)

        for servico in servicos:

            linha = tabela.rowCount()

            tabela.insertRow(linha)

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(servico.id_servico)
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    servico.descricao
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    f"R$ {servico.valor_padrao:.2f}"
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    servico.observacoes or ""
                )
            )


    def editar_servico(self):

        linha = self.janela.tblServicos.currentRow()

        if linha < 0:
            return

        id_servico = self.janela.tblServicos.item(
            linha,
            0
        ).text()

        repository = ServicoRepository()

        servico = repository.buscar_por_id(
            int(id_servico)
        )

        if servico:

            self.form_servico = ServicoFormView(servico)

            self.form_servico.exec()

            self.carregar_servicos()


    def excluir_servico(self):

        linha = self.janela.tblServicos.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um serviço para excluir."
            )

            return

        id_servico = self.janela.tblServicos.item(
            linha,
            0
        ).text()

        descricao = self.janela.tblServicos.item(
            linha,
            1
        ).text()

        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja realmente excluir o serviço '{descricao}'?"
        )

        if resposta == QMessageBox.Yes:

            repository = ServicoRepository()

            repository.excluir(
                int(id_servico)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Serviço excluído com sucesso!"
            )

            self.carregar_servicos()


    def exec(self):

        self.janela.exec()