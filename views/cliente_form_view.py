from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from utils.recursos import caminho_recurso
from models.cliente import Cliente
from repositories.cliente_repository import ClienteRepository


class ClienteFormView:

    def __init__(self, cliente=None):

        self.cliente = cliente

        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/cliente_form.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.repository = ClienteRepository()

        self.janela.btnCancelar.clicked.connect(
        self.janela.reject
        )

        self.janela.btnSalvar.clicked.connect(
            self.salvar
        )

        if self.cliente:
            self.carregar_cliente()


    def carregar_cliente(self):

        self.janela.txtNome.setText(
            self.cliente.nome
        )

        self.janela.txtTelefone.setText(
            self.cliente.telefone or ""
        )

        self.janela.txtCpf.setText(
            self.cliente.cpf or ""
        )

        self.janela.txtEndereco.setText(
            self.cliente.endereco or ""
        )

        self.janela.txtObservacoes.setPlainText(
            self.cliente.observacoes or ""
        )


    def salvar(self):

        nome = self.janela.txtNome.text().strip()

        if not nome:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "O nome do cliente é obrigatório."
            )
            return


        if self.cliente:

            # Atualização

            self.cliente.nome = nome
            self.cliente.telefone = (
                self.janela.txtTelefone.text().strip()
            )
            self.cliente.cpf = (
                self.janela.txtCpf.text().strip()
            )
            self.cliente.endereco = (
                self.janela.txtEndereco.text().strip()
            )
            self.cliente.observacoes = (
                self.janela.txtObservacoes.toPlainText().strip()
            )


            self.repository.atualizar(
                self.cliente
            )


            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Cliente atualizado com sucesso!"
            )


        else:

            # Novo cadastro

            cliente = Cliente(
                nome=nome,
                telefone=self.janela.txtTelefone.text().strip(),
                cpf=self.janela.txtCpf.text().strip(),
                endereco=self.janela.txtEndereco.text().strip(),
                observacoes=self.janela.txtObservacoes.toPlainText().strip()
            )


            self.repository.inserir(cliente)


            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Cliente cadastrado com sucesso!"
            )


        self.janela.accept()
    def exec(self):

        self.janela.exec()