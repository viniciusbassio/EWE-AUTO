from database.conexao import criar_conexao
from models.configuracao import Configuracao


class ConfiguracaoRepository:

    def buscar(self) -> Configuracao | None:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT *
                FROM configuracoes
                WHERE id_configuracao = 1
            """)

            linha = cursor.fetchone()

            if linha is None:
                return None

            return Configuracao(
                id_configuracao=linha["id_configuracao"],
                nome_oficina=linha["nome_oficina"],
                cnpj=linha["cnpj"] or "",
                telefone=linha["telefone"] or "",
                endereco=linha["endereco"] or "",
                cidade=linha["cidade"] or "",
                estado=linha["estado"] or "",
                email=linha["email"] or "",
                logo=linha["logo"] or ""
            )

        finally:
            conexao.close()


    def salvar(self, configuracao: Configuracao):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO configuracoes (
                    id_configuracao,
                    nome_oficina,
                    cnpj,
                    telefone,
                    endereco,
                    cidade,
                    estado,
                    email,
                    logo
                )
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)

                ON CONFLICT(id_configuracao)
                DO UPDATE SET
                    nome_oficina = excluded.nome_oficina,
                    cnpj = excluded.cnpj,
                    telefone = excluded.telefone,
                    endereco = excluded.endereco,
                    cidade = excluded.cidade,
                    estado = excluded.estado,
                    email = excluded.email,
                    logo = excluded.logo
            """, (
                configuracao.nome_oficina,
                configuracao.cnpj,
                configuracao.telefone,
                configuracao.endereco,
                configuracao.cidade,
                configuracao.estado,
                configuracao.email,
                configuracao.logo
            ))

            conexao.commit()

        finally:
            conexao.close()