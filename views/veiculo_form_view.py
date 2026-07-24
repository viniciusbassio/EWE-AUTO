from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from models.veiculo import Veiculo
from repositories.veiculo_repository import VeiculoRepository
from repositories.cliente_repository import ClienteRepository


class VeiculoFormView:

    def __init__(self, veiculo=None):

        self.veiculo = veiculo

        loader = QUiLoader()

        arquivo = QFile("ui/veiculo_form.ui")
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.repository = VeiculoRepository()

        self.cliente_repository = ClienteRepository()

        self.carregar_clientes()

        self.janela.btnCancelar.clicked.connect(
            self.janela.reject
        )

        self.janela.btnSalvar.clicked.connect(
            self.salvar
        )

        if self.veiculo:
            self.carregar_veiculo()


    def carregar_clientes(self):

        clientes = self.cliente_repository.listar()

        for cliente in clientes:

            self.janela.cmbCliente.addItem(
                cliente.nome,
                cliente.id_cliente
            )


    def carregar_veiculo(self):

        indice = self.janela.cmbCliente.findData(
            self.veiculo.cliente_id
        )

        if indice >= 0:

            self.janela.cmbCliente.setCurrentIndex(
                indice
            )

        self.janela.txtPlaca.setText(
            self.veiculo.placa
        )

        self.janela.txtMarca.setText(
            self.veiculo.marca
        )

        self.janela.txtModelo.setText(
            self.veiculo.modelo
        )

        self.janela.spnAno.setValue(
            self.veiculo.ano or 1900
        )

        self.janela.txtCor.setText(
            self.veiculo.cor or ""
        )

        self.janela.spnKm.setValue(
            self.veiculo.km or 0
        )

        self.janela.txtMotor.setText(
            self.veiculo.motor or ""
        )

        indice = self.janela.cmbCombustivel.findText(
            self.veiculo.combustivel or ""
        )

        if indice >= 0:

            self.janela.cmbCombustivel.setCurrentIndex(
                indice
            )


    def salvar(self):

        cliente_id = self.janela.cmbCliente.currentData()

        placa = self.janela.txtPlaca.text().strip()

        marca = self.janela.txtMarca.text().strip()

        modelo = self.janela.txtModelo.text().strip()

        if not placa:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "A placa é obrigatória."
            )

            return

        if not marca:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "A marca é obrigatória."
            )

            return

        if not modelo:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "O modelo é obrigatório."
            )

            return


        if self.veiculo:

            self.veiculo.cliente_id = cliente_id
            self.veiculo.placa = placa
            self.veiculo.marca = marca
            self.veiculo.modelo = modelo
            self.veiculo.ano = self.janela.spnAno.value()
            self.veiculo.cor = self.janela.txtCor.text().strip()
            self.veiculo.km = self.janela.spnKm.value()
            self.veiculo.motor = self.janela.txtMotor.text().strip()
            self.veiculo.combustivel = (
                self.janela.cmbCombustivel.currentText()
            )

            self.repository.atualizar(
                self.veiculo
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Veículo atualizado com sucesso!"
            )

        else:

            veiculo = Veiculo(
                cliente_id=cliente_id,
                placa=placa,
                marca=marca,
                modelo=modelo,
                ano=self.janela.spnAno.value(),
                cor=self.janela.txtCor.text().strip(),
                km=self.janela.spnKm.value(),
                motor=self.janela.txtMotor.text().strip(),
                combustivel=self.janela.cmbCombustivel.currentText()
            )

            self.repository.inserir(
                veiculo
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Veículo cadastrado com sucesso!"
            )

        self.janela.accept()


    def exec(self):

        self.janela.exec()