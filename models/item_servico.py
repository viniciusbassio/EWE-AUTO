class ItemServico:

    def __init__(
        self,
        os_id: int,
        servico_id: int,
        quantidade: float = 1,
        valor_unitario: float = 0.0,
        valor_total: float = 0.0,
        id_item_servico: int | None = None
    ):

        self.id_item_servico = id_item_servico
        self.os_id = os_id
        self.servico_id = servico_id

        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total

        # Apenas para exibição
        self.descricao_servico = None

    def __repr__(self):

        return (
            f"ItemServico("
            f"id={self.id_item_servico}, "
            f"servico_id={self.servico_id}, "
            f"qtd={self.quantidade}, "
            f"valor={self.valor_total})"
        )