# Diário de engenharia · Caju Suporte

Escreva com suas palavras, como se fosse explicar para um colega. Frases curtas valem mais que texto copiado.

---

## Sprint 0

### CAJU-01 · Ambiente
- Modelo: qwen3:8b no Ollama 0.40.7 (pacote ollama-cuda do Arch)
- Máquina: Omarchy, Ryzen 5 5600X, 16 GB de RAM, RTX 3060 com 12 GB de memória de vídeo
- Memória de vídeo: 606 MiB com o desktop; 6025 MiB com o modelo carregado → o modelo ocupa ~5,4 GB
- `ollama ps`: 100% GPU, contexto de 4096 tokens
- Latência quente (--verbose): 4,4 s no total; carga 0,6 ms; 254 tokens gerados a 59 tokens/s.
  Quase todo o tempo foi geração, e quase toda a geração foi raciocínio ("Thinking").
- Latência fria: carga 4,9 s; total 16,5 s; tokens gerados 689
- Observação: perguntei a data e ele raciocinou que não sabia, mas respondeu "30/10/2024" com confiança.
- Infra: o espelho do Omarchy deu 404 (lista de pacotes velha, resolvido com `omarchy update`) e o disco encheu (resolvido limpando o cache do pacman e snapshots antigos)

### CAJU-03 · Chat no terminal
1. O que o think faz e onde o raciocínio aparece na resposta?
- O `think` é um campo no chat que habilita ou desabilita (true ou false) o pensamento na saída da resposta. Quando enviei sem esse parâmetro, ele veio pré-setado como true, saindo o campo `thinking` no output com o raciocinio utilizado para chegar à resposta
- Habilitar ou desabilitar o `think` traz consigo uma questão de custo X qualidade. O que vou escrever a seguir é baseado em testes que fiz no terminal. Quando o parâmetro está desabilitado, ele tem um custo menor: gasta menos tokens e a resposta é gerada em um tempo menor. Ainda sobre o quesito custo, quando o parâmetro está habilitado, são gastos mais tokens e a resposta demorou quase o dobro de tempo para ser gerada. No entanto, quando falamos sobre qualidade das respostas geradas, as respostas geradas para o `think=True` foram mais corretas do que as para `think=False`, tendo uma qualidade maior.
- No momento, acredito que quero mais agilidade no meu chat(), pois não é interessante que o cliente fique esperando tanto tempo, vou apostar na rapidex do `think=False` por padrão.

### CAJU-04 · Experimentos
**E1 · Temperatura**
- Esperava:
- Aconteceu:
- Por quê:

**E2 · Alucinação**
- Esperava:
- Aconteceu:
- Por quê:

**E3 · Esquecimento**
- Esperava:
- Aconteceu:
- Por quê:

**E4 · System prompt**
- Esperava:
- Aconteceu:
- Por quê:

**E5 · Tokens reais**
| Conversa | Estimativa (tokens_da_conversa) | Real (prompt_eval_count) | Caracteres por token |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Perguntas de estudo
1.
2.
3.
4.
5.

### O que mais me surpreendeu nesta sprint

---

## Sprint 1

### Portão 1 · roteiro (cole a saída do agente)
```
```
Acertos: _ de 5

### Perguntas de estudo
1.
2.
3.
4.
5.
6.

### O que mais me surpreendeu nesta sprint
