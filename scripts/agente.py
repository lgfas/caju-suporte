"""Sprint 1 · CAJU-08: o agente de verdade, com Ollama e ferramentas.

Rode com:  uv run python scripts/agente.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from caju.agent import rodar_agente  # noqa: E402,F401
from caju.llm import OllamaLLM  # noqa: E402,F401
from caju.tools import FERRAMENTAS, SCHEMAS  # noqa: E402,F401


def main() -> None:
    print("Caju Suporte (modo agente). /sair para encerrar.\n")
    historico: list[dict] = []

    while True:
        pergunta = input("cliente> ").strip()
        if not pergunta:
            continue
        if pergunta == "/sair":
            break

        # TODO CAJU-08:
        # 1. Rode rodar_agente(pergunta, OllamaLLM(), FERRAMENTAS, SCHEMAS, historico=historico).
        # 2. Antes da resposta, imprima cada chamada de ferramenta, por exemplo:
        #       [ferramenta] buscar_pedido({'pedido_id': 'CJ-1002'}) -> {...}
        #    e quantos passos o agente levou. Isso é o seu primeiro "trace".
        # 3. Atualize o historico com a conversa do resultado, SEM o system prompt.
        raise NotImplementedError("CAJU-08")


if __name__ == "__main__":
    main()
