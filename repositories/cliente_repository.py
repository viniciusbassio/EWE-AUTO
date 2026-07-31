from database.conexao import criar_conexao
from models.cliente import Cliente
from typing import List, Optional

class ClienteRepository:

    def _mapear_cliente(self, linha) -> Cliente:
        return Cliente(
            id_cliente=linha["id_cliente"],
            nome=linha["nome"],
            telefone=linha["telefone"],
            cpf=linha["cpf"],
            endereco=linha["endereco"],
            observacoes=linha["observacoes"]
        )


    def inserir(self, cliente: Cliente) -> int:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO clientes (
                    nome,
                    telefone,
                    cpf,
                    endereco,
                    observacoes
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                cliente.nome,
                cliente.telefone,
                cliente.cpf,
                cliente.endereco,
                cliente.observacoes
            ))

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()


    def listar(self) -> List[Cliente]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nome,
                    telefone,
                    cpf,
                    endereco,
                    observacoes
                FROM clientes
                ORDER BY id_cliente Desc
            """)

            linhas = cursor.fetchall()

            return [
                self._mapear_cliente(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def pesquisar(self, texto: str) -> List[Cliente]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nome,
                    telefone,
                    cpf,
                    endereco,
                    observacoes
                FROM clientes
                WHERE nome LIKE ?
                ORDER BY id_cliente
            """, (f"{texto}%",))

            linhas = cursor.fetchall()

            return [
                self._mapear_cliente(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_cliente,
                    nome,
                    telefone,
                    cpf,
                    endereco,
                    observacoes
                FROM clientes
                WHERE id_cliente = ?
            """, (id_cliente,))

            linha = cursor.fetchone()

            if linha is None:
                return None

            return self._mapear_cliente(linha)

        finally:
            conexao.close()


    def atualizar(self, cliente: Cliente):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE clientes
                   SET nome = ?,
                       telefone = ?,
                       cpf = ?,
                       endereco = ?,
                       observacoes = ?
                 WHERE id_cliente = ?
            """, (
                cliente.nome,
                cliente.telefone,
                cliente.cpf,
                cliente.endereco,
                cliente.observacoes,
                cliente.id_cliente
            ))

            conexao.commit()

        finally:
            conexao.close()


    def excluir(self, id_cliente: int):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM clientes
                WHERE id_cliente = ?
            """, (id_cliente,))

            conexao.commit()

        finally:
            conexao.close()