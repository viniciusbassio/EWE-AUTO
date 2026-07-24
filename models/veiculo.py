class Veiculo:

    def __init__(
        self,
        cliente_id: int,
        placa: str,
        marca: str,
        modelo: str,
        ano: int | None = None,
        cor: str = "",
        km: int = 0,
        motor: str = "",
        combustivel: str = "",
        id_veiculo: int | None = None,
        cliente: str | None = None
    ):
        self.id_veiculo = id_veiculo
        self.cliente_id = cliente_id
        self.cliente = cliente
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.km = km
        self.motor = motor
        self.combustivel = combustivel

    def __repr__(self):
        return (
            f"Veiculo("
            f"id={self.id_veiculo}, "
            f"cliente_id={self.cliente_id}, "
            f"cliente='{self.cliente}', "
            f"placa='{self.placa}', "
            f"marca='{self.marca}', "
            f"modelo='{self.modelo}', "
            f"ano={self.ano}, "
            f"cor='{self.cor}', "
            f"km={self.km}, "
            f"motor='{self.motor}', "
            f"combustivel='{self.combustivel}')"
        )