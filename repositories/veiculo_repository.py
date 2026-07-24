from database.conexao import criar_conexao
from models.veiculo import Veiculo


class VeiculoRepository:

    def _mapear_veiculo(self, linha) -> Veiculo:

        return Veiculo(
            id_veiculo=linha["id_veiculo"],
            cliente_id=linha["cliente_id"],
            cliente=linha["cliente"],
            placa=linha["placa"],
            marca=linha["marca"],
            modelo=linha["modelo"],
            ano=linha["ano"],
            cor=linha["cor"],
            km=linha["km"],
            motor=linha["motor"],
            combustivel=linha["combustivel"]
        )


    def inserir(self, veiculo: Veiculo) -> int:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO veiculos (
                    cliente_id,
                    placa,
                    marca,
                    modelo,
                    ano,
                    cor,
                    km,
                    motor,
                    combustivel
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                veiculo.cliente_id,
                veiculo.placa,
                veiculo.marca,
                veiculo.modelo,
                veiculo.ano,
                veiculo.cor,
                veiculo.km,
                veiculo.motor,
                veiculo.combustivel
            ))

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()


    def listar(self) -> list[Veiculo]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
            SELECT
                v.id_veiculo,
                v.cliente_id,
                c.nome AS cliente,
                v.placa,
                v.marca,
                v.modelo,
                v.ano,
                v.cor,
                v.km,
                v.motor,
                v.combustivel
            FROM veiculos v
            INNER JOIN clientes c
                ON c.id_cliente = v.cliente_id
            ORDER BY v.id_veiculo DESC
            """)

            linhas = cursor.fetchall()

            return [
                self._mapear_veiculo(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def pesquisar(self, texto: str) -> list[Veiculo]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                v.id_veiculo,
                v.cliente_id,
                c.nome AS cliente,
                v.placa,
                v.marca,
                v.modelo,
                v.ano,
                v.cor,
                v.km,
                v.motor,
                v.combustivel
            FROM veiculos v
            INNER JOIN clientes c
                ON c.id_cliente = v.cliente_id
            WHERE v.placa LIKE ?
            ORDER BY v.id_veiculo
            """, (f"{texto}%",))

            linhas = cursor.fetchall()

            return [
                self._mapear_veiculo(linha)
                for linha in linhas
            ]

        finally:
            conexao.close()


    def buscar_por_id(self, id_veiculo: int) -> Veiculo | None:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    v.id_veiculo,
                    v.cliente_id,
                    c.nome AS cliente,
                    v.placa,
                    v.marca,
                    v.modelo,
                    v.ano,
                    v.cor,
                    v.km,
                    v.motor,
                    v.combustivel
                FROM veiculos v
                INNER JOIN clientes c
                    ON c.id_cliente = v.cliente_id
                WHERE v.id_veiculo = ?
            """, (id_veiculo,))

            linha = cursor.fetchone()

            if linha is None:
                return None

            return self._mapear_veiculo(linha)

        finally:
            conexao.close()


    def atualizar(self, veiculo: Veiculo):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE veiculos
                   SET cliente_id = ?,
                       placa = ?,
                       marca = ?,
                       modelo = ?,
                       ano = ?,
                       cor = ?,
                       km = ?,
                       motor = ?,
                       combustivel = ?
                 WHERE id_veiculo = ?
            """, (
                veiculo.cliente_id,
                veiculo.placa,
                veiculo.marca,
                veiculo.modelo,
                veiculo.ano,
                veiculo.cor,
                veiculo.km,
                veiculo.motor,
                veiculo.combustivel,
                veiculo.id_veiculo
            ))

            conexao.commit()

        finally:
            conexao.close()


    def excluir(self, id_veiculo: int):

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM veiculos
                WHERE id_veiculo = ?
            """, (id_veiculo,))

            conexao.commit()

        finally:
            conexao.close()