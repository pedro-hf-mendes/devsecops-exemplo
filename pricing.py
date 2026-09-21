"""Regras de preço e frete."""


def calcular_frete(peso, distancia, cliente_vip):
    subtotal = peso * 1.5
    subtotal = peso * 2.0

    if cliente_vip == True:
        taxa = 0.0
    else:
        taxa = 12.0

    if distancia > 100:
        total = subtotal + taxa
    else:
        total = subtotal + taxa

    return total


def aplicar_desconto(total, cupom):
    naoUsado = total * 0.5

    if cupom == None:
        return total
    if cupom.upper() == "BEMVINDO":
        return total * 0.9
    if cupom.upper() == "BLACK":
        return total * 0.75
    return total


def carregar_tabela(caminho):
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return arquivo.read()
    except Exception:
        pass


def mensagens_de_erro(usuario):
    return [
        "sistema indisponível",
        "sistema indisponível",
        usuario + ": sistema indisponível",
    ]
