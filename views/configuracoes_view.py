import shutil
from pathlib import Path
from utils.recursos import caminho_recurso
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox
)

from models.configuracao import Configuracao
from repositories.configuracao_repository import ConfiguracaoRepository


class ConfiguracoesView:

    def __init__(self):
        loader = QUiLoader()

        arquivo = QFile(caminho_recurso("ui/configuracoes.ui"))
        arquivo.open(QFile.ReadOnly)

        self.janela = loader.load(arquivo)

        arquivo.close()

        self.repository = ConfiguracaoRepository()
        self.caminho_logo_selecionada = None

        self.janela.btnSelecionarLogo.clicked.connect(
            self.selecionar_logo
        )

        self.janela.btnSalvar.clicked.connect(
            self.salvar
        )

        self.janela.btnCancelar.clicked.connect(
            self.janela.reject
        )

        self.carregar_configuracao()

    def carregar_configuracao(self):
        configuracao = self.repository.buscar()

        if configuracao is None:
            self.janela.txtNomeOficina.setText(
                "EWE Centro Automotivo"
            )
            return

        self.janela.txtNomeOficina.setText(
            configuracao.nome_oficina or ""
        )

        self.janela.txtCnpj.setText(
            configuracao.cnpj or ""
        )

        self.janela.txtTelefone.setText(
            configuracao.telefone or ""
        )

        self.janela.txtEndereco.setText(
            configuracao.endereco or ""
        )

        self.janela.txtCidade.setText(
            configuracao.cidade or ""
        )

        self.janela.txtEstado.setText(
            configuracao.estado or ""
        )

        self.janela.txtEmail.setText(
            configuracao.email or ""
        )

        self.janela.txtLogo.setText(
            configuracao.logo or ""
        )

    def selecionar_logo(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self.janela,
            "Selecionar logo da oficina",
            "",
            (
                "Imagens (*.png *.jpg *.jpeg);;"
                "Todos os arquivos (*.*)"
            )
        )

        if not caminho:
            return

        self.caminho_logo_selecionada = Path(caminho)

        self.janela.txtLogo.setText(
            str(self.caminho_logo_selecionada)
        )

    def copiar_logo(self) -> str:
        if self.caminho_logo_selecionada is None:
            return self.janela.txtLogo.text().strip()

        raiz_projeto = Path(__file__).resolve().parent.parent
        pasta_assets = raiz_projeto / "assets"

        pasta_assets.mkdir(
            parents=True,
            exist_ok=True
        )

        extensao = (
            self.caminho_logo_selecionada
            .suffix
            .lower()
        )

        if extensao not in [".png", ".jpg", ".jpeg"]:
            extensao = ".png"

        destino = (
            pasta_assets
            / f"logo_empresa{extensao}"
        )

        origem_resolvida = (
            self.caminho_logo_selecionada.resolve()
        )

        destino_resolvido = destino.resolve()

        if origem_resolvida != destino_resolvido:
            shutil.copy2(
                origem_resolvida,
                destino_resolvido
            )

        return str(
            Path("assets")
            / destino.name
        )

    def salvar(self):
        nome_oficina = (
            self.janela.txtNomeOficina
            .text()
            .strip()
        )

        if not nome_oficina:
            QMessageBox.warning(
                self.janela,
                "Atenção",
                "Informe o nome da oficina."
            )
            return

        try:
            caminho_logo = self.copiar_logo()

            configuracao = Configuracao(
                id_configuracao=1,
                nome_oficina=nome_oficina,
                cnpj=self.janela.txtCnpj.text().strip(),
                telefone=self.janela.txtTelefone.text().strip(),
                endereco=self.janela.txtEndereco.text().strip(),
                cidade=self.janela.txtCidade.text().strip(),
                estado=(
                    self.janela.txtEstado
                    .text()
                    .strip()
                    .upper()
                ),
                email=self.janela.txtEmail.text().strip(),
                logo=caminho_logo
            )

            self.repository.salvar(
                configuracao
            )

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Configurações salvas com sucesso!"
            )

            self.janela.accept()

        except Exception as erro:
            QMessageBox.critical(
                self.janela,
                "Erro",
                (
                    "Não foi possível salvar as "
                    f"configurações.\n\n{erro}"
                )
            )

    def exec(self):
        return self.janela.exec()