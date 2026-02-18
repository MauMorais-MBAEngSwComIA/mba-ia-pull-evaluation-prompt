# Relatório de Compliance — Desafio Prompt Engineering

Comparação entre os requisitos dos critérios de entrega (novos) e o estado atual do workspace.  
Verificação realizada em **18/02/2026 às 19:34**.

---

## ✅ Resultado Geral: 38/38

| Seção | Itens | ✅ OK | ⚠️ Parcial | ❌ Ausente |
|-------|-------|-------|-----------|-----------| 
| Objetivo | 5 | 5 | 0 | 0 |
| Stack Tecnológica | 5 | 5 | 0 | 0 |
| Req. 1 — Pull | 3 | 3 | 0 | 0 |
| Req. 2 — Otimização | 6 | 6 | 0 | 0 |
| Req. 3 — Push e Avaliação | 3 | 3 | 0 | 0 |
| Req. 4 — Testes | 6 | 6 | 0 | 0 |
| Estrutura do Projeto | 7 | 7 | 0 | 0 |
| Critérios de Entrega (README) | 3 | 3 | 0 | 0 |
| **TOTAL** | **38** | **38** | **0** | **0** |

---

## Detalhamento

### ✅ Objetivo (5/5)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Pull de prompts do LangSmith Hub | ✅ | `src/pull_prompts.py` |
| Refatorar e otimizar prompts | ✅ | `prompts/bug_to_user_story_v2.yml` (4 técnicas) |
| Push dos prompts otimizados | ✅ | `src/push_prompts.py` |
| Avaliar qualidade com métricas | ✅ | `src/evaluate.py` + `src/metrics.py` |
| Atingir ≥ 0.9 em todas as métricas | ✅ | V2: Tone 0.97, AC 0.97, Format 0.99, Completeness 0.97 |

---

### ✅ Stack Tecnológica (5/5)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Python 3.9+ | ✅ | `requirements.txt`, executado com Python 3.13 |
| LangChain | ✅ | `langchain==0.3.13` |
| LangSmith | ✅ | `langsmith==0.2.7` |
| LangSmith Prompt Hub | ✅ | `pull_prompts.py` e `push_prompts.py` |
| Formato YAML | ✅ | `prompts/*.yml` |

---

### ✅ Requisito 1 — Pull do Prompt Inicial (3/3)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Configurar credenciais no `.env` | ✅ | `.env` + `.env.example` |
| Alvo: `leonanluppi/bug_to_user_story_v1` | ✅ | `src/pull_prompts.py` |
| Saída: `prompts/raw_prompts.yml` | ✅ | Arquivo gerado pelo script |

---

### ✅ Requisito 2 — Otimização do Prompt (6/6)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Arquivo `prompts/bug_to_user_story_v2.yml` | ✅ | Existe (4.2KB) |
| Pelo menos 2 técnicas avançadas | ✅ | 4 técnicas: Role Prompting, CoT, Few-Shot, Output Structuring |
| Campo `techniques` nos metadados YAML | ✅ | `techniques: ["role-prompting", "chain-of-thought", "few-shot-learning", "output-structuring"]` |
| Instruções claras e regras explícitas | ✅ | Seção "REGRAS CRITICAS" com 8 regras explícitas |
| Exemplos de entrada/saída (Few-shot) | ✅ | 1 exemplo completo (Bug → User Story com 3 cenários Gherkin + Contexto Técnico) |
| Tratamento de edge cases | ✅ | Cenário 3 obrigatório: "caso de borda" |

---

### ✅ Requisito 3 — Push e Avaliação (3/3)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| `src/push_prompts.py` | ✅ | Existe |
| Dataset com ≥ 15 exemplos originais preservados | ✅ | 15 exemplos do boilerplate + 19 extras = **34 total** |
| Métricas ≥ 0.9 (Tone, AC, Format, Completeness) | ✅ | V2: 0.97 / 0.97 / 0.99 / 0.97 — todas ≥ 0.9 |

---

### ✅ Requisito 4 — Testes de Validação (6/6)

| Critério | Status | Teste (dentro de `class TestPrompts`) |
|----------|--------|---------------------------------------|
| 1. `test_prompt_has_system_prompt` | ✅ | Verifica instruções de sistema não vazias |
| 2. `test_prompt_has_role_definition` | ✅ | Verifica persona "Product Owner" |
| 3. `test_prompt_mentions_format` | ✅ | Verifica formato Como/Eu quero/Para que |
| 4. `test_prompt_has_few_shot_examples` | ✅ | Verifica seção "Exemplo" + "Bug Report:" |
| 5. `test_prompt_no_todos` | ✅ | Verifica ausência de [TODO], [FIXME], PLACEHOLDER |
| 6. `test_minimum_techniques` | ✅ | Verifica campo `techniques` no YAML (≥ 2 itens) |

**pytest: 30 passed, 0 failed (1.21s)**

---

### ✅ Estrutura do Projeto (7/7)

| Arquivo/Diretório | Status |
|--------------------|--------|
| `prompts/bug_to_user_story_v1.yml` | ✅ |
| `prompts/bug_to_user_story_v2.yml` (com campo `techniques`) | ✅ |
| `src/pull_prompts.py` | ✅ |
| `src/push_prompts.py` | ✅ |
| `src/evaluate.py` | ✅ |
| `src/metrics.py` | ✅ |
| `tests/test_prompts.py` (class TestPrompts com 6 stubs) | ✅ |

---

### ✅ Critérios de Entrega — README.md (3/3)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Técnicas Aplicadas (Fase 2) com justificativa | ✅ | Seção "🔬 Técnicas Aplicadas (Fase 2)" com 4 técnicas e impacto |
| Resultados Finais (tabela, links, screenshots) | ✅ | Tabela V1 vs V2 ✅, links LangSmith ✅, screenshots ✅ |
| Como Executar com exemplo prático | ✅ | Seção "🚀 Como Executar" com Bug Report → User Story de exemplo |

---

## 📐 Configuração de Avaliação

| Aspecto | Detalhe |
|---|---|
| **Modelo Gerador** | `gemini-2.0-flash` (para V1 e V2) |
| **Modelo Avaliador** | `gemini-2.5-flash` (LLM-as-Judge) |
| **Dataset** | 34 exemplos (15 originais + 19 curados) |
| **Métricas** | Tone, Acceptance Criteria, User Story Format, Completeness |
| **Threshold** | ≥ 0.9 em todas as métricas oficiais |

---

## 🎯 Conclusão

**Todos os 38 requisitos do desafio (critérios atualizados) foram atendidos com sucesso.**

### Mudanças em relação à v1.0.0 (critérios originais)

| Item | v1.0.0 | v1.2.0 |
|---|---|---|
| Dataset | 10 exemplos (custom) | 34 exemplos (15 originais + 19 curados) |
| Testes | 24 testes (classes separadas) | 30 testes (`class TestPrompts` + extras) |
| YAML metadata | `tags` apenas | `tags` + `techniques` |
| Prompt V2 | XML Isolation + CoT | Role Prompting + Few-Shot rico + Output Structuring |
| Gerador | gemini-2.5-flash | gemini-2.0-flash |
| Avaliador | gemini-2.5-flash (mesmo) | gemini-2.5-flash (independente) |
| V1 scores | Todos ≥ 0.9 | AC=0.88 ❌ (os demais ≥ 0.9) |
| V2 scores | Todos ~0.93 | Todos ≥ 0.97 ✅ |
| README | Seções básicas | Seções exigidas + exemplo prático |
