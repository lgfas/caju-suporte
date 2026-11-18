"""Testes de aceite da Sprint 1 (CAJU-07). Rode com: pytest tests/test_s1_agent.py -v

Aqui não tem Ollama: o LLM é um roteiro (tests/fakes.py). Assim você testa o SEU código,
o loop, e não o humor do modelo.
"""

import copy
import json

from caju.agent import MENSAGEM_ESCALONAMENTO, rodar_agente
from fakes import FakeLLM, SempreChamaFerramenta, chamada, resposta


def eco(texto: str) -> dict:
    return {"eco": texto}


def soma(a: str, b: str) -> dict:
    return {"total": int(a) + int(b)}


def quebra(motivo: str) -> dict:
    raise RuntimeError(f"banco fora do ar: {motivo}")


FERRAMENTAS = {"eco": eco, "soma": soma, "quebra": quebra}
SCHEMAS = [{"type": "function", "function": {"name": n, "description": "teste", "parameters": {}}} for n in FERRAMENTAS]


def rodar(llm, **kwargs):
    kwargs.setdefault("system_prompt", "Você é um teste.")
    return rodar_agente("pergunta do cliente", llm, FERRAMENTAS, SCHEMAS, **kwargs)


def mensagens_de_ferramenta(mensagens):
    return [m for m in mensagens if m["role"] == "tool"]


# --- caminho feliz ----------------------------------------------------------

def test_resposta_direta_sem_ferramenta():
    llm = FakeLLM([resposta("Olá! Como posso ajudar?")])
    r = rodar(llm)
    assert r.resposta == "Olá! Como posso ajudar?"
    assert r.passos == 1
    assert r.chamadas == []


def test_primeira_chamada_ao_llm_tem_system_pergunta_e_schemas():
    llm = FakeLLM([resposta("ok")])
    rodar(llm)
    mensagens, schemas = llm.recebido[0]
    assert mensagens[0] == {"role": "system", "content": "Você é um teste."}
    assert mensagens[-1] == {"role": "user", "content": "pergunta do cliente"}
    assert schemas == SCHEMAS


def test_uma_ferramenta_e_depois_a_resposta():
    llm = FakeLLM([chamada(("eco", {"texto": "CJ-1002"})), resposta("Seu pedido foi enviado.")])
    r = rodar(llm)

    assert r.resposta == "Seu pedido foi enviado."
    assert r.passos == 2
    assert r.chamadas == [{"nome": "eco", "argumentos": {"texto": "CJ-1002"}, "resultado": {"eco": "CJ-1002"}}]

    # Na 2ª chamada, o LLM precisa ver o próprio pedido de ferramenta e o resultado dela.
    mensagens, _ = llm.recebido[1]
    assert mensagens[-2]["role"] == "assistant" and mensagens[-2]["tool_calls"]
    assert mensagens[-1]["role"] == "tool"
    assert mensagens[-1]["tool_name"] == "eco"
    assert json.loads(mensagens[-1]["content"]) == {"eco": "CJ-1002"}


def test_varias_ferramentas_no_mesmo_turno_rodam_em_ordem():
    llm = FakeLLM([chamada(("soma", {"a": "2", "b": "3"}), ("eco", {"texto": "oi"})), resposta("pronto")])
    r = rodar(llm)
    assert [c["nome"] for c in r.chamadas] == ["soma", "eco"]
    tool_msgs = mensagens_de_ferramenta(llm.recebido[1][0])
    assert [json.loads(m["content"]) for m in tool_msgs] == [{"total": 5}, {"eco": "oi"}]


def test_argumentos_em_texto_json_tambem_funcionam():
    # Ollama manda dict; a API da OpenAI manda string JSON. Seu loop deve aceitar os dois.
    llm = FakeLLM([chamada(("soma", '{"a": "10", "b": "5"}')), resposta("15")])
    r = rodar(llm)
    assert r.chamadas[0]["resultado"] == {"total": 15}


def test_conteudo_da_ferramenta_preserva_acentos():
    llm = FakeLLM([chamada(("eco", {"texto": "São Paulo"})), resposta("ok")])
    rodar(llm)
    assert "São Paulo" in mensagens_de_ferramenta(llm.recebido[1][0])[0]["content"]


# --- quando dá errado -------------------------------------------------------

def test_ferramenta_inexistente_vira_erro_para_o_modelo_e_o_loop_continua():
    llm = FakeLLM([chamada(("apagar_banco", {})), resposta("Desculpe, não consigo fazer isso.")])
    r = rodar(llm)
    assert r.resposta == "Desculpe, não consigo fazer isso."
    conteudo = json.loads(mensagens_de_ferramenta(llm.recebido[1][0])[0]["content"])
    assert "erro" in conteudo and "apagar_banco" in conteudo["erro"]


def test_excecao_na_ferramenta_vira_erro_para_o_modelo_e_o_loop_continua():
    llm = FakeLLM([chamada(("quebra", {"motivo": "manutenção"})), resposta("Sistema instável, tente mais tarde.")])
    r = rodar(llm)
    assert r.passos == 2
    conteudo = json.loads(mensagens_de_ferramenta(llm.recebido[1][0])[0]["content"])
    assert "erro" in conteudo
    assert r.chamadas[0]["resultado"] == conteudo


def test_argumento_errado_vira_erro_e_nao_derruba_o_agente():
    llm = FakeLLM([chamada(("soma", {"a": "1"})), resposta("faltou um número")])
    r = rodar(llm)
    assert r.resposta == "faltou um número"
    assert "erro" in r.chamadas[0]["resultado"]


def test_limite_de_passos_encerra_e_escalona_para_humano():
    llm = SempreChamaFerramenta()
    r = rodar(llm, max_passos=3)
    assert llm.chamadas == 3
    assert r.passos == 3
    assert r.resposta == MENSAGEM_ESCALONAMENTO
    assert "humano" in MENSAGEM_ESCALONAMENTO.lower() or "atendente" in MENSAGEM_ESCALONAMENTO.lower()


# --- histórico --------------------------------------------------------------

def test_historico_entra_entre_o_system_e_a_pergunta_e_nao_e_alterado():
    historico = [{"role": "user", "content": "meu e-mail é ana@example.com"}, {"role": "assistant", "content": "Anotado!"}]
    original = copy.deepcopy(historico)
    llm = FakeLLM([resposta("ok")])
    r = rodar(llm, historico=historico)

    mensagens, _ = llm.recebido[0]
    assert mensagens[1:3] == original
    assert historico == original
    # O resultado traz a conversa completa, pronta para virar o histórico do próximo turno.
    assert r.mensagens[-1] == {"role": "assistant", "content": "ok"}
