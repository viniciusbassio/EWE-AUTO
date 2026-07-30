from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QAbstractItemView
)
from utils.recursos import caminho_recurso
from repositories.ordem_servico_repository import OrdemServicoRepository
from views.ordem_servico_form_view import OrdemServicoFormView


class OrdensServicoView:

    def __init__(self):

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/ordens_servico.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()


        self.repository = OrdemServicoRepository()


        self.configurar_tabela()


        self.janela.btnFechar.clicked.connect(
            self.janela.close
        )


        self.janela.btnNovo.clicked.connect(
            self.abrir_nova_ordem
        )


        self.janela.btnEditar.clicked.connect(
            self.editar_ordem
        )


        self.janela.btnExcluir.clicked.connect(
            self.excluir_ordem
        )


        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar_ordens
        )


        self.janela.tblOrdensServico.doubleClicked.connect(
            lambda: self.editar_ordem()
        )


        self.carregar_ordens()



    def configurar_tabela(self):

        tabela = self.janela.tblOrdensServico


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


        tabela.setSortingEnabled(True)



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

        tabela.horizontalHeader().setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )

        tabela.horizontalHeader().setSectionResizeMode(
            6,
            QHeaderView.ResizeToContents
        )



    def abrir_nova_ordem(self):

        self.form = OrdemServicoFormView()

        self.form.exec()

        self.carregar_ordens()



    def carregar_ordens(self):

        ordens = self.repository.listar()

        self.preencher_tabela(ordens)



    def pesquisar_ordens(self, texto=""):

        texto = texto.strip()
    
        if texto:
            ordens = self.repository.pesquisar_ordens(
                texto
            )
        else:
            ordens = self.repository.listar()
    
        self.preencher_tabela(ordens)



    def preencher_tabela(self, ordens):

        tabela = self.janela.tblOrdensServico


        tabela.setSortingEnabled(False)

        tabela.setRowCount(0)


        for ordem in ordens:

            linha = tabela.rowCount()

            tabela.insertRow(linha)


            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(ordem.id_os)
                )
            )


            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(ordem.numero_os)
                )
            )


            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    ordem.cliente or ""
                )
            )


            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    ordem.veiculo or ""
                )
            )


            tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    ordem.data_abertura
                )
            )


            tabela.setItem(
                linha,
                5,
                QTableWidgetItem(
                    ordem.status
                )
            )


            tabela.setItem(
                linha,
                6,
                QTableWidgetItem(
                    f"R$ {ordem.valor_total:.2f}"
                )
            )


        tabela.setSortingEnabled(True)



    def obter_id_selecionado(self):

        linha = self.janela.tblOrdensServico.currentRow()


        if linha < 0:
            return None


        return int(
            self.janela.tblOrdensServico.item(
                linha,
                0
            ).text()
        )



    def editar_ordem(self):

        id_os = self.obter_id_selecionado()


        if id_os is None:
            return


        ordem = self.repository.buscar_por_id(
            id_os
        )


        if ordem:

            self.form = OrdemServicoFormView(
                ordem
            )

            self.form.exec()

            self.carregar_ordens()



    def excluir_ordem(self):

        id_os = self.obter_id_selecionado()


        if id_os is None:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione uma ordem de serviço."
            )

            return



        resposta = QMessageBox.question(
            self.janela,
            "Confirmação",
            "Deseja realmente excluir esta Ordem de Serviço?"
        )


        if resposta == QMessageBox.Yes:

            self.repository.excluir(
                id_os
            )


            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Ordem de Serviço excluída com sucesso!"
            )


            self.carregar_ordens()



    def exec(self):

        self.janela.exec()