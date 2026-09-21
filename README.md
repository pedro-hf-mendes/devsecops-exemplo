# security-ci-cd-example

API Flask mínima usada como laboratório para instalar e comparar três
ferramentas de análise estática de segurança:

| Ferramenta | Onde roda | Quando |
| --- | --- | --- |
| SonarLint (SonarQube for IDE) | VS Code | enquanto você escreve |
| Bandit | pre-commit hook | no `git commit` |
| CodeQL | GitHub Actions | no push e no pull request |

## Branches

| Branch | Conteúdo |
| --- | --- |
| `main` | a aplicação escrita corretamente |
| `insecure_development` | os mesmos módulos, degradados |

Os dois lados têm os mesmos arquivos e as mesmas funções. Só a implementação
muda:

```bash
git diff main insecure_development
```

| Arquivo | Papel |
| --- | --- |
| `app.py` | rotas Flask |
| `db.py` | acesso ao banco |
| `diagnostics.py` | ping e checagem de parceiro |
| `accounts.py` | senha, sessão e relatórios |
| `pricing.py` | regra de negócio |

---

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python app.py
```

Na primeira execução o `users.db` é criado e populado. A API sobe em
`http://127.0.0.1:5000`:

| Rota | Exemplo |
| --- | --- |
| `/usuarios` | `/usuarios?nome=ana` |
| `/login` | `/login?nome=ana&senha=senha-da-ana` |
| `/ping` | `/ping?host=exemplo.com` |
| `/calcular` | `/calcular?expr=42` |
| `/sessao` | `/sessao?arquivo=sessao.json` |
| `/relatorio` | `/relatorio` |
| `/frete` | `/frete?peso=3&distancia=150&cupom=BLACK` |

Usuários iniciais: `ana`, `bruno` e `carla`, com as senhas `senha-da-ana`,
`senha-do-bruno` e `tr0ub4dor`.

---

## Etapa 1 — SonarLint no VS Code

1. Na aba de extensões (`Ctrl+Shift+X`), instale **SonarLint** (publicado como
   *SonarQube for IDE*, id `SonarSource.sonarlint-vscode`).
2. Instale também a extensão **Python** (`ms-python.python`).
3. A extensão precisa de um **JRE 17+**; se não encontrar Java, ela pede
   permissão para baixar o próprio — aceite.
4. `Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`.

Não há nada a configurar no repositório. Abra um arquivo e os avisos aparecem
sublinhados; a lista completa fica no painel **Problems** (`Ctrl+Shift+M`).
Para ver a explicação de uma regra, use **SonarQube for IDE: Show Rule
Description**.

**Connected Mode** (opcional): `Ctrl+Shift+P` → **Connect to SonarQube Cloud /
Server**, gere um token, guarde nas *User Settings* e faça o binding do
projeto. É o que habilita as regras de injeção, que exigem SonarQube Cloud ou
Server Developer Edition.

---

## Etapa 2 — Bandit como pre-commit hook

```bash
pip install bandit
bandit -r . -ll -ii        # severidade e confiança médias ou acima
```

Um hook do Git é um executável com o nome certo dentro de `.git/hooks/`:

```bash
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
arquivos=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
[ -z "$arquivos" ] && exit 0

bandit -q -ll -ii $arquivos
HOOK

chmod +x .git/hooks/pre-commit
```

O Bandit devolve código de saída diferente de zero quando encontra algo, e o
Git aborta o commit quando o hook falha.

Para testar, traga um arquivo vulnerável para a `main` manualmente

Para desligar: `rm .git/hooks/pre-commit`. O diretório `.git/` não é
versionado, então cada clone precisa criar o seu.

---

## Etapa 3 — CodeQL no GitHub Actions

Visível num pull-request da branch insecure_development para a main
