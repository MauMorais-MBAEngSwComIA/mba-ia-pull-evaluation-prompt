"""
Conftest.py — Geração automática de test_report.md após execução do pytest.

Sempre que `pytest tests/` for executado, um relatório Markdown será gerado
na raiz do projeto com o resultado de todos os testes agrupados por critério.
"""

import os
import pytest
from datetime import datetime


# Armazena resultados dos testes
class TestReportData:
    results = []
    session_start = None
    session_end = None


def pytest_sessionstart(session):
    TestReportData.results = []
    TestReportData.session_start = datetime.now()


def pytest_runtest_logreport(report):
    """Captura o resultado de cada teste na fase 'call'."""
    if report.when == "call":
        # Extrair classe e nome do teste
        node_parts = report.nodeid.split("::")
        class_name = node_parts[1] if len(node_parts) > 2 else "General"
        test_name = node_parts[-1]
        
        TestReportData.results.append({
            "class": class_name,
            "test": test_name,
            "outcome": report.outcome,  # "passed", "failed", "skipped"
            "duration": report.duration,
            "message": str(report.longrepr) if report.failed else "",
        })


def pytest_sessionfinish(session, exitstatus):
    """Gera o test_report.md ao final da sessão."""
    TestReportData.session_end = datetime.now()
    
    results = TestReportData.results
    if not results:
        return

    total = len(results)
    passed = sum(1 for r in results if r["outcome"] == "passed")
    failed = sum(1 for r in results if r["outcome"] == "failed")
    skipped = sum(1 for r in results if r["outcome"] == "skipped")
    duration = (TestReportData.session_end - TestReportData.session_start).total_seconds()

    # Mapeamento de classes para critérios do desafio
    criteria_map = {
        "TestPromptLoading": ("0", "Carregamento do Prompt"),
        "TestSystemPrompt": ("1", "Existência de System Prompt"),
        "TestPersonaDefinition": ("2", "Definição de Persona (Role)"),
        "TestFormatRequirement": ("3", "Exigência de Formato (Markdown/User Story)"),
        "TestFewShotExamples": ("4", "Presença de Few-Shot Examples"),
        "TestNoTodoTerms": ("5", "Ausência de Termos [TODO]"),
        "TestAdvancedTechniques": ("6", "Uso de ≥ 2 Técnicas Avançadas"),
    }

    # Status geral
    status_emoji = "✅ APROVADO" if failed == 0 else "❌ REPROVADO"

    # Gerar Markdown
    lines = []
    lines.append("# Relatório de Testes — Prompt Validation")
    lines.append("")
    lines.append(f"**Data**: {TestReportData.session_end.strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"**Duração**: {duration:.2f}s")
    lines.append(f"**Status**: {status_emoji}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Resumo")
    lines.append("")
    lines.append(f"| Total | ✅ Passed | ❌ Failed | ⏭️ Skipped |")
    lines.append(f"|-------|----------|----------|-----------|")
    lines.append(f"| {total} | {passed} | {failed} | {skipped} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Resultados por Critério")
    lines.append("")

    # Agrupar resultados por classe
    from collections import OrderedDict
    grouped = OrderedDict()
    for r in results:
        cls = r["class"]
        if cls not in grouped:
            grouped[cls] = []
        grouped[cls].append(r)

    for cls, tests in grouped.items():
        criteria_id, criteria_name = criteria_map.get(cls, ("?", cls))
        cls_passed = all(t["outcome"] == "passed" for t in tests)
        cls_emoji = "✅" if cls_passed else "❌"

        lines.append(f"### {cls_emoji} Critério {criteria_id}: {criteria_name}")
        lines.append("")
        lines.append(f"| Teste | Status | Tempo |")
        lines.append(f"|-------|--------|-------|")

        for t in tests:
            test_label = t["test"].replace("test_", "").replace("_", " ").title()
            status = "✅ Pass" if t["outcome"] == "passed" else "❌ Fail" if t["outcome"] == "failed" else "⏭️ Skip"
            lines.append(f"| {test_label} | {status} | {t['duration']:.3f}s |")
        
        lines.append("")

        # Se houve falha, mostrar detalhes
        for t in tests:
            if t["outcome"] == "failed" and t["message"]:
                lines.append(f"> **Falha em `{t['test']}`:**")
                lines.append(f"> ```")
                # Limitar mensagem a 5 linhas
                msg_lines = t["message"].split("\n")[:5]
                for ml in msg_lines:
                    lines.append(f"> {ml}")
                lines.append(f"> ```")
                lines.append("")

    lines.append("---")
    lines.append(f"*Gerado automaticamente por `pytest` em {TestReportData.session_end.strftime('%d/%m/%Y %H:%M:%S')}.*")
    lines.append("")

    # Salvar na raiz do projeto
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(project_root, "test_report.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
