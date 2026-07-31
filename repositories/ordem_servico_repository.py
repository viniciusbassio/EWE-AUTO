from database.conexao import criar_conexao
from models.ordem_servico import OrdemServico
from typing import List, Optional

class OrdemServicoRepository:

    def _mapear_ordem(self, linha) -> OrdemServico:

        ordem = OrdemServico(
            id_os=linha["id_os"],
            numero_os=linha["numero_os"],
            cliente_id=linha["cliente_id"],
            veiculo_id=linha["veiculo_id"],
            data_abertura=linha["data_abertura"],
            data_fechamento=linha["data_fechamento"],
            problema_relatado=linha["problema_relatado"],
            diagnostico=linha["diagnostico"],
            valor_mao_obra=linha["valor_mao_obra"],
            valor_pecas=linha["valor_pecas"],
            valor_total=linha["valor_total"],
            forma_pagamento=linha["forma_pagamento"],
            status=linha["status"],
            observacoes=linha["observacoes"]
        )

        if "nome_cliente" in linha.keys():
            ordem.cliente = linha["nome_cliente"] or ""

        if "placa" in linha.keys():
            marca = linha["marca"] or ""
            modelo = linha["modelo"] or ""
            placa = linha["placa"] or ""

            ordem.veiculo = (
                f"{marca} {modelo} - {placa}"
            ).strip()

        return ordem


    def inserir(self, ordem: OrdemServico) -> int:

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO ordens_servico(
                    numero_os,
                    cliente_id,
                    veiculo_id,
                    data_abertura,
                    data_fechamento,
                    problema_relatado,
                    diagnostico,
                    valor_mao_obra,
                    valor_pecas,
                    valor_total,
                    forma_pagamento,
                    status,
                    observacoes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ordem.numero_os,
                ordem.cliente_id,
                ordem.veiculo_id,
                ordem.data_abertura,
                ordem.data_fechamento,
                ordem.problema_relatado,
                ordem.diagnostico,
                ordem.valor_mao_obra,
                ordem.valor_pecas,
                ordem.valor_total,
                ordem.forma_pagamento,
                ordem.status,
                ordem.observacoes
            ))

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()


    def listar(self) -> List[OrdemServico]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    os.*,
                    c.nome AS nome_cliente,
                    v.marca,
                    v.modelo,
                    v.placa
                FROM ordens_servico os
                INNER JOIN clientes c
                    ON c.id_cliente = os.cliente_id
                INNER JOIN veiculos v
                    ON v.id_veiculo = os.veiculo_id
                ORDER BY os.id_os DESC
            """)

            return [
                self._mapear_ordem(linha)
                for linha in cursor.fetchall()
            ]

        finally:
            conexao.close()


    def buscar_por_id(self, id_os: int) -> Optional[OrdemServico]:

        conexao = criar_conexao()

        try:
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT
                    os.*,
                    c.nome AS nome_cliente,
                    v.marca,
                    v.modelo,
                    v.placa
                FROM ordens_servico os
                INNER JOIN clientes c
                    ON c.id_cliente = os.cliente_id
                INNER JOIN veiculos v
                    ON v.id_veiculo = os.veiculo_id
                WHERE os.id_os = ?
            """, (id_os,))

            linha = cursor.fetchone()

            if linha is None:
                return None

            return self._mapear_ordem(linha)

        finally:
            conexao.close()


    def atualizar(self, ordem: OrdemServico):

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE ordens_servico
                   SET numero_os=?,
                       cliente_id=?,
                       veiculo_id=?,
                       data_abertura=?,
                       data_fechamento=?,
                       problema_relatado=?,
                       diagnostico=?,
                       valor_mao_obra=?,
                       valor_pecas=?,
                       valor_total=?,
                       forma_pagamento=?,
                       status=?,
                       observacoes=?
                 WHERE id_os=?
            """, (

                ordem.numero_os,
                ordem.cliente_id,
                ordem.veiculo_id,
                ordem.data_abertura,
                ordem.data_fechamento,
                ordem.problema_relatado,
                ordem.diagnostico,
                ordem.valor_mao_obra,
                ordem.valor_pecas,
                ordem.valor_total,
                ordem.forma_pagamento,
                ordem.status,
                ordem.observacoes,
                ordem.id_os

            ))

            conexao.commit()

        finally:
            conexao.close()


    def excluir(self, id_os: int):

        conexao = criar_conexao()

        try:

            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM ordens_servico
                WHERE id_os = ?
            """, (id_os,))

            conexao.commit()

        finally:
            conexao.close()

    def pesquisar_ordens(self, texto: str) -> List[OrdemServico]:

        conexao = criar_conexao()
    
        try:
            cursor = conexao.cursor()
    
            termo = f"%{texto.strip()}%"
    
            cursor.execute("""
                SELECT
                    os.*,
                    c.nome AS nome_cliente,
                    v.marca,
                    v.modelo,
                    v.placa
                FROM ordens_servico os
                INNER JOIN clientes c
                    ON c.id_cliente = os.cliente_id
                INNER JOIN veiculos v
                    ON v.id_veiculo = os.veiculo_id
                WHERE CAST(os.numero_os AS TEXT) LIKE ?
                   OR c.nome LIKE ?
                   OR v.placa LIKE ?
                   OR v.marca LIKE ?
                   OR v.modelo LIKE ?
                   OR os.status LIKE ?
                ORDER BY os.id_os DESC
            """, (
                termo,
                termo,
                termo,
                termo,
                termo,
                termo
            ))
    
            return [
                self._mapear_ordem(linha)
                for linha in cursor.fetchall()
            ]
    
        finally:
            conexao.close()