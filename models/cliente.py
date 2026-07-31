from typing import Optional

class Cliente:
    def __init__(
        self,
        nome: str,
        telefone: str,
        cpf: str,
        endereco: str,
        observacoes: str = "",
        id_cliente: Optional[int] = None
    ):
        self.id_cliente = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.endereco = endereco
        self.observacoes = observacoes

    def __repr__(self):
        return (
            f"Cliente("
            f"id={self.id_cliente}, "
            f"nome='{self.nome}', "
            f"telefone='{self.telefone}', "
            f"cpf='{self.cpf}', "
            f"endereco='{self.endereco}', "
            f"observacoes='{self.observacoes}')"
        )