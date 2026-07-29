class OrdemServico:

    def __init__(
        self,
        numero_os: int,
        cliente_id: int,
        veiculo_id: int,
        data_abertura: str,
        problema_relatado: str,
        data_fechamento: str | None = None,
        diagnostico: str = "",
        valor_mao_obra: float = 0.0,
        valor_pecas: float = 0.0,
        valor_total: float = 0.0,
        forma_pagamento: str = "",
        status: str = "Aberta",
        observacoes: str = "",
        id_os: int | None = None
    ):

        self.id_os = id_os
        self.numero_os = numero_os
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id

        self.data_abertura = data_abertura
        self.data_fechamento = data_fechamento

        self.problema_relatado = problema_relatado
        self.diagnostico = diagnostico

        self.valor_mao_obra = valor_mao_obra
        self.valor_pecas = valor_pecas
        self.valor_total = valor_total

        self.forma_pagamento = forma_pagamento
        self.status = status
        self.observacoes = observacoes

        # Campos apenas para exibição
        self.cliente = None
        self.veiculo = None

        # Listas dos itens
        self.itens_servico = []
        self.itens_peca = []

    def __repr__(self):

        return (
            f"OrdemServico("
            f"id={self.id_os}, "
            f"numero={self.numero_os}, "
            f"cliente_id={self.cliente_id}, "
            f"veiculo_id={self.veiculo_id}, "
            f"status='{self.status}', "
            f"valor_total={self.valor_total})"
        )