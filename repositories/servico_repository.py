from database.conexao import criar_conexao
from models.servico import Servico


class ServicoRepository:

    def _mapear_servico(self, linha) -> Servico:
        return Servico(
            id_servico=linha["id_servico"],
            descricao=linha["descricao"],
            valor_padrao=linha["valor_padrao"],
            observacoes=linha["observacoes"]
        )


    def inserir(self, servico: Servico) -> int:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO servicos (
                    descricao,
                    valor_padrao,
                    observacoes
                )
                VALUES (?, ?, ?)
            """, (
                servico.descricao,
                servico.valor_padrao,
                servico.observacoes
            ))

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()


    def listar(self) -> list[Servico]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_servico,
                    descricao,
                    valor_padrao,
                    observacoes
                FROM servicos
                ORDER BY id_servico DESC
            """)

            linhas = cursor.fetchall()

            return [
                self._mapear_servico(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def pesquisar(self, texto: str) -> list[Servico]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_servico,
                    descricao,
                    valor_padrao,
                    observacoes
                FROM servicos
                WHERE descricao LIKE ?
                ORDER BY id_servico
            """, (f"%{texto}%",))

            linhas = cursor.fetchall()

            return [
                self._mapear_servico(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def buscar_por_id(self, id_servico: int) -> Servico | None:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    id_servico,
                    descricao,
                    valor_padrao,
                    observacoes
                FROM servicos
                WHERE id_servico = ?
            """, (id_servico,))

            linha = cursor.fetchone()

            if linha is None:
                return None

            return self._mapear_servico(linha)

        finally:
            conexao.close()


    def atualizar(self, servico: Servico):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE servicos
                   SET descricao = ?,
                       valor_padrao = ?,
                       observacoes = ?
                 WHERE id_servico = ?
            """, (
                servico.descricao,
                servico.valor_padrao,
                servico.observacoes,
                servico.id_servico
            ))

            conexao.commit()

        finally:
            conexao.close()


    def excluir(self, id_servico: int):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM servicos
                WHERE id_servico = ?
            """, (id_servico,))

            conexao.commit()

        finally:
            conexao.close()