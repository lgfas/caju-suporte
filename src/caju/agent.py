"""Sprint 1 · CAJU-07: o loop do agente.

Um agente é isto, e nada mais misterioso:

    mensagens = [system, *historico, pergunta]
    repita até max_passos:
        msg = llm(mensagens, schemas)          # o modelo responde OU pede ferramentas
        guarde msg em mensagens
        se msg não pediu ferramenta: fim, msg["content"] é a resposta
        para cada ferramenta pedida:
            execute, guarde o resultado como mensagem {"role": "tool", ...}
    estourou o limite: devolva MENSAGEM_ESCALONAMENTO

O `llm` é qualquer função  llm(mensagens, schemas) -> dict  que devolve uma mensagem de assistente:
    {"role": "assistant", "content": "texto"}                                   # resposta final
    {"role": "assistant", "content": "", "tool_calls": [                         # pedido de ferramenta
        {"function": {"name": "buscar_pedido", "arguments": {"pedido_id": "CJ-1002"}}}
    ]}
Nos testes ele é falso (tests/fakes.py). No uso real ele é o Ollama (llm.OllamaLLM).
"""

from dataclasses import dataclass, field

from caju.config import SYSTEM_PROMPT

MENSAGEM_ESCALONAMENTO = "Não consegui resolver por aqui. Vou passar sua conversa para um atendente humano."


@dataclass
class Resultado:
    resposta: str  # o texto final para o cliente
    passos: int  # quantas vezes o LLM foi chamado
    mensagens: list = field(default_factory=list)  # a conversa completa, incluindo as mensagens "tool"
    chamadas: list = field(default_factory=list)  # [{"nome": ..., "argumentos": {...}, "resultado": {...}}]


def rodar_agente(
    pergunta: str,
    llm,
    ferramentas: dict,
    schemas: list[dict],
    system_prompt: str = SYSTEM_PROMPT,
    historico: list[dict] | None = None,
    max_passos: int = 5,
) -> Resultado:
    """Roda o loop do agente e devolve um Resultado.

    Detalhes que os testes cobram:
    - A mensagem de resultado de ferramenta tem o formato
        {"role": "tool", "tool_name": "<nome>", "content": json.dumps(resultado, ensure_ascii=False)}
    - "arguments" pode chegar como dict (Ollama) ou como string JSON (OpenAI). Aceite os dois.
    - Ferramenta que não existe, exceção dentro da ferramenta ou argumento errado:
      NÃO derrube o agente. Vire {"erro": "..."} e devolva ao modelo, para ele se corrigir.
    - Não altere a lista `historico` recebida.
    """
    raise NotImplementedError("CAJU-07")
