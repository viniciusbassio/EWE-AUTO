class Peca:

    def __init__(
        self,
        descricao: str,
        marca: str = "",
        valor: float = 0.0,
        id_peca: int | None = None
    ):
        self.id_peca = id_peca
        self.descricao = descricao
        self.marca = marca
        self.valor = valor

    def __repr__(self):
        return (
            f"Peca("
            f"id={self.id_peca}, "
            f"descricao='{self.descricao}', "
            f"marca='{self.marca}', "
            f"valor={self.valor})"
        )