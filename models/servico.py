class Servico:

    def __init__(
        self,
        descricao: str,
        valor_padrao: float,
        observacoes: str = "",
        id_servico: int | None = None
    ):
        self.id_servico = id_servico
        self.descricao = descricao
        self.valor_padrao = valor_padrao
        self.observacoes = observacoes

    def __repr__(self):
        return (
            f"Servico("
            f"id={self.id_servico}, "
            f"descricao='{self.descricao}', "
            f"valor_padrao={self.valor_padrao}, "
            f"observacoes='{self.observacoes}')"
        )