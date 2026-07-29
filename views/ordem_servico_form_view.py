from datetime import datetime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QMessageBox
)
from repositories.ordem_servico_repository import OrdemServicoRepository
from repositories.item_servico_repository import ItemServicoRepository
from repositories.item_peca_repository import ItemPecaRepository
from views.selecionar_servico_view import SelecionarServicoView
from views.selecionar_peca_view import SelecionarPecaView
from views.selecionar_cliente_view import SelecionarClienteView
from views.selecionar_veiculo_view import SelecionarVeiculoView
from models.ordem_servico import OrdemServico
from models.item_servico import ItemServico
from models.item_peca import ItemPeca
from repositories.cliente_repository import ClienteRepository
from repositories.veiculo_repository import VeiculoRepository
from repositories.servico_repository import ServicoRepository
from repositories.peca_repository import PecaRepository

class OrdemServicoFormView(QDialog):

    def __init__(self, ordem=None):

        super().__init__()

        loader = QUiLoader()

        arquivo = QFile(
            "ui/ordem_servico_form.ui"
        )

        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo,  self)

        arquivo.close()

        self.janela.cmbStatus.clear()

        self.janela.cmbStatus.addItems([
            "Aberta",
            "Em andamento",
            "Finalizada",
            "Entregue",
            "Cancelada"
        ])

        self.janela.cmbPagamento.clear()

        self.janela.cmbPagamento.addItems([
            "",
            "Dinheiro",
            "Pix",
            "Cartão de débito",
            "Cartão de crédito",
            "Transferência"
        ])

        self.ordem = ordem

        if self.ordem is not None:
            self.janela.setWindowTitle(f"Editar Ordem de Serviço Nº {self.ordem.numero_os}")
        else:
            self.janela.setWindowTitle("Nova Ordem de Serviço")

        self.servicos = []
        self.pecas = []
        self.cliente = None
        self.veiculo = None
        self.ordem_repository = OrdemServicoRepository()
        self.item_servico_repository = ItemServicoRepository()
        self.item_peca_repository = ItemPecaRepository()
        self.cliente_repository = ClienteRepository()
        self.veiculo_repository = VeiculoRepository()
        self.servico_repository = ServicoRepository()
        self.peca_repository = PecaRepository()

        self.janela.btnCancelar.clicked.connect(self.janela.reject)
        self.janela.btnSalvar.clicked.connect(self.salvar)
        self.janela.btnAdicionarServico.clicked.connect(self.adicionar_servico)
        self.janela.btnAdicionarPeca.clicked.connect(self.adicionar_peca)
        self.janela.btnRemoverServico.clicked.connect(self.remover_servico)
        self.janela.btnRemoverPeca.clicked.connect(self.remover_peca)
        self.janela.btnSelecionarCliente.clicked.connect(self.selecionar_cliente)
        self.janela.btnSelecionarVeiculo.clicked.connect(self.selecionar_veiculo)

        if self.ordem is not None:
            self.carregar_ordem()



    def adicionar_servico(self):
        tela = SelecionarServicoView()
        if tela.exec():
            self.servicos.append(
                {   "servico": tela.servico,
                    "quantidade": tela.quantidade
                }
            )
            self.atualizar_servicos()

    def adicionar_peca(self):
        tela = SelecionarPecaView()
        if tela.exec():
            self.pecas.append(
                {   "peca": tela.peca,
                    "quantidade": tela.quantidade
                }
            )
            self.atualizar_pecas()



    def atualizar_servicos(self):

        tabela = self.janela.tblServicos
        tabela.setRowCount(0)

        for item in self.servicos:

            linha = tabela.rowCount()
            tabela.insertRow(linha)

            servico = item["servico"]
            quantidade = item["quantidade"]

            valor_total = (
                servico.valor_padrao *
                quantidade
            )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    servico.descricao
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(quantidade)
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
                    f"R$ {valor_total:.2f}"
                )
            )

        self.calcular_total()

    def atualizar_pecas(self):

        tabela = self.janela.tblPecas
        tabela.setRowCount(0)

        for item in self.pecas:

            linha = tabela.rowCount()
            tabela.insertRow(linha)

            peca = item["peca"]
            quantidade = item["quantidade"]

            valor_total = (
                peca.valor *
                quantidade
            )

            tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    peca.descricao
                )
            )

            tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(quantidade)
                )
            )

            tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    f"R$ {peca.valor:.2f}"
                )
            )

            tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    f"R$ {valor_total:.2f}"
                )
            )

        self.calcular_total()
    
    def remover_servico(self):

        linha = (
            self.janela.tblServicos.currentRow()
        )

        if linha >= 0:

            self.servicos.pop(linha)

            self.atualizar_servicos()



    def remover_peca(self):

        linha = (
            self.janela.tblPecas.currentRow()
        )

        if linha >= 0:

            self.pecas.pop(linha)

            self.atualizar_pecas()



    def calcular_total(self):

        valor_servicos = sum(
            item["servico"].valor_padrao *
            item["quantidade"]
            for item in self.servicos
        )


        valor_pecas = sum(
            item["peca"].valor *
            item["quantidade"]
            for item in self.pecas
        )


        total = (
            valor_servicos +
            valor_pecas
        )


        self.janela.lblValorServicos.setText(
            f"R$ {valor_servicos:.2f}"
        )


        self.janela.lblValorPecas.setText(
            f"R$ {valor_pecas:.2f}"
        )


        self.janela.lblValorTotal.setText(
            f"R$ {total:.2f}"
        )

    def salvar(self):

        if self.cliente is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um cliente."
            )
            return

        if self.veiculo is None:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um veículo."
            )
            return

        problema = (
            self.janela.txtProblema
            .toPlainText()
            .strip()
        )

        if not problema:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Informe o problema relatado."
            )
            return

        if not self.servicos and not self.pecas:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Adicione pelo menos um serviço ou uma peça."
            )
            return

        diagnostico = (
            self.janela.txtDiagnostico
            .toPlainText()
            .strip()
        )

        status = (
            self.janela.cmbStatus
            .currentText()
            .strip()
        )

        forma_pagamento = (
            self.janela.cmbPagamento
            .currentText()
            .strip()
        )

        valor_servicos = sum(
            item["servico"].valor_padrao
            * item["quantidade"]
            for item in self.servicos
        )

        valor_pecas = sum(
            item["peca"].valor
            * item["quantidade"]
            for item in self.pecas
        )

        valor_total = valor_servicos + valor_pecas

        try:
            agora = datetime.now()

            if self.ordem is None:
                numero_os = int(
                    agora.strftime("%Y%m%d%H%M%S")
                )

                data_abertura = agora.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                id_os = None
                data_fechamento = None
                observacoes = ""

            else:
                numero_os = self.ordem.numero_os
                data_abertura = self.ordem.data_abertura
                id_os = self.ordem.id_os
                data_fechamento = self.ordem.data_fechamento
                observacoes = self.ordem.observacoes or ""

            ordem = OrdemServico(
                id_os=id_os,
                numero_os=numero_os,
                cliente_id=self.cliente.id_cliente,
                veiculo_id=self.veiculo.id_veiculo,
                data_abertura=data_abertura,
                data_fechamento=data_fechamento,
                problema_relatado=problema,
                diagnostico=diagnostico,
                valor_mao_obra=valor_servicos,
                valor_pecas=valor_pecas,
                valor_total=valor_total,
                forma_pagamento=forma_pagamento,
                status=status,
                observacoes=observacoes
            )

            if self.ordem is None:
                id_ordem_servico = (
                    self.ordem_repository.inserir(
                        ordem
                    )
                )

            else:
                id_ordem_servico = self.ordem.id_os

                self.ordem_repository.atualizar(
                    ordem
                )

                self.item_servico_repository.excluir_por_os(
                    id_ordem_servico
                )

                self.item_peca_repository.excluir_por_os(
                    id_ordem_servico
                )

            for item in self.servicos:
                servico = item["servico"]
                quantidade = item["quantidade"]

                valor_unitario = servico.valor_padrao
                valor_total_item = (
                    valor_unitario * quantidade
                )

                item_servico = ItemServico(
                    os_id=id_ordem_servico,
                    servico_id=servico.id_servico,
                    quantidade=quantidade,
                    valor_unitario=valor_unitario,
                    valor_total=valor_total_item
                )

                self.item_servico_repository.inserir(
                    item_servico
                )

            for item in self.pecas:
                peca = item["peca"]
                quantidade = item["quantidade"]

                valor_unitario = peca.valor
                valor_total_item = (
                    valor_unitario * quantidade
                )

                item_peca = ItemPeca(
                    os_id=id_ordem_servico,
                    peca_id=peca.id_peca,
                    quantidade=quantidade,
                    valor_unitario=valor_unitario,
                    valor_total=valor_total_item
                )

                self.item_peca_repository.inserir(
                    item_peca
                )

            mensagem = (
                "Ordem de serviço atualizada com sucesso."
                if self.ordem
                else "Ordem de serviço salva com sucesso."
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                mensagem
            )

            self.janela.accept()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro",
                (
                    "Não foi possível salvar a ordem "
                    f"de serviço.\n\n{erro}"
                )
            )

    def carregar_ordem(self):

        self.cliente = self.cliente_repository.buscar_por_id(
            self.ordem.cliente_id
        )

        self.veiculo = self.veiculo_repository.buscar_por_id(
            self.ordem.veiculo_id
        )

        if self.cliente:
            self.janela.txtCliente.setText(
                self.cliente.nome or ""
            )

        if self.veiculo:
            self.janela.txtVeiculo.setText(
                (
                    f"{self.veiculo.marca or ''} "
                    f"{self.veiculo.modelo or ''} - "
                    f"{self.veiculo.placa or ''}"
                ).strip()
            )

        self.janela.txtProblema.setPlainText(
            self.ordem.problema_relatado or ""
        )

        self.janela.txtDiagnostico.setPlainText(
            self.ordem.diagnostico or ""
        )

        self.janela.cmbStatus.setCurrentText(
            self.ordem.status or "Aberta"
        )

        self.janela.cmbPagamento.setCurrentText(
            self.ordem.forma_pagamento or ""
        )

        self.servicos = []

        itens_servico = (
            self.item_servico_repository
            .listar_por_os(self.ordem.id_os)
        )

        for item in itens_servico:

            servico = self.servico_repository.buscar_por_id(
                item.servico_id
            )

            if servico:
                self.servicos.append({
                    "servico": servico,
                    "quantidade": item.quantidade
                })

        self.pecas = []

        itens_peca = (
            self.item_peca_repository
            .listar_por_os(self.ordem.id_os)
        )

        for item in itens_peca:

            peca = self.peca_repository.buscar_por_id(
                item.peca_id
            )

            if peca:
                self.pecas.append({
                    "peca": peca,
                    "quantidade": item.quantidade
                })

        self.atualizar_servicos()
        self.atualizar_pecas()

    def exec(self):

        return self.janela.exec()

    def selecionar_cliente(self):

        tela = SelecionarClienteView()

        if tela.exec():

            self.cliente = tela.cliente

            self.janela.txtCliente.setText(
                self.cliente.nome
            )

            self.veiculo = None

            self.janela.txtVeiculo.clear()

    def selecionar_veiculo(self):

        if not self.cliente:
        
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Selecione um cliente primeiro."
            )
    
            return
    
    
        tela = SelecionarVeiculoView(
            self.cliente.id_cliente
        )
    
    
        if tela.exec():
        
            self.veiculo = tela.veiculo
    
            self.janela.txtVeiculo.setText(
                f"{self.veiculo.marca} {self.veiculo.modelo} - {self.veiculo.placa}"
            )