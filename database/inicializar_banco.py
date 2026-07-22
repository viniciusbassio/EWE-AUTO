from pathlib import Path
from database.conexao import criar_conexao, BANCO_DADOS


def inicializar_banco():
    if BANCO_DADOS.exists():
        return

    caminho_schema = Path(__file__).parent / "schema.sql"

    with open(caminho_schema, "r", encoding="utf-8") as arquivo:
        script_sql = arquivo.read()

    conexao = criar_conexao()

    try:
        conexao.executescript(script_sql)
        conexao.commit()
        print("Banco criado com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print(f"Erro ao criar banco: {erro}")

    finally:
        conexao.close()


if __name__ == "__main__":
    inicializar_banco()