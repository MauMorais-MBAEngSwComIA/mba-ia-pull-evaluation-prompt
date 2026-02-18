# Prompt Evaluation: Bug to User Story

Pipeline completo de **Engenharia de Prompt** para converter Bug Reports em User Stories no padrão INVEST, com avaliação automatizada via **LangChain** e **LangSmith**.

## 🎯 Objetivo

Transformar relatos de bugs técnicos (muitas vezes curtos ou confusos) em User Stories estruturadas, com critérios de aceite claros e contexto técnico preservado. O projeto demonstra como técnicas avançadas de Prompt Engineering melhoram a qualidade de saída de LLMs de forma mensurável.

## 🛠️ Stack Tecnológico

| Componente      | Tecnologia                 |
| --------------- | -------------------------- |
| Linguagem       | Python 3.9+                |
| Orquestração  | LangChain                  |
| Observabilidade | LangSmith                  |
| LLM (Gerador)   | Google Gemini 2.0 Flash    |
| LLM (Avaliador) | Google Gemini 2.5 Flash    |
| Métricas       | LLM-as-a-Judge customizado |
| Testes          | Pytest                     |

---

## 🔬 Técnicas Aplicadas (Fase 2)

O prompt V2 combina **4 técnicas avançadas** de Prompt Engineering:

### 1. Role Prompting (Persona)

Define uma persona especializada de **Product Owner Sênior** com 15 anos de experiência em metodologias ágeis.

```
Voce e um Product Owner Senior com 15 anos de experiencia em metodologias ageis.
Sua especialidade e transformar Bug Reports em User Stories profissionais e completas.
```

> **Impacto:** Direciona o LLM a adotar vocabulário técnico adequado e priorizar valor de negócio. Tone atingiu **0.97** com `gemini-2.0-flash`.

### 2. Chain of Thought (CoT) — Via Seções Estruturadas

Em vez de raciocínio interno escondido em tags XML, o CoT é externalizado na saída via seção **Contexto Técnico**, que obriga o modelo a analisar e preservar todos os dados técnicos do bug.

```
## Contexto Tecnico
- **Problema identificado**: [descrição técnica extraída do bug]
- **Componentes afetados**: [lista de componentes]
- **Metricas/Limites**: [dados numéricos]
```

> **Impacto:** Completeness subiu de 0.88 (V1) para **0.97** (V2) — o modelo preserva todos os dados técnicos do bug original.

### 3. Few-Shot Learning

Um exemplo completo inline (Bug Report → User Story com 3 cenários Gherkin + Contexto Técnico) serve como "molde" para o formato e nível de detalhe esperado.

> **Impacto:** Acceptance Criteria subiu de 0.88 (V1) para **0.97** (V2). O exemplo rico em Gherkin ensina o modelo a produzir cenários específicos e testáveis.

### 4. Output Structuring (Formato Obrigatório)

8 regras críticas explícitas + template rígido que força a estrutura exata da User Story:

- **Anti-preamble**: Proíbe saudações como "Claro!", forçando resposta direta
- **Persona específica**: Proíbe "Como um usuário" genérico
- **Quantidade mínima**: 3-7 cenários Gherkin obrigatórios
- **Benefício real**: "Para que" deve expressar valor mensurável

> **Impacto:** User Story Format atingiu **0.99** — a melhor métrica do V2.

---

## 📊 Resultados Finais

Avaliação com **34 exemplos** (15 originais + 19 curados). Gerador: `gemini-2.0-flash`. Avaliador: `gemini-2.5-flash` (LLM-as-Judge independente).

| Métrica                          | V1 (Baseline) |  V2 (Otimizado)  | Meta (≥ 0.9) |   Δ Melhoria   |
| --------------------------------- | :-----------: | :--------------: | :-----------: | :--------------: |
| **Tone**                    |    0.9476    | **0.9741** |   ✅ ambos   | **+0.027** |
| **Acceptance Criteria**     |   0.8838 ❌   | **0.9688** |   ✅ só V2   | **+0.085** |
| **User Story Format**       |    0.9529    | **0.9894** |   ✅ ambos   | **+0.037** |
| **Completeness**            |    0.9288    | **0.9721** |   ✅ ambos   | **+0.043** |
| **F1 Score** *(auxiliar)* |    0.8325    |      0.8489      |      —      |      +0.016      |

> **Destaque:** O V1 falha no threshold de Acceptance Criteria (0.88 < 0.9). O V2 resolve esta deficiência (+8.5%) e melhora **todas** as demais métricas simultaneamente. O F1 Score é uma métrica auxiliar (sobreposição de tokens) — valores abaixo de 0.9 são esperados.

### 📐 Configuração de Avaliação

| Aspecto                    | Detalhe                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Modelo Gerador**   | `gemini-2.0-flash` (mesmo para V1 e V2)                                                            |
| **Modelo Avaliador** | `gemini-2.5-flash` (LLM-as-Judge independente)                                                     |
| **Justificativa**    | O avaliador precisa ser mais capaz que o gerador para distinguir qualidade entre "bom" e "excelente" |

### 🔗 Experimentos no LangSmith

