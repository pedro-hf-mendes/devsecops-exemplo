"""Acesso ao banco de usuários."""

import sqlite3

import accounts

BANCO = "users.db"

USUARIOS_INICIAIS = [
    ("ana", "senha-da-ana"),
    ("bruno", "senha-do-bruno"),
    ("carla", "tr0ub4dor"),
]


def _conectar() -> sqlite3.Connection:
    return sqlite3.connect(BANCO)


def criar_esquema() -> None:
    """Cria e popula o banco na primeira execução."""
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, nome TEXT, sal TEXT, senha_hash TEXT)"
    )
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        for nome, senha in USUARIOS_INICIAIS:
            sal, senha_hash = accounts.hash_de_senha(senha)
            cursor.execute(
                "INSERT INTO users (nome, sal, senha_hash) VALUES (?, ?, ?)",
                (nome, sal, senha_hash),
            )
    conexao.commit()


def buscar_por_nome(nome: str) -> list[tuple]:
    """Consulta parametrizada: o valor viaja como dado, nunca como sintaxe.

    O `?` faz o driver enviar a query e o valor separadamente. Não existe
    escape a ser furado, porque o valor nunca chega a ser interpretado como SQL.
    """
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM users WHERE nome = ?", (nome,))
    return cursor.fetchall()


def credenciais(nome: str) -> tuple | None:
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT sal, senha_hash FROM users WHERE nome = ?", (nome,))
    return cursor.fetchone()


def listar(limite: int = 50) -> list[tuple]:
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM users LIMIT ?", (limite,))
    return cursor.fetchall()
