"""Sprint 0 · CAJU-02: gerenciar a janela de contexto.

O modelo não tem memória. Toda chamada recebe a conversa inteira como uma lista de mensagens:
    [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}, ...]
Essa lista tem um limite de tamanho (a janela de contexto), medido em tokens. Aqui você vai
montar essa lista e cortá-la quando ela crescer demais.
"""

# Cada mensagem custa alguns tokens além do texto (marcadores de papel, separadores).
TOKENS_POR_MENSAGEM = 4


def estimar_tokens(texto: str) -> int:
    """Estimativa rápida: cerca de 4 caracteres por token, arredondando para cima.

    É só uma regra de bolso. O número exato depende do tokenizador de cada modelo;
    em português ela costuma errar para menos. Você vai medir isso no diário.
    """
    raise NotImplementedError("CAJU-02")


def tokens_da_conversa(mensagens: list[dict]) -> int:
    """Soma estimar_tokens(content) + TOKENS_POR_MENSAGEM para cada mensagem.

    Atenção: o content pode ser None (mensagens que só chamam ferramenta).
    """
    raise NotImplementedError("CAJU-02")


def montar_mensagens(system_prompt: str, historico: list[dict], pergunta: str) -> list[dict]:
    """Devolve [system, *historico, user]. Não altere a lista `historico` recebida."""
    raise NotImplementedError("CAJU-02")


def cortar_historico(mensagens: list[dict], max_tokens: int) -> list[dict]:
    """Remove as mensagens MAIS ANTIGAS até a conversa caber em max_tokens.

    Regras:
    - Se a primeira mensagem for "system", ela nunca sai.
    - A última mensagem (a pergunta atual) nunca sai.
    - Se nem system + última cabem, devolva só essas duas.
    - Não altere a lista recebida: devolva uma nova.
    """
    raise NotImplementedError("CAJU-02")
