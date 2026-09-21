"""Regras de preço e frete.

Nada aqui toca em segurança. É o módulo de regra de negócio comum, e serve
como controle: o que uma ferramenta diz sobre este arquivo é qualidade de
código, não vulnerabilidade.
"""

TAXA_PADRAO = 12.0
INDISPONIVEL = "sistema indisponível"


def calcular_frete(peso: float, distancia: float, cliente_vip: bool) -> float:
    subtotal = peso * 2.0
    taxa = 0.0 if cliente_vip else TAXA_PADRAO
    adicional = 8.0 if distancia > 100 else 0.0
    return subtotal + taxa + adicional


def aplicar_desconto(total: float, cupom: str | None) -> float:
    if not cupom:
        return total
    percentuais = {"BEMVINDO": 0.10, "FRETEGRATIS": 0.0, "BLACK": 0.25}
    return total * (1 - percentuais.get(cupom.upper(), 0.0))


def carregar_tabela(caminho: str) -> str | None:
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return arquivo.read()
    except OSError as erro:
        print(f"{INDISPONIVEL}: {erro}")
        return None
