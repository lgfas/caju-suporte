"""Sprint 0 · CAJU-03: chat no terminal com o modelo local.

Rode com:  uv run python scripts/chat.py      (ou: python scripts/chat.py com o venv ativo)

Comandos:
  /tokens        mostra a estimativa de tokens da conversa
  /temp 0.2      muda a temperatura
  /limpar        apaga o histórico (o system prompt fica)
  /sair          encerra
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from caju.config import SYSTEM_PROMPT  # noqa: E402
from caju.contexto import cortar_historico, montar_mensagens, tokens_da_conversa  # noqa: E402,F401
from caju.llm import chat  # noqa: E402,F401

MAX_TOKENS = 2000  # pequeno de propósito, para você ver o corte acontecer


def main() -> None:
    historico: list[dict] = []
    temperatura = 0.7
    print("Caju Suporte (modo chat). /sair para encerrar.\n")

    while True:
        pergunta = input("você> ").strip()
        if not pergunta:
            continue
        if pergunta == "/sair":
            break

        # TODO CAJU-03:
        # 1. Trate /tokens, /temp <valor> e /limpar.
        # 2. Monte as mensagens com montar_mensagens e corte com cortar_historico(…, MAX_TOKENS).
        # 3. Chame chat(...), imprima a resposta como "caju> ...".
        # 4. Guarde a pergunta e a resposta no historico para o próximo turno.
        raise NotImplementedError("CAJU-03")


if __name__ == "__main__":
    main()
