class Configuracao:

    def __init__(
        self,
        nome_oficina: str,
        cnpj: str = "",
        telefone: str = "",
        endereco: str = "",
        cidade: str = "",
        estado: str = "",
        email: str = "",
        logo: str = "",
        id_configuracao: int = 1
    ):
        self.id_configuracao = id_configuracao
        self.nome_oficina = nome_oficina
        self.cnpj = cnpj
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.email = email
        self.logo = logo