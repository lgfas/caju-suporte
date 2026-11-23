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
    mensagem_system = {'role': 'system', 'content': SYSTEM_PROMPT}
    print("Caju Suporte (modo chat). /sair para encerrar.\n")

    while True:
        pergunta = input("você> ").strip()
        if not pergunta:
            continue
        if pergunta == "/sair":
            break

        # TODO CAJU-03:
        # 1. Trate /tokens, /temp <valor> e /limpar.
        if pergunta == "/tokens":
            print(tokens_da_conversa([mensagem_system] + historico))
            continue

        if pergunta.startswith("/temp"):
            partes = pergunta.split()
            try:
                temperatura = float(partes[1])
                print(f"temperatura = {temperatura}")
            except (IndexError, ValueError):
                print("uso: /temp 0.2")
            continue

        if pergunta == "/limpar":
            historico = []
            print("histórico apagado")
            continue
        # 2. Monte as mensagens com montar_mensagens e corte com cortar_historico(…, MAX_TOKENS).
        mensagens = montar_mensagens(system_prompt=SYSTEM_PROMPT, historico=historico, pergunta=pergunta)
        mensagens = cortar_historico(mensagens=mensagens, max_tokens=MAX_TOKENS)
        # 3. Chame chat(...), imprima a resposta como "caju> ...".
        resposta = chat(mensagens=mensagens, temperatura=temperatura)

        print("caju> " + resposta)
        # 4. Guarde a pergunta e a resposta no historico para o próximo turno.
        historico.append({"role": "user", "content": pergunta})
        historico.append({"role": "assistant", "content": resposta})


if __name__ == "__main__":
    main()
