"""Verificações de conectividade usadas pela rota de diagnóstico."""

import os

import requests


def _normalizar(host: str) -> str:
    return host.strip()


def ping(host: str) -> int:
    alvo = _normalizar(host)
    return os.system("ping -c 1 " + alvo)  # <-- sink: command injection


def status_do_parceiro(url: str) -> int:
    return requests.get(url, verify=False, timeout=10).status_code
