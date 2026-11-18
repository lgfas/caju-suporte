"""LLM falso para testar o loop do agente sem Ollama: rápido e sempre igual."""

import copy


def resposta(texto):
    """Mensagem do assistente que responde ao cliente (encerra o loop)."""
    return {"role": "assistant", "content": texto}


def chamada(*pares):
    """Mensagem do assistente pedindo ferramentas: chamada(("buscar_pedido", {"pedido_id": "CJ-1"}))."""
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [{"function": {"name": nome, "arguments": args}} for nome, args in pares],
    }


class FakeLLM:
    """Devolve as respostas do roteiro, em ordem, e grava o que recebeu em cada chamada."""

    def __init__(self, roteiro):
        self.roteiro = list(roteiro)
        self.recebido = []  # lista de (mensagens, schemas), uma por chamada

    def __call__(self, mensagens, schemas):
        self.recebido.append((copy.deepcopy(mensagens), schemas))
        if not self.roteiro:
            raise AssertionError("O agente chamou o LLM mais vezes do que o roteiro previa")
        return self.roteiro.pop(0)


class SempreChamaFerramenta:
    """Um LLM 'teimoso' que nunca para de pedir ferramenta. Serve para testar o limite de passos."""

    def __init__(self):
        self.chamadas = 0

    def __call__(self, mensagens, schemas):
        self.chamadas += 1
        return chamada(("eco", {"texto": "de novo"}))
