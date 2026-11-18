"""Sprint 1 · CAJU-05 e CAJU-06: as ferramentas do agente.

Uma ferramenta é uma função Python comum. O modelo não a executa: ele só lê o SCHEMA dela
(nome, descrição, parâmetros) e responde "quero chamar buscar_pedido com pedido_id=CJ-1002".
Quem executa é o loop do agente (agent.py).

Regras para toda ferramenta deste arquivo:
- Nunca levante exceção para erro esperado (pedido não existe, campo vazio).
  Devolva {"erro": "mensagem que o modelo consiga entender"}.
- Devolva só o que o modelo precisa saber (menor privilégio).
- Seja tolerante com argumentos imperfeitos: o modelo erra maiúsculas, espaços, prefixos.
- Use ARQUIVO_PEDIDOS e ARQUIVO_CHAMADOS deste módulo (os testes trocam esses caminhos).
"""

import json  # noqa: F401  (você vai precisar)
from datetime import datetime  # noqa: F401

from caju.config import ARQUIVO_CHAMADOS, ARQUIVO_PEDIDOS  # noqa: F401


def buscar_pedido(pedido_id: str) -> dict:
    """Detalhes de um pedido pelo código.

    - Aceita "CJ-1002", " cj-1002 " e "1002".
    - Devolve o pedido de data/pedidos.json SEM o campo "email".
    - Se não existir: {"erro": "Pedido CJ-9999 não encontrado."} (o código precisa aparecer na mensagem).
    """
    raise NotImplementedError("CAJU-05")


def listar_pedidos(email: str) -> list[dict]:
    """Resumo dos pedidos de um cliente, do mais recente para o mais antigo.

    - Cada item tem só: id, data, status, total.
    - Ignora maiúsculas e espaços no e-mail.
    - E-mail desconhecido devolve [].
    """
    raise NotImplementedError("CAJU-05")


def abrir_chamado(email: str, assunto: str, descricao: str) -> dict:
    """Registra um chamado para o time humano em ARQUIVO_CHAMADOS (uma lista JSON).

    - Protocolos em sequência: CH-0001, CH-0002...
    - Cada chamado salvo tem pelo menos: protocolo, email, assunto, descricao, status="aberto", criado_em.
    - Devolve {"protocolo": "CH-0001", "status": "aberto"}.
    - Assunto vazio (ou só espaços): devolve {"erro": ...} e NÃO grava nada.
    - Salve com ensure_ascii=False para os acentos ficarem legíveis.
    """
    raise NotImplementedError("CAJU-05")


# --- CAJU-06: registro e schemas ---------------------------------------------

# Nome que o modelo usa -> função que o loop executa.
FERRAMENTAS = {
    "buscar_pedido": buscar_pedido,
    "listar_pedidos": listar_pedidos,
    "abrir_chamado": abrir_chamado,
}

# O que o modelo enxerga. O primeiro já está pronto como exemplo; escreva os outros dois.
# A descrição é a parte mais importante: é com ela que o modelo decide QUANDO usar a ferramenta.
SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_pedido",
            "description": (
                "Busca os detalhes de UM pedido pelo código (ex.: CJ-1002): status, itens, "
                "código de rastreio e previsão de entrega. Use quando o cliente informar o código."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pedido_id": {"type": "string", "description": "Código do pedido, como CJ-1002"},
                },
                "required": ["pedido_id"],
            },
        },
    },
    # TODO CAJU-06: schema de listar_pedidos
    # TODO CAJU-06: schema de abrir_chamado
]
