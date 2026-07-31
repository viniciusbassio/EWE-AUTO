import sqlite3
from pathlib import Path

# Caminho do banco de dados
BASE_DIR = Path(__file__).resolve().parent
BANCO_DADOS = BASE_DIR / "ewe.db"


def criar_conexao():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """
    conexao = sqlite3.connect(BANCO_DADOS)

    # Ativa suporte a chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON;")

    # Retorna as linhas como objetos semelhantes a dicionários
    conexao.row_factory = sqlite3.Row

    return conexao