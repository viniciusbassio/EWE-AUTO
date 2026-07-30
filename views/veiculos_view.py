from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from utils.recursos import caminho_recurso
from repositories.veiculo_repository import VeiculoRepository
from views.veiculo_form_view import VeiculoFormView


class VeiculosView:

    def __init__(self):

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/veiculos.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.configurar_tabela()

        self.janela.btnFechar.clicked.connect(
            self.janela.close
        )

        self.janela.btnNovo.clicked.connect(
            self.abrir_novo_veiculo
        )

        self.janela.btnEditar.clicked.connect(
            self.editar_veiculo
        )

        self.janela.btnExcluir.clicked.connect(
            self.excluir_veiculo
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar_veiculos
        )

        self.carregar_veiculos()


    def configurar_tabela(self):

        tabela = self.janela.tblVeiculos

        tabela.setColumnHidden(0, True)

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )  # Cliente

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )  # Placa

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )  # Marca

        tabela.horizontalHeader().setSectionResizeMode(
            4,
            QHeaderView.Stretch
        )  # Modelo

        tabela.horizontalHeader().setSectionResizeMode(
            5,
            QHeaderView.ResizeToContents
        )  # Ano

        tabela.horizontalHeader().setSectionResizeMode(
            6,
            QHeaderView.ResizeToContents
        )  # Cor

        tabela.horizontalHeader().setSectionResizeMode(
            7,
            QHeaderView.ResizeToContents
        )  # KM

        tabela.horizontalHeader().setSectionResizeMode(
            8,
            QHeaderView.ResizeToContents
        )  # Motor

        tabela.horizontalHeader().setSectionResizeMode(
            9,
            QHeaderView.ResizeToContents
        )  # Combustível


    def abrir_novo_veiculo(self):

        self.form_veiculo = VeiculoFormView()

        self.form_veiculo.exec()

        self.carregar_veiculos()


    def carregar_veiculos(self):

        repository = VeiculoRepository()

        veiculos = repository.listar()

        self.preencher_tabela(veiculos)


    def pesquisar_veiculos(self):

        texto = self.janela.txtPesquisar.text()

        repository = VeiculoRepository()

        veiculos = repository.pesquisar(texto)

        self.preencher_tabela(veiculos)


    def preencher_tabela(self, veiculos):

        tabela = self.janela.tblVeiculos

        tabela.setRowCount(0)

        for veiculo in veiculos:

            linha = tabela.rowCount()

            tabela.insertRow(linha)

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(veiculo.id_veiculo)
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(veiculo.cliente)
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    veiculo.placa
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    veiculo.marca
                )
            )

            tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    veiculo.modelo
                )
            )

            tabela.setItem(
                linha,
                5,
                QTableWidgetItem(
                    str(veiculo.ano or "")
                )
            )

            tabela.setItem(
                linha,
                6,
                QTableWidgetItem(
                    veiculo.cor or ""
                )
            )

            tabela.setItem(
                linha,
                7,
                QTableWidgetItem(
                    str(veiculo.km or "")
                )
            )

            tabela.setItem(
                linha,
                8,
                QTableWidgetItem(
                    veiculo.motor or ""
                )
            )

            tabela.setItem(
                linha,
                9,
                QTableWidgetItem(
                    veiculo.combustivel or ""
                )
            )


    def editar_veiculo(self):

        linha = self.janela.tblVeiculos.currentRow()

        if linha < 0:
            return

        id_veiculo = self.janela.tblVeiculos.item(
            linha,
            0
        ).text()

        repository = VeiculoRepository()

        veiculo = repository.buscar_por_id(
            int(id_veiculo)
        )

        if veiculo:

            self.form_veiculo = VeiculoFormView(
                veiculo
            )

            self.form_veiculo.exec()

            self.carregar_veiculos()


    def excluir_veiculo(self):

        linha = self.janela.tblVeiculos.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um veículo para excluir."
            )

            return

        id_veiculo = self.janela.tblVeiculos.item(
            linha,
            0
        ).text()

        placa = self.janela.tblVeiculos.item(
            linha,
            2
        ).text()

        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja realmente excluir o veículo {placa}?"
        )

        if resposta == QMessageBox.Yes:

            repository = VeiculoRepository()

            repository.excluir(
                int(id_veiculo)
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Veículo excluído com sucesso!"
            )

            self.carregar_veiculos()


    def exec(self):

        self.janela.exec()