from database.conexao import criar_conexao
from models.peca import Peca
from typing import List, Optional

class PecaRepository:

    def _mapear_peca(self, linha) -> Peca:
        return Peca(
            id_peca=linha["id_peca"],
            descricao=linha["descricao"],
            marca=linha["marca"],
            valor=linha["valor"]
        )


    def inserir(self, peca: Peca) -> int:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO pecas (
                    descricao,
                    marca,
                    valor
                )
                VALUES (?, ?, ?)
            """, (
                peca.descricao,
                peca.marca,
                peca.valor
            ))

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()


    def listar(self) -> List[Peca]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_peca,
                    descricao,
                    marca,
                    valor
                FROM pecas
                ORDER BY id_peca DESC
            """)

            linhas = cursor.fetchall()

            return [
                self._mapear_peca(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def pesquisar(self, texto: str) -> List[Peca]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_peca,
                    descricao,
                    marca,
                    valor
                FROM pecas
                WHERE descricao LIKE ?
                ORDER BY id_peca
            """, (f"{texto}%",))

            linhas = cursor.fetchall()

            return [
                self._mapear_peca(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def buscar_por_id(self, id_peca: int) -> Optional[Peca]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_peca,
                    descricao,
                    marca,
                    valor
                FROM pecas
                WHERE id_peca = ?
            """, (id_peca,))

            linha = cursor.fetchone()

            if linha is None:
                return None

            return self._mapear_peca(linha)

        finally:
            conexao.close()


    def atualizar(self, peca: Peca):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE pecas
                   SET descricao = ?,
                       marca = ?,
                       valor = ?
                 WHERE id_peca = ?
            """, (
                peca.descricao,
                peca.marca,
                peca.valor,
                peca.id_peca
            ))

            conexao.commit()

        finally:
            conexao.close()


    def excluir(self, id_peca: int):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM pecas
                WHERE id_peca = ?
            """, (id_peca,))

            conexao.commit()

        finally:
            conexao.close()