- **Dataset (34 exemplos)**: [Ver no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21?tab=1)
- **Experimento V1**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=6ad15198-3eb4-44ac-b1ca-9d7e8762e764)
- **Experimento V2**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=f18833fe-490e-4021-9f9e-582a1aab8cdb)
- **Comparação V1 x V2**: [Ver resultados no LangSmith](https://smith.langchain.com/o/4edf22f3-ecb6-499b-b514-311998f18731/datasets/6e40fce8-8415-4916-bf24-1aaf2b640f21/compare?selectedSessions=f18833fe-490e-4021-9f9e-582a1aab8cdb%2C6ad15198-3eb4-44ac-b1ca-9d7e8762e764&source=f18833fe-490e-4021-9f9e-582a1aab8cdb)

### 📸 Screenshots

![Resultado do Experimento V2 no LangSmith](docs/screenshots/experiment_v2.png)

![Comparação V1 vs V2 no LangSmith](docs/screenshots/comparison_v1_v2.png)

---

## 🚀 Como Executar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` a partir do template:

```bash
cp .env.example .env
# Preencha: LANGSMITH_API_KEY, GOOGLE_API_KEY, LANGCHAIN_PROJECT
```

### Sincronizar Dataset com LangSmith

```bash
python src/upload_dataset.py
```

### Rodar Avaliação Completa (V1 e V2)

```bash
# Avaliar prompt V1 (baseline) — gerador 2.0, avaliador 2.5
python src/evaluate.py --prompt bug_to_user_story_v1 --model gemini-2.0-flash --evaluator-model gemini-2.5-flash

# Avaliar prompt V2 (otimizado) — gerador 2.0, avaliador 2.5
python src/evaluate.py --prompt bug_to_user_story_v2 --model gemini-2.0-flash --evaluator-model gemini-2.5-flash
```

### Exemplo Prático de Uso

**Entrada (Bug Report):**

```
O botão 'Salvar' na tela de perfil não funciona quando o nome
contém caracteres especiais (ç, ã, é). Retorna erro 500.
```

**Saída gerada pelo V2:**

```markdown
# Salvar Perfil de Usuario com Caracteres Especiais

**Como** um usuario cadastrado na plataforma,
**Eu quero** salvar meu perfil com qualquer caractere no nome sem encontrar erros,
**Para que** eu possa usar meu nome real e manter meus dados atualizados sem frustracoes.

## Criterios de Aceite

### Cenario 1: Salvamento bem-sucedido com caracteres especiais
- **Dado** que estou na tela de edicao de perfil
- **Quando** insiro um nome com caracteres especiais e clico em Salvar
- **Entao** o perfil deve ser salvo com sucesso retornando HTTP 200
- **E** o nome deve ser exibido corretamente em todas as paginas

### Cenario 2: Prevencao do Erro 500 atual
- **Dado** que o sistema recebe um nome com caracteres nao-ASCII
- **Quando** tenta persistir os dados
- **Entao** nao deve ocorrer Erro 500

### Cenario 3: Validacao no frontend antes do envio
- **Dado** que estou preenchendo o campo de nome
- **Quando** insiro caracteres validos de qualquer idioma
- **Entao** o frontend deve aceitar a entrada sem bloqueio

## Contexto Tecnico
- **Problema identificado**: Erro 500 ao salvar perfil com caracteres especiais
- **Componentes afetados**: Tela de perfil, API de salvamento, banco de dados
- **Severidade**: Alta
```

### Testes de Validação do Prompt

```bash
pytest tests/test_prompts.py -v
```

**Resultado esperado:** 30 testes passando, validando:

- Existência de System Prompt
- Definição de Persona (Role)
- Exigência de formato Markdown/User Story
- Presença de Few-Shot examples
- Ausência de marcadores `[TODO]`
- Uso de pelo menos 2 técnicas (via metadados YAML)

### Push do Prompt para o LangSmith Hub

```bash
python src/push_prompts.py
```

---

## 📂 Estrutura do Projeto

```
prompt-evaluation-langchain-langsmith/
├── prompts/
│   ├── bug_to_user_story_v1.yml      # Prompt Original (Baseline)
│   └── bug_to_user_story_v2.yml      # Prompt Otimizado (4 técnicas)
├── src/
│   ├── evaluate.py                   # Motor de avaliação (LLM-as-Judge)
│   ├── upload_dataset.py             # Sincronização do dataset com LangSmith
│   ├── push_prompts.py               # Publicação no LangSmith Hub
│   ├── pull_prompts.py               # Captura do LangSmith Hub
│   ├── metrics.py                    # Métricas customizadas (Tone, AC, Format, Completeness)
│   └── utils.py                      # Utilitários e configuração de LLM
├── datasets/
│   └── bug_to_user_story.jsonl       # Dataset de avaliação (34 exemplos)
├── tests/
│   └── test_prompts.py               # 30 testes automatizados de validação
├── docs/                             # Documentação e critérios do desafio
├── .env.example                      # Template de configuração
├── requirements.txt                  # Dependências Python
└── README.md                         # Este arquivo
```

---

## 📋 Iterações do Prompt (Histórico)

| Versão      | Modelo    | Técnicas                                  |     Comp.     |       AC       |     Format     |      Tone      |
| ------------ | --------- | ------------------------------------------ | :------------: | :------------: | :------------: | :------------: |
| **V1** | 2.0-flash | Zero-shot                                  |      0.93      |    0.88 ❌    |      0.95      |      0.95      |
| **V2** | 2.0-flash | Role + CoT + Few-Shot + Output Structuring | **0.97** | **0.97** | **0.99** | **0.97** |

> O V2 foi desenvolvido em 4 iterações: (1) XML Isolation + CoT interno (V2 original), (2) remoção do XML + CoT na saída + 2 Few-Shot ricos (V3), (3) análise profunda dos avaliadores + anti-preamble + persona específica + regras de quantidade (V4), (4) promoção da V4 para V2 final.

---

**Desenvolvido como parte do Desafio Técnico de Prompt Engineering — MBA em Engenharia de Software com IA.**
