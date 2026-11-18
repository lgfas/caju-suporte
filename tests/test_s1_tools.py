"""Testes de aceite da Sprint 1 (CAJU-05 e CAJU-06). Rode com: pytest tests/test_s1_tools.py -v"""

import inspect
import json

import pytest

from caju import tools


@pytest.fixture(autouse=True)
def chamados_isolados(tmp_path, monkeypatch):
    """Cada teste grava chamados num arquivo temporário, nunca no data/ de verdade."""
    arquivo = tmp_path / "chamados.json"
    monkeypatch.setattr(tools, "ARQUIVO_CHAMADOS", arquivo)
    return arquivo


# --- CAJU-05: buscar_pedido -------------------------------------------------

def test_buscar_pedido_existente():
    pedido = tools.buscar_pedido("CJ-1002")
    assert pedido["id"] == "CJ-1002"
    assert pedido["status"] == "enviado"
    assert pedido["rastreio"] == "BR482911204CJ"
    assert pedido["previsao_entrega"] == "2026-11-11"


def test_buscar_pedido_tolera_argumento_baguncado():
    # Modelos mandam argumentos imperfeitos. Sua ferramenta deve ser tolerante.
    assert tools.buscar_pedido("  cj-1002 ")["id"] == "CJ-1002"
    assert tools.buscar_pedido("1002")["id"] == "CJ-1002"


def test_buscar_pedido_inexistente_devolve_erro_legivel_sem_excecao():
    resultado = tools.buscar_pedido("CJ-9999")
    assert set(resultado) == {"erro"}
    assert "CJ-9999" in resultado["erro"]


def test_buscar_pedido_nao_expoe_email_do_cliente():
    # Menor privilégio: o modelo não precisa do e-mail para falar do pedido.
    assert "email" not in tools.buscar_pedido("CJ-1002")


# --- CAJU-05: listar_pedidos ------------------------------------------------

def test_listar_pedidos_do_cliente_mais_recente_primeiro():
    pedidos = tools.listar_pedidos("ana.souza@example.com")
    assert [p["id"] for p in pedidos] == ["CJ-1002", "CJ-1001"]


def test_listar_pedidos_devolve_so_o_resumo():
    resumo = tools.listar_pedidos("bruno.lima@example.com")[0]
    assert set(resumo) == {"id", "data", "status", "total"}


def test_listar_pedidos_ignora_maiusculas_e_espacos_no_email():
    assert len(tools.listar_pedidos("  Bruno.Lima@Example.com ")) == 2


def test_listar_pedidos_de_email_desconhecido_devolve_lista_vazia():
    assert tools.listar_pedidos("ninguem@example.com") == []


# --- CAJU-05: abrir_chamado -------------------------------------------------

def test_abrir_chamado_grava_e_devolve_protocolo(chamados_isolados):
    resultado = tools.abrir_chamado(
        email="bruno.lima@example.com",
        assunto="Prensa chegou trincada",
        descricao="Pedido CJ-1004, vidro trincado.",
    )
    assert resultado["protocolo"] == "CH-0001"
    salvos = json.loads(chamados_isolados.read_text(encoding="utf-8"))
    assert salvos[0]["protocolo"] == "CH-0001"
    assert salvos[0]["email"] == "bruno.lima@example.com"
    assert salvos[0]["status"] == "aberto"


def test_abrir_chamado_numera_em_sequencia():
    tools.abrir_chamado("ana.souza@example.com", "Atraso", "CJ-1002 atrasado")
    segundo = tools.abrir_chamado("ana.souza@example.com", "Outro", "Outra coisa")
    assert segundo["protocolo"] == "CH-0002"


def test_abrir_chamado_sem_assunto_devolve_erro(chamados_isolados):
    resultado = tools.abrir_chamado("ana.souza@example.com", "   ", "algo")
    assert "erro" in resultado
    assert not chamados_isolados.exists()


# --- CAJU-06: registro e schemas --------------------------------------------

def test_registro_tem_as_tres_ferramentas():
    assert set(tools.FERRAMENTAS) == {"buscar_pedido", "listar_pedidos", "abrir_chamado"}


def test_cada_ferramenta_tem_um_schema_com_o_mesmo_nome():
    nomes = [s["function"]["name"] for s in tools.SCHEMAS]
    assert sorted(nomes) == sorted(tools.FERRAMENTAS)
    for s in tools.SCHEMAS:
        assert s["type"] == "function"


@pytest.mark.parametrize("schema", tools.SCHEMAS, ids=lambda s: s["function"]["name"])
def test_schema_bate_com_a_assinatura_da_funcao(schema):
    fn = tools.FERRAMENTAS[schema["function"]["name"]]
    params = inspect.signature(fn).parameters
    obrigatorios = {n for n, p in params.items() if p.default is inspect.Parameter.empty}

    corpo = schema["function"]["parameters"]
    assert corpo["type"] == "object"
    assert set(corpo["properties"]) == set(params)
    assert set(corpo.get("required", [])) == obrigatorios
    for nome, prop in corpo["properties"].items():
        assert prop["type"] == "string", nome
        assert len(prop.get("description", "")) >= 10, f"descreva o parâmetro {nome}"


@pytest.mark.parametrize("schema", tools.SCHEMAS, ids=lambda s: s["function"]["name"])
def test_descricao_da_ferramenta_explica_quando_usar(schema):
    # A descrição é o que o modelo lê para decidir. Seja específico.
    assert len(schema["function"]["description"]) >= 40
