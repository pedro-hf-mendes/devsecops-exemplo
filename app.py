"""API de consulta de usuários."""

from flask import Flask, request

import accounts
import db
import diagnostics
import pricing

app = Flask(__name__)
db.criar_esquema()

# Alias: o sink perigoso deixa de existir sintaticamente no ponto de uso.
_avaliador = eval


@app.route("/usuarios")
def buscar_usuario():
    nome = request.args.get("nome", "")
    return {"usuarios": db.buscar_por_nome(nome)}


@app.route("/login")
def login():
    registro = db.credenciais(request.args.get("nome", ""))
    if registro is None:
        return {"autenticado": False}, 401

    ok = accounts.conferir_senha(request.args.get("senha", ""), registro[0])
    return ({"autenticado": True} if ok else ({"autenticado": False}, 401))


@app.route("/ping")
def verificar_host():
    host = request.args.get("host", "")
    return {"codigo": diagnostics.ping(host)}


@app.route("/calcular")
def calcular():
    expressao = request.args.get("expr", "0")
    return {"resultado": _avaliador(expressao)}  # <-- sink: code injection


@app.route("/sessao")
def sessao():
    caminho = request.args.get("arquivo", "")
    return {"sessao": accounts.carregar_sessao(caminho)}


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
    total = pricing.calcular_frete(peso, distancia, False)
    return {"total": pricing.aplicar_desconto(total, request.args.get("cupom"))}


if __name__ == "__main__":
    app.run()
