# Relatório de Comparação de Prompts

**Data**: 18/02/2026
**Dataset**: `prompt-optimization-challenge-resolved-eval` — **34 exemplos** (15 originais + 19 extras curados)
**Gerador**: Google Gemini 2.0 Flash
**Avaliador**: Google Gemini 2.5 Flash (LLM-as-a-Judge)
**Método**: Métricas customizadas com avaliador independente do gerador

---

## Resultados V1 vs V2

| Métrica                          |  V1 (Baseline)  |  V2 (Otimizado)  |  Meta (≥ 0.9)  |        Δ        |
| --------------------------------- | :--------------: | :--------------: | :-------------: | :---------------: |
| **Tone**                    |      0.9476      | **0.9741** |    ✅ ambos    | **+0.0265** |
| **Acceptance Criteria**     |    0.8838 ❌    | **0.9688** |    ✅ só V2    | **+0.0850** |
| **User Story Format**       |      0.9529      | **0.9894** |    ✅ ambos    | **+0.0365** |
| **Completeness**            |      0.9288      | **0.9721** |    ✅ ambos    | **+0.0433** |
| **F1 Score** *(auxiliar)* |      0.8325      |      0.8489      |       —       |      +0.0164      |
| **Média Oficial**          | **0.9283** | **0.9761** | ✅ só V2 total | **+0.0478** |

---

## 🏆 Análise

- **V1 (Baseline)**: REPROVADO. Falha em `acceptance_criteria` (0.88 < 0.9). O prompt zero-shot não produz cenários Gherkin consistentes com o modelo gemini-2.0-flash.
- **V2 (Otimizado)**: APROVADO. Supera V1 em **todas as 4 métricas**, com destaque para Acceptance Criteria (+8.5%), onde o Few-Shot com exemplos ricos em Gherkin faz diferença decisiva.
- **F1 Score**: Métrica auxiliar baseada em sobreposição de tokens (não oficial). Valores abaixo de 0.9 são esperados pois o modelo gera User Stories com vocabulário próprio.

## 🔬 Técnicas Aplicadas no V2

| Técnica                      | Impacto Observado                                                               |
| ----------------------------- | ------------------------------------------------------------------------------- |
| **Role Prompting**      | Tone consistentemente alto (0.97) — linguagem profissional e empática         |
| **Chain of Thought**    | Completeness 0.93→0.97 — seção "Contexto Técnico" preserva dados do bug    |
| **Few-Shot Learning**   | AC 0.88→0.97 — 2 exemplos ricos (simples + complexo com 4 cenários Gherkin)  |
| **Output Structuring**  | Format 0.95→0.99 — template rígido força estrutura "Como/Eu quero/Para que" |
| **Anti-preamble Rules** | Elimina "Claro!", "Com certeza!" — resposta começa direto no título          |
| **Persona Específica** | Evita "Como um usuário" genérico, melhora Format e Tone                       |

## 📐 Configuração de Avaliação

| Aspecto                    | Detalhe                                                                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Modelo Gerador**   | `gemini-2.0-flash` (mesmo para V1 e V2)                                                                                                           |
| **Modelo Avaliador** | `gemini-2.5-flash` (LLM-as-Judge independente)                                                                                                    |
| **Justificativa**    | O avaliador precisa ser mais capaz que o gerador para distinguir qualidade. Usar o mesmo modelo (2.0) como juiz resulta em teto artificial de ~0.87 |

## 🔗 Links LangSmith

- **Dataset (34 exemplos)**: [Ver no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21?tab=1)
- **Experimento V1**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=6ad15198-3eb4-44ac-b1ca-9d7e8762e764)
- **Experimento V2**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=f18833fe-490e-4021-9f9e-582a1aab8cdb)
- **Comparação V1 x V2**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=f18833fe-490e-4021-9f9e-582a1aab8cdb%2C6ad15198-3eb4-44ac-b1ca-9d7e8762e764&source=f18833fe-490e-4021-9f9e-582a1aab8cdb)
