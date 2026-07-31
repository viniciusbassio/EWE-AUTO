from PySide2.QtWidgets import QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from utils.recursos import caminho_recurso
from models.peca import Peca
from repositories.peca_repository import PecaRepository


class PecaFormView:

    def __init__(self, peca=None):

        self.peca = peca

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/peca_form.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.repository = PecaRepository()

        self.janela.btnCancelar.clicked.connect(
            self.janela.reject
        )

        self.janela.btnSalvar.clicked.connect(
            self.salvar
        )

        if self.peca:
            self.carregar_peca()


    def carregar_peca(self):

        self.janela.txtDescricao.setText(
            self.peca.descricao
        )

        self.janela.txtMarca.setText(
            self.peca.marca or ""
        )

        self.janela.spnValor.setValue(
            self.peca.valor
        )


    def salvar(self):

        descricao = self.janela.txtDescricao.text().strip()

        if not descricao:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "A descrição da peça é obrigatória."
            )
            return

        if self.peca:

            self.peca.descricao = descricao
            self.peca.marca = self.janela.txtMarca.text().strip()
            self.peca.valor = self.janela.spnValor.value()

            self.repository.atualizar(self.peca)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Peça atualizada com sucesso!"
            )

        else:

            peca = Peca(
                descricao=descricao,
                marca=self.janela.txtMarca.text().strip(),
                valor=self.janela.spnValor.value()
            )

            self.repository.inserir(peca)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Peça cadastrada com sucesso!"
            )

        self.janela.accept()


    def exec(self):
        self.janela.exec()