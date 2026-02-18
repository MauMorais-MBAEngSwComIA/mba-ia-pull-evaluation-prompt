# Relatório de Compliance — Desafio Prompt Engineering

Comparação entre os requisitos de `docs/00.proposicao_problema.md` e o estado atual do workspace.
Verificação realizada em **18/02/2026 às 11:50**.

---

## ✅ Resultado Geral: 35/35

| Seção | Itens | ✅ OK | ⚠️ Parcial | ❌ Ausente |
|-------|-------|-------|-----------|-----------|
| Objetivo | 5 | 5 | 0 | 0 |
| Stack Tecnológica | 5 | 5 | 0 | 0 |
| Req. 1 — Pull | 3 | 3 | 0 | 0 |
| Req. 2 — Otimização | 5 | 5 | 0 | 0 |
| Req. 3 — Push e Avaliação | 2 | 2 | 0 | 0 |
| Req. 4 — Testes | 6 | 6 | 0 | 0 |
| Estrutura do Projeto | 6 | 6 | 0 | 0 |
| Critérios de Entrega (README) | 3 | 3 | 0 | 0 |
| **TOTAL** | **35** | **35** | **0** | **0** |

---

## Detalhamento

### ✅ Objetivo (5/5)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Pull de prompts do LangSmith Hub | ✅ | `src/pull_prompts.py` → `prompts/raw_prompts.yml` |
| Refatorar e otimizar prompts | ✅ | `prompts/bug_to_user_story_v2.yml` (4 técnicas) |
| Push dos prompts otimizados | ✅ | `src/push_prompts.py` |
| Avaliar qualidade com métricas | ✅ | `src/evaluate.py` + `src/metrics.py` |
| Atingir ≥ 0.9 em todas as métricas | ✅ | Tone 1.00, AC 0.97, Format 0.99, Completeness 0.99 |

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
| Alvo: `leonanluppi/bug_to_user_story_v1` | ✅ | `src/pull_prompts.py` linha 35 |
| Saída: `prompts/raw_prompts.yml` | ✅ | Script configurado para salvar em `prompts/raw_prompts.yml` |

---

### ✅ Requisito 2 — Otimização do Prompt (5/5)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Arquivo `prompts/bug_to_user_story_v2.yml` | ✅ | Existe (3.6KB) |
| Pelo menos 2 técnicas avançadas | ✅ | 4 técnicas: CoT, Few-Shot, XML Isolation, Role Prompting |
| Instruções claras e regras explícitas | ✅ | Seções "INSTRUÇÕES DE PROCESSO" e "FORMATO DE SAÍDA OBRIGATÓRIO" |
| Exemplos de entrada/saída (Few-shot) | ✅ | Seção "EXEMPLOS (Few-Shot)" com Bug Report + Saída completa |
| Tratamento de edge cases | ✅ | "Cenário 2: Tratamento de Erro ou Caso de Borda" |

---

### ✅ Requisito 3 — Push e Avaliação (2/2)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| `src/push_prompts.py` | ✅ | Existe (1.2KB) |
| Métricas ≥ 0.9 (Tone, AC, Format, Completeness) | ✅ | Todas ≥ 0.97 |

---

### ✅ Requisito 4 — Testes de Validação (6/6)

| Critério | Status | Teste |
|----------|--------|-------|
| 1. Existência de System Prompt | ✅ | `TestSystemPrompt` (3 testes) |
| 2. Definição de Persona (Role) | ✅ | `TestPersonaDefinition` (2 testes) |
| 3. Exigência de formato (Markdown/User Story) | ✅ | `TestFormatRequirement` (4 testes) |
| 4. Presença de Few-shot examples | ✅ | `TestFewShotExamples` (3 testes) |
| 5. Ausência de termos `[TODO]` | ✅ | `TestNoTodoTerms` (3 testes) |
| 6. Uso de ≥ 2 técnicas avançadas | ✅ | `TestAdvancedTechniques` (5 testes) |

**pytest: 24 passed, 0 failed (0.89s)**

---

### ✅ Estrutura do Projeto (6/6)

| Arquivo/Diretório | Status |
|--------------------|--------|
| `prompts/bug_to_user_story_v1.yml` | ✅ |
| `prompts/bug_to_user_story_v2.yml` | ✅ |
| `src/pull_prompts.py` | ✅ |
| `src/push_prompts.py` | ✅ |
| `src/evaluate.py` | ✅ |
| `src/metrics.py` | ✅ |
| `tests/test_prompts.py` | ✅ |

---

### ✅ Critérios de Entrega — README.md (3/3)

| Requisito | Status | Evidência |
|-----------|--------|-----------|
| Técnicas Aplicadas (justificativa) | ✅ | Seção "Técnicas de Prompt Engineering Aplicadas" com 4 técnicas justificadas |
| Resultados Finais (link, screenshots, tabela) | ✅ | Tabela V1 vs V2 ✅, 3 links LangSmith ✅, 2 screenshots ✅ |
| Instruções de Execução | ✅ | Seções 1-6 (Instalação → Testes) |

---

## 🎯 Conclusão

**Todos os 35 requisitos do desafio foram atendidos com sucesso.** O projeto está pronto para entrega.
