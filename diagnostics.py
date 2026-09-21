"""Verificações de conectividade usadas pela rota de diagnóstico."""

import re
import shutil
import subprocess

import requests

HOST_VALIDO = re.compile(r"^[a-zA-Z0-9.-]{1,253}$")


def ping(host: str) -> int:
    """Allowlist na entrada e argumentos em lista, sem shell.

    Sem `shell=True`, o sistema operacional recebe uma lista de argumentos já
    separada. Um host como `x; rm -rf /` seria tratado como um nome de host
    esquisito, não como dois comandos — e a allowlist o recusa antes disso.
    """
    if not HOST_VALIDO.match(host):
        raise ValueError("host inválido")

    binario = shutil.which("ping")
    if binario is None:
        raise RuntimeError("ping indisponível")

    resultado = subprocess.run(
        [binario, "-c", "1", "--", host],
        shell=False,
        check=False,
        capture_output=True,
        timeout=5,
    )
    return resultado.returncode


def status_do_parceiro(url: str) -> int:
    """Certificado TLS validado."""
    return requests.get(url, verify=True, timeout=10).status_code
