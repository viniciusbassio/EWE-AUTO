from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (getSampleStyleSheet, ParagraphStyle)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)


class OrdemServicoPDF:

    def __init__(self):
        self.pasta_saida = (
            Path(__file__).resolve().parent
            / "gerados"
        )

        self.pasta_saida.mkdir(
            parents=True,
            exist_ok=True
        )

        self.estilos = getSampleStyleSheet()

        self.estilo_titulo = ParagraphStyle(
            name="TituloOS",
            parent=self.estilos["Title"],
            alignment=TA_CENTER,
            fontSize=16,
            leading=20,
            spaceAfter=8
        )

        self.estilo_subtitulo = ParagraphStyle(
            name="SubtituloOS",
            parent=self.estilos["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=6,
            spaceAfter=4
        )

        self.estilo_normal = ParagraphStyle(
            name="TextoOS",
            parent=self.estilos["Normal"],
            fontSize=9,
            leading=12
        )

        self.estilo_total = ParagraphStyle(
            name="TotalOS",
            parent=self.estilos["Normal"],
            alignment=TA_RIGHT,
            fontSize=10,
            leading=13
        )

    def formatar_moeda(self, valor: float) -> str:
        valor = valor or 0.0

        valor_formatado = (
            f"{valor:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        return f"R$ {valor_formatado}"

    def formatar_data_hora(self, valor) -> str:
        if not valor:
            return ""

        if isinstance(valor, datetime):
            return valor.strftime(
                "%d/%m/%Y %H:%M"
            )

        texto = str(valor).strip()

        formatos_aceitos = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%d/%m/%Y"
        ]

        for formato in formatos_aceitos:
            try:
                data = datetime.strptime(
                    texto,
                    formato
                )

                return data.strftime(
                    "%d/%m/%Y %H:%M"
                )

            except ValueError:
                continue

        return texto
    
    def formatar_numero_os(self, ordem) -> str:
        ano = datetime.now().year

        if ordem.data_abertura:
            texto_data = str(ordem.data_abertura).strip()

            formatos_aceitos = [
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%d/%m/%Y"
            ]

            for formato in formatos_aceitos:
                try:
                    data_abertura = datetime.strptime(
                        texto_data,
                        formato
                    )

                    ano = data_abertura.year
                    break

                except ValueError:
                    continue

        sequencia = ordem.id_os or 0

        return f"{sequencia:04d}/{ano}"

    def gerar(
        self,
        ordem,
        cliente,
        veiculo,
        servicos,
        pecas,
        configuracao
    ) -> Path:

        numero_os_formatado = self.formatar_numero_os(ordem)
        numero_arquivo = numero_os_formatado.replace(
            "/",
            "-"
        )

        caminho_pdf = (
            self.pasta_saida
            / f"OS_{numero_arquivo}.pdf"
        )

        documento = SimpleDocTemplate(
            str(caminho_pdf),
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=12 * mm,
            bottomMargin=12 * mm
        )

        elementos = []

        logo = ""

        if configuracao.logo:
            caminho_logo = Path(
                configuracao.logo
            )

            if not caminho_logo.is_absolute():
                raiz_projeto = (
                    Path(__file__)
                    .resolve()
                    .parent
                    .parent
                )

                caminho_logo = (
                    raiz_projeto
                    / caminho_logo
                )

            if caminho_logo.exists():
                logo = Image(
                    str(caminho_logo),
                    width=35 * mm,
                    height=25 * mm,
                    kind="proportional"
                )

        cidade_estado = " - ".join(
            valor
            for valor in [
                configuracao.cidade or "",
                configuracao.estado or ""
            ]
            if valor
        )

        dados_oficina = Paragraph(
            (
                f"<b>"
                f"{configuracao.nome_oficina or ''}"
                f"</b><br/>"
                f"{configuracao.endereco or ''}<br/>"
                f"{cidade_estado}<br/>"
                f"Telefone: "
                f"{configuracao.telefone or ''}<br/>"
                f"E-mail: "
                f"{configuracao.email or ''}<br/>"
                f"CNPJ: "
                f"{configuracao.cnpj or ''}"
            ),
            self.estilo_normal
        )

        cabecalho = Table(
            [[logo, dados_oficina]],
            colWidths=[
                45 * mm,
                135 * mm
            ]
        )

        cabecalho.setStyle(
            TableStyle([
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (0, 0),
                    "CENTER"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.black
                )
            ])
        )

        elementos.append(cabecalho)
        elementos.append(
            Spacer(1, 4 * mm)
        )

        elementos.append(
            Paragraph(
                (
                    f"<b>ORDEM DE SERVIÇO Nº "
                    f"{numero_os_formatado}</b>"
                ),
                self.estilo_titulo
            )
        )

        data_abertura_formatada = (
            self.formatar_data_hora(
                ordem.data_abertura
            )
        )

        dados_os = [
            [
                Paragraph(
                    (
                        f"<b>Data de abertura:</b> "
                        f"{data_abertura_formatada}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>Status:</b> "
                        f"{ordem.status or ''}"
                    ),
                    self.estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Forma de pagamento:</b> "
                        f"{ordem.forma_pagamento or ''}"
                    ),
                    self.estilo_normal
                ),
                ""
            ]
        ]

        tabela_dados_os = Table(
            dados_os,
            colWidths=[
                90 * mm,
                90 * mm
            ]
        )

        tabela_dados_os.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        elementos.append(tabela_dados_os)
        elementos.append(
            Spacer(1, 5 * mm)
        )

        elementos.append(
            Paragraph(
                "DADOS DO CLIENTE",
                self.estilo_subtitulo
            )
        )

        dados_cliente = [
            [
                Paragraph(
                    (
                        f"<b>Nome:</b> "
                        f"{cliente.nome or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>Telefone:</b> "
                        f"{cliente.telefone or ''}"
                    ),
                    self.estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>CPF:</b> "
                        f"{cliente.cpf or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                (
                    f"<b>Endereço:</b> "
                    f"{getattr(cliente, 'endereco', '') or ''}"
                ),
                self.estilo_normal
                )
            ]
        ]

        tabela_cliente = Table(
            dados_cliente,
            colWidths=[
                90 * mm,
                90 * mm
            ]
        )

        tabela_cliente.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        elementos.append(tabela_cliente)
        elementos.append(
            Spacer(1, 4 * mm)
        )

        elementos.append(
            Paragraph(
                "DADOS DO VEÍCULO",
                self.estilo_subtitulo
            )
        )

        dados_veiculo = [
            [
                Paragraph(
                    (
                        f"<b>Placa:</b> "
                        f"{veiculo.placa or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>Marca:</b> "
                        f"{veiculo.marca or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>Modelo:</b> "
                        f"{veiculo.modelo or ''}"
                    ),
                    self.estilo_normal
                )
            ],
            [
                Paragraph(
                    (
                        f"<b>Ano:</b> "
                        f"{veiculo.ano or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>Cor:</b> "
                        f"{veiculo.cor or ''}"
                    ),
                    self.estilo_normal
                ),
                Paragraph(
                    (
                        f"<b>KM:</b> "
                        f"{getattr(veiculo, 'km', '') or ''}"
                    ),
                    self.estilo_normal
                )
            ]
        ]

        tabela_veiculo = Table(
            dados_veiculo,
            colWidths=[
                60 * mm,
                60 * mm,
                60 * mm
            ]
        )

        tabela_veiculo.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        elementos.append(tabela_veiculo)
        elementos.append(
            Spacer(1, 4 * mm)
        )

        elementos.append(
            Paragraph(
                "PROBLEMA RELATADO",
                self.estilo_subtitulo
            )
        )

        tabela_problema = Table(
            [[
                Paragraph(
                    ordem.problema_relatado or "",
                    self.estilo_normal
                )
            ]],
            colWidths=[180 * mm]
        )

        tabela_problema.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        elementos.append(tabela_problema)

        elementos.append(
            Paragraph(
                "DIAGNÓSTICO",
                self.estilo_subtitulo
            )
        )

        tabela_diagnostico = Table(
            [[
                Paragraph(
                    ordem.diagnostico or "",
                    self.estilo_normal
                )
            ]],
            colWidths=[180 * mm]
        )

        tabela_diagnostico.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        elementos.append(tabela_diagnostico)

        if servicos:
            elementos.append(
                Paragraph(
                    "SERVIÇOS",
                    self.estilo_subtitulo
                )
            )

            dados_servicos = [[
                "Descrição",
                "Qtd.",
                "Valor unitário",
                "Total"
            ]]

            for item in servicos:
                servico = item["servico"]
                quantidade = item["quantidade"]
                valor_unitario = item["valor_unitario"]
                valor_total = item["valor_total"]

                dados_servicos.append([
                    Paragraph(
                        servico.descricao or "",
                        self.estilo_normal
                    ),
                    str(quantidade),
                    self.formatar_moeda(
                        valor_unitario
                    ),
                    self.formatar_moeda(
                        valor_total
                    )
                ])

            tabela_servicos = Table(
                dados_servicos,
                colWidths=[
                    90 * mm,
                    20 * mm,
                    35 * mm,
                    35 * mm
                ],
                repeatRows=1
            )

            tabela_servicos.setStyle(
                self._estilo_tabela_itens()
            )

            elementos.append(
                tabela_servicos
            )

        if pecas:
            elementos.append(
                Paragraph(
                    "PEÇAS",
                    self.estilo_subtitulo
                )
            )

            dados_pecas = [[
                "Descrição",
                "Qtd.",
                "Valor unitário",
                "Total"
            ]]

            for item in pecas:
                peca = item["peca"]
                quantidade = item["quantidade"]
                valor_unitario = item["valor_unitario"]
                valor_total = item["valor_total"]

                dados_pecas.append([
                    Paragraph(
                        peca.descricao or "",
                        self.estilo_normal
                    ),
                    str(quantidade),
                    self.formatar_moeda(
                        valor_unitario
                    ),
                    self.formatar_moeda(
                        valor_total
                    )
                ])

            tabela_pecas = Table(
                dados_pecas,
                colWidths=[
                    90 * mm,
                    20 * mm,
                    35 * mm,
                    35 * mm
                ],
                repeatRows=1
            )

            tabela_pecas.setStyle(
                self._estilo_tabela_itens()
            )

            elementos.append(
                tabela_pecas
            )

        elementos.append(
            Spacer(1, 5 * mm)
        )

        dados_totais = [
            [
                "Mão de obra:",
                self.formatar_moeda(
                    ordem.valor_mao_obra
                )
            ],
            [
                "Peças:",
                self.formatar_moeda(
                    ordem.valor_pecas
                )
            ],
            [
                "TOTAL:",
                self.formatar_moeda(
                    ordem.valor_total
                )
            ]
        ]

        tabela_totais = Table(
            dados_totais,
            colWidths=[
                40 * mm,
                40 * mm
            ],
            hAlign="RIGHT"
        )

        tabela_totais.setStyle(
            TableStyle([
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.25,
                    colors.grey
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "RIGHT"
                ),
                (
                    "FONTNAME",
                    (0, 2),
                    (-1, 2),
                    "Helvetica-Bold"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        elementos.append(
            tabela_totais
        )

        elementos.append(
            Spacer(1, 15 * mm)
        )

        assinaturas = Table(
            [
                [
                    "__________________________________",
                    "__________________________________"
                ],
                [
                    "Assinatura do cliente",
                    (
                        configuracao.nome_oficina
                        or "Oficina"
                    )
                ]
            ],
            colWidths=[
                90 * mm,
                90 * mm
            ]
        )

        assinaturas.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, 1),
                    "Helvetica"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9
                )
            ])
        )

        elementos.append(
            assinaturas
        )

        documento.build(
            elementos
        )

        return caminho_pdf

    def _estilo_tabela_itens(self) -> TableStyle:
        return TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.25,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "RIGHT"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])