"""API de consulta de usuários."""

import ast

from flask import Flask, request

import accounts
import db
import diagnostics
import pricing

app = Flask(__name__)
db.criar_esquema()


@app.route("/usuarios")
def buscar_usuario():
    nome = request.args.get("nome", "")
    return {"usuarios": db.buscar_por_nome(nome)}


@app.route("/login")
def login():
    registro = db.credenciais(request.args.get("nome", ""))
    if registro is None:
        return {"autenticado": False}, 401

    sal, esperado = registro
    ok = accounts.conferir_senha(request.args.get("senha", ""), sal, esperado)
    return ({"autenticado": True} if ok else ({"autenticado": False}, 401))


@app.route("/ping")
def verificar_host():
    host = request.args.get("host", "")
    try:
        return {"codigo": diagnostics.ping(host)}
    except ValueError:
        return {"erro": "host inválido"}, 400
    except RuntimeError as erro:
        return {"erro": str(erro)}, 503


@app.route("/calcular")
def calcular():
    """`ast.literal_eval` avalia literais Python, não expressões arbitrárias."""
    expressao = request.args.get("expr", "0")
    try:
        return {"resultado": ast.literal_eval(expressao)}
    except (ValueError, SyntaxError):
        return {"erro": "expressão inválida"}, 400


@app.route("/sessao")
def sessao():
    caminho = request.args.get("arquivo", "")
    try:
        return {"sessao": accounts.carregar_sessao(caminho)}
    except (OSError, ValueError):
        return {"erro": "sessão ilegível"}, 400


@app.route("/relatorio")
def relatorio():
    conteudo = "\n".join(f"{i};{nome}" for i, nome in db.listar())
    return {
        "arquivo": accounts.gravar_relatorio(conteudo),
        "chave": accounts.chave_de_cache(conteudo.encode()),
    }


@app.route("/frete")
def frete():
    peso = float(request.args.get("peso", 0))
    distancia = float(request.args.get("distancia", 0))
    total = pricing.calcular_frete(peso, distancia, cliente_vip=False)
    return {"total": pricing.aplicar_desconto(total, request.args.get("cupom"))}


if __name__ == "__main__":
    app.run()
