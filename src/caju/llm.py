"""Conversa com o modelo local via Ollama.

Sprint 0 · CAJU-03: chat()       — texto entra, texto sai.
Sprint 1 · CAJU-08: OllamaLLM   — o adaptador que o loop do agente usa.

Documentação: https://docs.ollama.com/capabilities/tool-calling
Biblioteca:   pip install ollama   (o Ollama precisa estar rodando: `ollama serve`)
"""

from caju.config import MODELO


def chat(mensagens: list[dict], modelo: str = MODELO, temperatura: float = 0.7) -> str:
    """CAJU-03: manda a lista de mensagens ao Ollama e devolve só o texto da resposta.

    Pistas:
    - import ollama dentro da função (assim os testes rodam sem o Ollama instalado).
    - A temperatura vai em options={"temperature": ...}.
    - O qwen3 pode "pensar" antes de responder. Descubra na documentação onde esse
      raciocínio aparece na resposta e o que o parâmetro `think` faz. Anote no diário.
    """
    raise NotImplementedError("CAJU-03")


class OllamaLLM:
    """CAJU-08: adaptador entre o Ollama e o loop do agente.

    Uso:  llm = OllamaLLM();  msg = llm(mensagens, schemas)

    Deve devolver um dict no formato que agent.py espera:
        {"role": "assistant", "content": "...", "tool_calls": [{"function": {"name": ..., "arguments": {...}}}]}
    (sem a chave "tool_calls", ou com lista vazia, quando o modelo não pedir ferramenta).

    Pistas:
    - ollama.chat(model=..., messages=..., tools=schemas, options=...)
    - A resposta é um objeto, não um dict. Converta só os campos de que o loop precisa.
    - Use temperatura baixa (0 a 0.2) aqui. Por quê? Responda no diário.
    """

    def __init__(self, modelo: str = MODELO, temperatura: float = 0.0):
        self.modelo = modelo
        self.temperatura = temperatura

    def __call__(self, mensagens: list[dict], schemas: list[dict]) -> dict:
        raise NotImplementedError("CAJU-08")
