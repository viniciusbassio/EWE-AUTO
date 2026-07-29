from database.conexao import criar_conexao
from models.item_peca import ItemPeca


class ItemPecaRepository:

    def _mapear_item(self, linha):

        return ItemPeca(
            id_item_peca=linha["id_item_peca"],
            os_id=linha["os_id"],
            peca_id=linha["peca_id"],
            quantidade=linha["quantidade"],
            valor_unitario=linha["valor_unitario"],
            valor_total=linha["valor_total"]
        )


    def inserir(self, item: ItemPeca):

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO itens_peca(
                    os_id,
                    peca_id,
                    quantidade,
                    valor_unitario,
                    valor_total
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                item.os_id,
                item.peca_id,
                item.quantidade,
                item.valor_unitario,
                item.valor_total
            ))

            conexao.commit()

        finally:
            conexao.close()


    def listar_por_os(self, os_id: int):

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                SELECT *
                FROM itens_peca
                WHERE os_id=?
            """, (os_id,))

            return [
                self._mapear_item(linha)
                for linha in cursor.fetchall()
            ]

        finally:
            conexao.close()


    def excluir_por_os(self, os_id: int):

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                DELETE
                FROM itens_peca
                WHERE os_id=?
            """, (os_id,))

            conexao.commit()

        finally:
            conexao.close()