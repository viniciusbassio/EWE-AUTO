from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QMessageBox
from utils.recursos import caminho_recurso
from models.servico import Servico
from repositories.servico_repository import ServicoRepository
from typing import Optional

class ServicoFormView:

    def __init__(self, servico: Optional[Servico] = None):

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/servico_form.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.servico = servico

        self.janela.btnSalvar.clicked.connect(
            self.salvar
        )

        self.janela.btnCancelar.clicked.connect(
            self.janela.close
        )

        if self.servico:
            self.carregar_dados()


    def carregar_dados(self):

        self.janela.txtDescricao.setText(
            self.servico.descricao
        )

        self.janela.spnValorPadrao.setValue(
            self.servico.valor_padrao
        )

        self.janela.txtObservacoes.setPlainText(
            self.servico.observacoes or ""
        )


    def salvar(self):

        descricao = self.janela.txtDescricao.text().strip()

        valor_padrao = self.janela.spnValorPadrao.value()

        observacoes = self.janela.txtObservacoes.toPlainText().strip()


        if not descricao:

            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Informe a descrição do serviço."
            )
            return


        repository = ServicoRepository()


        if self.servico is None:

            servico = Servico(
                descricao=descricao,
                valor_padrao=valor_padrao,
                observacoes=observacoes
            )

            repository.inserir(servico)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Serviço cadastrado com sucesso!"
            )

        else:

            self.servico.descricao = descricao
            self.servico.valor_padrao = valor_padrao
            self.servico.observacoes = observacoes

            repository.atualizar(self.servico)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Serviço atualizado com sucesso!"
            )


        self.janela.accept()


    def exec(self):

        self.janela.exec()