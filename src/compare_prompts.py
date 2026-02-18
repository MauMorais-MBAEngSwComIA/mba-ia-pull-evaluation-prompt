"""
Script para comparar resultados dos prompts:
- V1 (Baseline)
- V2.8 (Scalpel - Otimizado)
- V3 (User Provided)

Salva resultados em Markdown e JSON.
"""

import sys
import json
import argparse
from evaluate import run_evaluation_for_prompt
from dotenv import load_dotenv

load_dotenv()

def run_comparison(model_name: str = "gemini-2.0-flash"):
    prompts_to_compare = [
        ("Baseline (v1)", "bug_to_user_story_v1"),
        ("Final (v2 XML)", "bug_to_user_story_v2")
    ]
    
    results = {}
    
    print(f"🏁 Iniciando Comparação Geral com Modelo: {model_name} ...")
    
    for label, prompt_name in prompts_to_compare:
        print(f"\n➡️  Avaliando {label} [{prompt_name}]...")
        scores = run_evaluation_for_prompt(prompt_name, model_name=model_name)
        if scores:
            results[label] = scores
        else:
            print(f"⚠️  Sem resultados para {label}")

    if not results:
        print("❌ Nenhuma avaliação obteve sucesso.")
        return

    # Montar Tabela
    # Identificar todas as métricas presentes
    all_metrics = set()
    for res in results.values():
        all_metrics.update(res.keys())
    
    metrics = sorted(list(all_metrics))
    
    # Cabeçalho
    labels = [p[0] for p in prompts_to_compare if p[0] in results]
    header = f"| Métrica | {' | '.join(labels)} | Meta (>0.9) |"
    separator = f"|---|{'---|' * len(labels)}---|"
    
    match_rows = []
    
    for metric in metrics:
        row = f"| {metric} |"
        for label in labels:
            score = results[label].get(metric, 0.0)
            status = "✅" if score >= 0.9 else "❌"
            # Highlight best score
            row += f" {score:.4f} |"
        
        row += " 0.9 |"
        match_rows.append(row)

    # Calcular Médias
    avg_row = f"| **MÉDIA GERAL** |"
    for label in labels:
        scores = results[label].values()
        avg = sum(scores) / len(scores) if scores else 0
        avg_row += f" **{avg:.4f}** |"
    avg_row += " - |"

    md_content = f"# Relatório de Comparação de Prompts\n\n"
    md_content += f"{header}\n{separator}\n"
    md_content += "\n".join(match_rows)
    md_content += f"\n{avg_row}\n"
    
    # Análise Rápida
    md_content += "\n## 🏆 Análise Rápida\n"
    
    # Métricas alvo
    target_metrics = ["tone", "acceptance_criteria", "user_story_format", "completeness"]
    
    def check_success(metrics_dict):
        return all(metrics_dict.get(m, 0) >= 0.9 for m in target_metrics)
        
    v2_success = check_success(results.get("Final (v2 XML)", {}))
    
    if v2_success:
        md_content += "\n- **V2 (XML)**: APROVADO! Todos os critérios (Tone, AC, Format, Completeness) estão >= 0.9."
    else:
        md_content += "\n- **Atenção**: O prompt V2 não atingiu todas as metas. Verifique os detalhes."

    filename = f"comparison_report_{model_name.replace(':', '').replace('.', '-')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\n✅ Relatório salvo em {filename}")
    print(md_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gemini-2.0-flash")
    args = parser.parse_args()
    
    run_comparison(model_name=args.model)
