"""Credenciais, sessões e relatórios de conta."""

import hashlib
import hmac
import json
import os
import secrets
import tempfile

ITERACOES = 600_000


def hash_de_senha(senha: str, sal: str | None = None) -> tuple[str, str]:
    """PBKDF2: lento e com sal, que é o que uma senha precisa.

    Lentidão aqui é recurso, não defeito: encarece o ataque de força bruta.
    O sal impede que senhas iguais gerem hashes iguais.
    """
    sal = sal or secrets.token_hex(16)
    derivado = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(sal), ITERACOES)
    return sal, derivado.hex()


def conferir_senha(senha: str, sal: str, esperado: str) -> bool:
    """Comparação em tempo constante, para não vazar o hash por temporização."""
    _, calculado = hash_de_senha(senha, sal)
    return hmac.compare_digest(calculado, esperado)


def chave_de_cache(dados: bytes) -> str:
    """MD5 como identificador de cache — uso não criptográfico.

    `usedforsecurity=False` declara essa intenção. A ferramenta de análise não
    tem como adivinhar se um MD5 é hash de senha ou chave de cache; aqui a
    dúvida é respondida no próprio código.
    """
    return hashlib.md5(dados, usedforsecurity=False).hexdigest()


def carregar_sessao(caminho: str) -> dict:
    """JSON não instancia objetos: desserializar não executa código."""
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def gravar_relatorio(conteudo: str) -> str:
    """Arquivo temporário com nome imprevisível e permissão restrita."""
    descritor, caminho = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(descritor, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    return caminho
