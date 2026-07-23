from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtWidgets import QMessageBox
from repositories.cliente_repository import ClienteRepository
from views.cliente_form_view import ClienteFormView


class ClientesView:

    def __init__(self):

        loader = QUiLoader()

        arquivo = QFile("ui/clientes.ui")
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.configurar_tabela()

        self.janela.btnFechar.clicked.connect(
            self.janela.close
        )

        self.janela.btnNovo.clicked.connect(
            self.abrir_novo_cliente
        )

        self.janela.btnEditar.clicked.connect(
            self.editar_cliente
        )

        self.janela.txtPesquisar.textChanged.connect(
            self.pesquisar_clientes
        )

        self.janela.btnExcluir.clicked.connect(
            self.excluir_cliente
        )
        

        self.carregar_clientes()


    def configurar_tabela(self):

        tabela = self.janela.tblClientes

        # Esconde coluna ID
        tabela.setColumnHidden(0, True)

        # Ajusta largura das colunas

        tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )  # Nome

        tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )  # Telefone

        tabela.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )  # CPF

        tabela.horizontalHeader().setSectionResizeMode(
            4,
            QHeaderView.Stretch
        )  # Endereço

        tabela.horizontalHeader().setSectionResizeMode(
            5,
            QHeaderView.Stretch
        )  # Observações


    def abrir_novo_cliente(self):

        self.form_cliente = ClienteFormView()

        self.form_cliente.exec()

        # Atualiza lista após cadastro
        self.carregar_clientes()


    def carregar_clientes(self):

        repository = ClienteRepository()

        clientes = repository.listar()

        self.preencher_tabela(clientes)


    def pesquisar_clientes(self):

        texto = self.janela.txtPesquisar.text()

        repository = ClienteRepository()

        clientes = repository.pesquisar(texto)

        self.preencher_tabela(clientes)


    def preencher_tabela(self, clientes):

        tabela = self.janela.tblClientes

        tabela.setRowCount(0)

        for cliente in clientes:

            linha = tabela.rowCount()

            tabela.insertRow(linha)

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(cliente.id_cliente)
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    cliente.nome
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    cliente.telefone or ""
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    cliente.cpf or ""
                )
            )

            tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    cliente.endereco or ""
                )
            )

            tabela.setItem(
                linha,
                5,
                QTableWidgetItem(
                    cliente.observacoes or ""
                )
            )

    def editar_cliente(self):

        linha = self.janela.tblClientes.currentRow()

        if linha < 0:
            return

        id_cliente = self.janela.tblClientes.item(
            linha,
            0
        ).text()

        repository = ClienteRepository()

        cliente = repository.buscar_por_id(
            int(id_cliente)
        )

        if cliente:

            self.form_cliente = ClienteFormView(cliente)

            self.form_cliente.exec()

            self.carregar_clientes()

    def excluir_cliente(self):
    
        linha = self.janela.tblClientes.currentRow()
    
        if linha < 0:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um cliente para excluir."
            )
            return
    
    
        id_cliente = self.janela.tblClientes.item(
            linha,
            0
        ).text()
    
    
        nome_cliente = self.janela.tblClientes.item(
        linha,
        1
        ).text()


        resposta = QMessageBox.question(
            self.janela,
            "Confirmar exclusão",
            f"Deseja realmente excluir o cliente {nome_cliente}?"
        )
    
    
        if resposta == QMessageBox.Yes:
        
            repository = ClienteRepository()
    
            repository.excluir(
                int(id_cliente)
            )
    
    
            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Cliente excluído com sucesso!"
            )
    
    
            self.carregar_clientes()
    def exec(self):

        self.janela.exec()