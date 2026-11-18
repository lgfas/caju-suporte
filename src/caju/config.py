"""Configuração lida de variáveis de ambiente (nunca coloque segredos no código)."""

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# Modelo do Ollama. Máquina mais fraca? export CAJU_MODELO=qwen3:4b
MODELO = os.environ.get("CAJU_MODELO", "qwen3:8b")

ARQUIVO_PEDIDOS = Path(os.environ.get("CAJU_PEDIDOS", RAIZ / "data" / "pedidos.json"))
ARQUIVO_CHAMADOS = Path(os.environ.get("CAJU_CHAMADOS", RAIZ / "data" / "chamados.json"))

SYSTEM_PROMPT = """Você é o assistente de atendimento da Loja Caju, uma loja online de cafés especiais e utensílios.
Responda em português do Brasil, de forma curta e cordial.
Se não souber uma informação sobre um pedido ou uma política, diga que vai verificar. Nunca invente."""
