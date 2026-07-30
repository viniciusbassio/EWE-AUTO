import sys
from pathlib import Path
from database.conexao import criar_conexao, BANCO_DADOS


def caminho_recurso(relativo):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent.parent

    return base / relativo


def inicializar_banco():
    if BANCO_DADOS.exists():
        return

    caminho_schema = caminho_recurso("database/schema.sql")

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