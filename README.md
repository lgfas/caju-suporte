# Caju Suporte

Agente de IA de atendimento da Loja Caju, uma loja online (fictícia) de cafés especiais.
Projeto de aprendizado de engenharia de IA: agentes, tool calling, MCP, RAG, evals e produção.

O plano completo, a arquitetura e o glossário estão no doc de kickoff do projeto.

## Começando

```bash
# 1. Modelo local (grátis)
ollama pull qwen3:8b          # máquina mais fraca: qwen3:4b  e  export CAJU_MODELO=qwen3:4b

# 2. Dependências
uv sync                       # sem uv: python -m venv .venv && source .venv/bin/activate
                              #         pip install ollama "mcp>=2.3,<3" pytest

# 3. Testes de aceite (no começo, todos falham: é o seu trabalho fazê-los passar)
uv run pytest -v
uv run pytest tests/test_s0_contexto.py -v     # só a sprint 0
```

## Como o trabalho funciona

1. Abra o ticket da sprint em `sprints/`.
2. Procure os `raise NotImplementedError("CAJU-XX")` com o número do ticket e implemente.
3. Rode os testes até passarem. **Não edite os testes**: eles são o critério de aceite.
4. Responda as perguntas de estudo em `notes/diario.md`.
5. Entregue: zip ou link do GitHub, a saída do `pytest` e o diário.

## Estrutura

```
data/pedidos.json        clientes e pedidos falsos
docs/politicas/          políticas da loja (base do RAG na sprint 4)
sprints/                 os tickets, uma sprint por arquivo
notes/diario.md          suas respostas e descobertas
src/caju/
  config.py              modelo, caminhos e system prompt (via variáveis de ambiente)
  contexto.py            S0: janela de contexto
  llm.py                 S0/S1: conversa com o Ollama
  tools.py               S1: as ferramentas e seus schemas
  agent.py               S1: o loop do agente
scripts/
  chat.py                S0: chat no terminal
  agente.py              S1: o agente com ferramentas
tests/                   testes de aceite (o LLM dos testes é falso: tests/fakes.py)
```

## Variáveis de ambiente

| Variável | Padrão | Para quê |
|---|---|---|
| `CAJU_MODELO` | `qwen3:8b` | modelo do Ollama |
| `CAJU_PEDIDOS` | `data/pedidos.json` | base de pedidos |
| `CAJU_CHAMADOS` | `data/chamados.json` | onde os chamados são gravados (fora do git) |
