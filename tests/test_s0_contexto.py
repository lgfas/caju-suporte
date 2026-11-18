"""Testes de aceite da Sprint 0 (CAJU-02). Rode com: pytest tests/test_s0_contexto.py -v"""

import copy

from caju.contexto import (
    TOKENS_POR_MENSAGEM,
    cortar_historico,
    estimar_tokens,
    montar_mensagens,
    tokens_da_conversa,
)

SYSTEM = {"role": "system", "content": "Você é o assistente da Loja Caju."}


def msg(role, n_chars):
    return {"role": role, "content": "x" * n_chars}


# --- estimar_tokens ---------------------------------------------------------

def test_texto_vazio_tem_zero_tokens():
    assert estimar_tokens("") == 0


def test_regra_de_bolso_quatro_caracteres_por_token_arredondando_para_cima():
    assert estimar_tokens("abcd") == 1
    assert estimar_tokens("abcde") == 2
    assert estimar_tokens("x" * 400) == 100


# --- tokens_da_conversa -----------------------------------------------------

def test_conversa_soma_conteudo_mais_custo_fixo_por_mensagem():
    mensagens = [msg("system", 40), msg("user", 8)]
    assert tokens_da_conversa(mensagens) == 10 + 2 + 2 * TOKENS_POR_MENSAGEM


def test_conversa_aceita_mensagem_sem_content():
    # Mensagens do assistente que só chamam ferramenta podem vir com content None.
    mensagens = [{"role": "assistant", "content": None}]
    assert tokens_da_conversa(mensagens) == TOKENS_POR_MENSAGEM


# --- montar_mensagens -------------------------------------------------------

def test_montar_coloca_system_primeiro_e_pergunta_por_ultimo():
    historico = [{"role": "user", "content": "oi"}, {"role": "assistant", "content": "olá!"}]
    resultado = montar_mensagens(SYSTEM["content"], historico, "cadê meu pedido?")
    assert resultado[0] == SYSTEM
    assert resultado[1:3] == historico
    assert resultado[-1] == {"role": "user", "content": "cadê meu pedido?"}
    assert len(resultado) == 4


def test_montar_nao_altera_o_historico_recebido():
    historico = [{"role": "user", "content": "oi"}]
    original = copy.deepcopy(historico)
    montar_mensagens("sys", historico, "nova")
    assert historico == original


# --- cortar_historico -------------------------------------------------------

def test_cortar_nao_mexe_quando_cabe():
    mensagens = [SYSTEM, msg("user", 20), msg("assistant", 20), msg("user", 20)]
    assert cortar_historico(mensagens, max_tokens=10_000) == mensagens


def test_cortar_remove_as_mensagens_mais_antigas_primeiro():
    antiga = {"role": "user", "content": "a" * 400}
    media = {"role": "assistant", "content": "b" * 400}
    nova = {"role": "user", "content": "c" * 40}
    mensagens = [SYSTEM, antiga, media, nova]
    limite = tokens_da_conversa([SYSTEM, media, nova])
    resultado = cortar_historico(mensagens, max_tokens=limite)
    assert resultado == [SYSTEM, media, nova]


def test_cortar_sempre_mantem_system_e_ultima_mensagem():
    mensagens = [SYSTEM, msg("user", 4000), msg("assistant", 4000), msg("user", 4000)]
    resultado = cortar_historico(mensagens, max_tokens=1)
    assert resultado == [SYSTEM, mensagens[-1]]


def test_cortar_funciona_sem_system_prompt():
    mensagens = [msg("user", 400), msg("assistant", 400), msg("user", 40)]
    limite = tokens_da_conversa(mensagens[1:])
    assert cortar_historico(mensagens, max_tokens=limite) == mensagens[1:]


def test_cortar_nao_altera_a_lista_recebida():
    mensagens = [SYSTEM, msg("user", 4000), msg("user", 40)]
    original = copy.deepcopy(mensagens)
    cortar_historico(mensagens, max_tokens=1)
    assert mensagens == original
