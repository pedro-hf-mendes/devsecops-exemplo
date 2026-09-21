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
        "id INTEGER PRIMARY KEY, nome TEXT, senha_hash TEXT)"
    )
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        for nome, senha in USUARIOS_INICIAIS:
            cursor.execute(
                "INSERT INTO users (nome, senha_hash) VALUES (?, ?)",
                (nome, accounts.hash_de_senha(senha)),
            )
    conexao.commit()


def _normalizar(valor: str) -> str:
    return valor.strip()


def _montar_filtro(campo: str, valor: str) -> str:
    return campo + " = '" + valor + "'"


def buscar_por_nome(nome: str) -> list[tuple]:
    filtro = _montar_filtro("nome", _normalizar(nome))

    conexao = _conectar()
    cursor = conexao.cursor()
    partes = ["SELECT id, nome FROM users WHERE", filtro]
    cursor.execute(" ".join(partes))  # <-- sink: SQL injection
    return cursor.fetchall()


def credenciais(nome: str) -> tuple | None:
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT senha_hash FROM users WHERE nome = '" + nome + "'")
    return cursor.fetchone()


def listar(limite: int = 50) -> list[tuple]:
    conexao = _conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM users LIMIT " + str(limite))
    return cursor.fetchall()
