"""
Testes de Validação do Prompt Otimizado (V2).

Critérios conforme docs/00.proposicao_problema.md:
1. Existência de System Prompt.
2. Definição de Persona (Role).
3. Exigência de formato (Markdown/User Story).
4. Presença de Few-shot examples.
5. Ausência de termos "[TODO]".
6. Uso de pelo menos 2 técnicas avançadas.
"""

import os
import pytest
from langchain_core.prompts import load_prompt

# Caminhos dos prompts
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')
V1_PATH = os.path.join(PROMPTS_DIR, 'bug_to_user_story_v1.yml')
V2_PATH = os.path.join(PROMPTS_DIR, 'bug_to_user_story_v2.yml')


# === Fixtures ===

@pytest.fixture
def v2_prompt():
    """Carrega e retorna o prompt V2."""
    return load_prompt(V2_PATH)

@pytest.fixture
def v2_template(v2_prompt):
    """Retorna o template (texto) do prompt V2."""
    return v2_prompt.template


# === 0. Testes de Carregamento ===

class TestPromptLoading:
    """Verifica que os arquivos de prompt existem e carregam corretamente."""

    def test_v1_file_exists(self):
        assert os.path.exists(V1_PATH), "Arquivo V1 não encontrado."

    def test_v2_file_exists(self):
        assert os.path.exists(V2_PATH), "Arquivo V2 não encontrado."

    def test_v2_loads_successfully(self, v2_prompt):
        assert v2_prompt is not None

    def test_v2_has_bug_report_input(self, v2_prompt):
        assert "bug_report" in v2_prompt.input_variables, \
            "O prompt deve aceitar 'bug_report' como variável de entrada."


# === 1. Existência de System Prompt ===

class TestSystemPrompt:
    """Verifica que o prompt contém instruções de sistema (System Prompt)."""

    def test_has_system_instructions(self, v2_template):
        """O prompt deve conter instruções claras de comportamento para o LLM."""
        # Verificar presença de seções de instrução
        assert "INSTRUÇÕES" in v2_template.upper() or "FORMATO" in v2_template.upper(), \
            "O prompt deve conter seções de instrução (System Prompt)."

    def test_has_task_definition(self, v2_template):
        """O prompt deve definir claramente a tarefa."""
        assert "TAREFA" in v2_template.upper() or "Converta" in v2_template, \
            "O prompt deve conter uma definição de tarefa."

    def test_template_is_not_trivial(self, v2_template):
        """O prompt otimizado deve ser substancialmente maior que um prompt trivial."""
        assert len(v2_template) > 500, \
            f"O prompt parece muito curto ({len(v2_template)} chars). Esperado > 500."


# === 2. Definição de Persona (Role) ===

class TestPersonaDefinition:
    """Verifica que o prompt define uma persona/role clara para o LLM."""

    def test_has_persona(self, v2_template):
        """O prompt deve definir quem o LLM é (ex: Product Owner, Analista)."""
        persona_keywords = ["Product Owner", "Analista", "Você é um", "Você é uma"]
        has_persona = any(kw in v2_template for kw in persona_keywords)
        assert has_persona, \
            "O prompt deve definir uma persona (Role) para o LLM."

    def test_persona_has_experience(self, v2_template):
        """A persona deve incluir contexto de experiência."""
        experience_keywords = ["experiência", "especialidade", "sênior", "senior"]
        has_experience = any(kw.lower() in v2_template.lower() for kw in experience_keywords)
        assert has_experience, \
            "A persona deve incluir contexto de experiência profissional."


# === 3. Exigência de Formato (Markdown / User Story) ===

class TestFormatRequirement:
    """Verifica que o prompt exige um formato estruturado de saída."""

    def test_requires_user_story_format(self, v2_template):
        """O prompt deve exigir o formato 'Como/Eu quero/Para que'."""
        assert "Como" in v2_template and "quero" in v2_template and "Para que" in v2_template, \
            "O prompt deve exigir o formato padrão de User Story (Como/Eu quero/Para que)."

    def test_requires_acceptance_criteria(self, v2_template):
        """O prompt deve exigir Critérios de Aceite."""
        assert "Critérios de Aceite" in v2_template or "Acceptance Criteria" in v2_template, \
            "O prompt deve exigir Critérios de Aceite."

    def test_requires_gherkin_syntax(self, v2_template):
        """O prompt deve exigir a sintaxe Gherkin (Dado/Quando/Então)."""
        gherkin_keywords = ["Dado", "Quando", "Então"]
        has_gherkin = all(kw in v2_template for kw in gherkin_keywords)
        assert has_gherkin, \
            "O prompt deve exigir sintaxe Gherkin (Dado/Quando/Então)."

    def test_requires_markdown_structure(self, v2_template):
        """O prompt deve exigir formatação Markdown (títulos com #)."""
        assert "# " in v2_template or "## " in v2_template, \
            "O prompt deve exigir formatação Markdown."


