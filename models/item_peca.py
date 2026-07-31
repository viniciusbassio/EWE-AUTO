from typing import Optional

class ItemPeca:

    def __init__(
        self,
        os_id: int,
        peca_id: int,
        quantidade: float = 1,
        valor_unitario: float = 0.0,
        valor_total: float = 0.0,
        id_item_peca: Optional[int] = None
    ):

        self.id_item_peca = id_item_peca
        self.os_id = os_id
        self.peca_id = peca_id

        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total

        # Apenas para exibição
        self.descricao_peca = None

    def __repr__(self):

        return (
            f"ItemPeca("
            f"id={self.id_item_peca}, "
            f"peca_id={self.peca_id}, "
            f"qtd={self.quantidade}, "
            f"valor={self.valor_total})"
        )