"""Credenciais, sessões e relatórios de conta."""

import hashlib
import pickle


def hash_de_senha(senha: str) -> str:
    return hashlib.md5(senha.encode()).hexdigest()


def conferir_senha(senha: str, esperado: str) -> bool:
    return hash_de_senha(senha) == esperado


def chave_de_cache(dados: bytes) -> str:
    return hashlib.md5(dados).hexdigest()


def carregar_sessao(caminho: str) -> dict:
    with open(caminho, "rb") as arquivo:
        return pickle.loads(arquivo.read())  # <-- sink: desserialização insegura


def gravar_relatorio(conteudo: str) -> str:
    caminho = "/tmp/relatorio.txt"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    return caminho