# === 4. Presença de Few-Shot Examples ===

class TestFewShotExamples:
    """Verifica que o prompt contém exemplos few-shot."""

    def test_has_few_shot_section(self, v2_template):
        """O prompt deve conter uma seção explícita de exemplos."""
        assert "Exemplo" in v2_template or "Few-Shot" in v2_template, \
            "O prompt deve conter uma seção de exemplos (Few-Shot)."

    def test_has_example_bug_report(self, v2_template):
        """O exemplo deve incluir um Bug Report de entrada."""
        assert "Bug Report:" in v2_template, \
            "O exemplo few-shot deve incluir um Bug Report de entrada."

    def test_has_example_output(self, v2_template):
        """O exemplo deve incluir uma saída esperada."""
        assert "Saída:" in v2_template or "user_story>" in v2_template, \
            "O exemplo few-shot deve incluir uma saída esperada."


# === 5. Ausência de Termos [TODO] ===

class TestNoTodoTerms:
    """Verifica que o prompt não contém placeholders inacabados."""

    def test_no_todo_markers(self, v2_template):
        """O prompt não deve conter marcadores [TODO]."""
        assert "[TODO]" not in v2_template, \
            "O prompt não deve conter marcadores [TODO]."

    def test_no_fixme_markers(self, v2_template):
        """O prompt não deve conter marcadores [FIXME]."""
        assert "[FIXME]" not in v2_template, \
            "O prompt não deve conter marcadores [FIXME]."

    def test_no_placeholder_markers(self, v2_template):
        """O prompt não deve conter marcadores genéricos de placeholder."""
        assert "XXX" not in v2_template and "PLACEHOLDER" not in v2_template, \
            "O prompt não deve conter placeholders genéricos."


# === 6. Uso de pelo menos 2 Técnicas Avançadas ===

class TestAdvancedTechniques:
    """Verifica que o prompt utiliza pelo menos 2 técnicas avançadas de Prompt Engineering."""

    def test_uses_chain_of_thought(self, v2_template):
        """Técnica 1: Chain of Thought (CoT) - Raciocínio passo a passo."""
        cot_indicators = ["Chain of Thought", "passo a passo", "<thinking>", "etapas de raciocínio"]
        has_cot = any(indicator in v2_template for indicator in cot_indicators)
        assert has_cot, \
            "O prompt deve utilizar Chain of Thought (CoT)."

    def test_uses_few_shot(self, v2_template):
        """Técnica 2: Few-Shot Learning - Exemplos concretos."""
        assert "Exemplo" in v2_template, \
            "O prompt deve utilizar Few-Shot Learning (exemplos)."

    def test_uses_xml_isolation(self, v2_template):
        """Técnica 3: XML Isolation - Separação estruturada de raciocínio e saída."""
        assert "<thinking>" in v2_template and "<user_story>" in v2_template, \
            "O prompt deve utilizar XML Isolation (<thinking> e <user_story>)."

    def test_uses_persona(self, v2_template):
        """Técnica 4: Role Prompting - Persona especializada."""
        assert "Você é um" in v2_template or "Você é uma" in v2_template, \
            "O prompt deve utilizar Role Prompting (persona)."

    def test_minimum_two_techniques(self, v2_template):
        """Verifica que pelo menos 2 técnicas estão presentes simultaneamente."""
        techniques_found = 0

        # CoT
        if any(kw in v2_template for kw in ["Chain of Thought", "<thinking>", "passo a passo"]):
            techniques_found += 1

        # Few-Shot
        if "Exemplo" in v2_template:
            techniques_found += 1

        # XML Isolation
        if "<thinking>" in v2_template and "<user_story>" in v2_template:
            techniques_found += 1

        # Role Prompting
        if "Você é um" in v2_template:
            techniques_found += 1

        assert techniques_found >= 2, \
            f"O prompt deve usar pelo menos 2 técnicas avançadas. Encontradas: {techniques_found}."
