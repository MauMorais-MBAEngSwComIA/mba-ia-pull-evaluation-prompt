"""
Script de avaliação usando LangSmith SDK (langsmith.evaluation).
Permite visualização de "Experiments" na plataforma.
Suporta --evaluator-model para separar modelo gerador do avaliador.
"""

import os
import argparse
import re
from typing import Any, Dict
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import load_prompt

# preciso de um wrapper para o SDK.
from langsmith import Client
from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate

from metrics import (
    evaluate_tone_score,
    evaluate_acceptance_criteria_score,
    evaluate_user_story_format_score,
    evaluate_completeness_score,
    evaluate_clarity,
    evaluate_precision,
    evaluate_f1_score
)
from utils import get_llm

load_dotenv()

from langsmith.evaluation import RunEvaluator, EvaluationResult

class GlobalEvaluator(RunEvaluator):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model_name = model_name

    def evaluate_run(self, run: Run, example: Example = None) -> Dict[str, Any]:
        bug_report = example.inputs.get("bug_report")
        reference_story = example.outputs.get("user_story") or example.outputs.get("reference")
        generated_story = run.outputs.get("output")

        # Smart Parsing: Remove Chain of Thought (Reasoning)
        # Se o prompt gera raciocínio, ele vem antes do título da User Story (# Título)
        # Vamos ignorar tudo antes do primeiro Markdown Header '# '
        if generated_story:
            # 1. Tentar extrair via XML (V5)
            if "<user_story>" in generated_story:
                match = re.search(r'<user_story>(.*?)</user_story>', generated_story, re.DOTALL)
                if match:
                    generated_story = match.group(1).strip()

            # 2. Fallback: Ignorar texto antes do primeiro título markdown (# ou ##)
            else:
                 # Encontra índices
                 h1_idx = generated_story.find("# ")
                 h2_idx = generated_story.find("## ")

                 # Pega o menor índice positivo
                 idxs = [i for i in [h1_idx, h2_idx] if i >= 0]

                 if idxs:
                     start_idx = min(idxs)
                     generated_story = generated_story[start_idx:].strip()
                 else:
                     print(f"DEBUG: Strip FAILED. No header found. Starts with: {generated_story[:30]}...")

        # DEBUG: Verificar o que está sendo avaliado
        print(f"DEBUG: Cleaned Story Start: {generated_story[:50]}...")

        if not generated_story:
            return EvaluationResult(key="error", score=0, comment="No output")

        eval_results = []

        # Lista de funções métricas
        metric_funcs = [
            ("tone", evaluate_tone_score),
            ("acceptance_criteria", evaluate_acceptance_criteria_score),
            ("user_story_format", evaluate_user_story_format_score),
            ("completeness", evaluate_completeness_score),
            ("f1_score", evaluate_f1_score)
        ]

        for name, func in metric_funcs:
            try:
                # Passar o modelo configurado para a função de métrica
                res = func(bug_report, generated_story, reference_story, model=self.model_name)
                score = res.get("score")
                print(f"      [Metric] {name}: {score}")

                eval_results.append(
                    EvaluationResult(
                        key=name,
                        score=score,
                        comment=res.get("reasoning")
                    )
                )
            except Exception as e:
                print(f"      [Error] Metric {name}: {e}")
                eval_results.append(EvaluationResult(key=name, score=0.0, comment=str(e)))

        return {"results": eval_results}


def run_evaluation_for_prompt(prompt_name: str, dataset_name: str = "prompt-optimization-challenge-resolved-eval", model_name: str = "gemini-2.0-flash", evaluator_model: str = None) -> Dict[str, float]:
    judge_model = evaluator_model if evaluator_model else model_name
    print(f"🚀 Iniciando Avaliação via SDK (LangSmith): {prompt_name} | Gen: {model_name} | Eval: {judge_model}")

    # 1. Carregar Prompt (forçar UTF-8 no Windows)
    try:
        import io, tempfile
        src_path = f"prompts/{prompt_name}.yml"
        with io.open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False,
                                         encoding="utf-8") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        prompt = load_prompt(tmp_path)
        os.unlink(tmp_path)
    except Exception as e:
        print(f"Erro ao carregar prompt: {e}")
        return {}

    # 2. Configurar LLM (Target - Gerador)
    try:
        llm = get_llm(model=model_name, temperature=0.0)
    except Exception as e:
        print(f"Erro ao configurar LLM: {e}")
        return {}

    # 3. Definir o Target (Chain ou Função)
    def target_func(inputs: dict) -> dict:
        chain = prompt | llm
        res = chain.invoke(inputs)
        return {"output": res.content}

    # 4. Configurar LangSmith Client
    client = Client()

    # 5. Configurar Avaliador (Judge — pode ser modelo diferente do gerador)
    custom_evaluator = GlobalEvaluator(model_name=judge_model)

    # 6. Executar Avaliação
    safe_model = model_name.replace(".", "-").replace(":", "")
    experiment_prefix = f"{prompt_name}-eval-{safe_model}"

    try:
        results = evaluate(
            target_func,
            data=dataset_name,
            evaluators=[custom_evaluator],
            experiment_prefix=experiment_prefix,
            max_concurrency=4
        )

        # Iterar manualmente para recuperar feedback
        metrics_accum = {}

        iterable_results = []
        if hasattr(results, '_results'):
             vals = results._results
             if isinstance(vals, dict):
                 iterable_results = vals.values()
             else:
                 iterable_results = vals
        elif hasattr(results, 'results'):
             iterable_results = results.results

        for res in iterable_results:
            feedbacks = []

            if isinstance(res, dict):
                feedbacks = res.get('feedback') or res.get('evaluation_results', {}).get('results')
            else:
                 if hasattr(res, 'feedback'):
                    feedbacks = res.feedback
                 elif hasattr(res, 'evaluation_results'):
                    feedbacks = res.evaluation_results

            if feedbacks:
                if isinstance(feedbacks, list):
                    for f in feedbacks:
                        key = getattr(f, 'key', None) or (f.get('key') if isinstance(f, dict) else None)
                        score = getattr(f, 'score', None) or (f.get('score') if isinstance(f, dict) else None)

                        if key and score is not None:
                            if key not in metrics_accum:
                                metrics_accum[key] = []
                            metrics_accum[key].append(score)

        final_metrics = {}
        if not metrics_accum:
             print("⚠️ Nenhuma métrica de feedback encontrada nos resultados.")
             return {}

        print("\n📊 Resumo da Avaliação:")
        for metric_name, scores in metrics_accum.items():
            if scores:
                avg = sum(scores) / len(scores)
                final_metrics[metric_name] = avg
                status = "✅" if avg >= 0.9 else "❌"
                print(f"  - {metric_name:<20}: {avg:.4f} {status}")
            else:
                final_metrics[metric_name] = 0.0
                print(f"  - {metric_name:<20}: N/A")

        print("\n🔗 Veja os resultados detalhados no LangSmith UI.")
        return final_metrics

    except Exception as e:
        print(f"\n❌ Erro fatal na execução da avaliação: {e}")
        import traceback
        traceback.print_exc()
        return {}

def main():
    parser = argparse.ArgumentParser(description="Rodar avaliação de prompt no LangSmith")
    parser.add_argument("--prompt", type=str, default="bug_to_user_story_v2", help="Nome do prompt (sem .yml)")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash", help="Modelo LLM gerador (Target)")
    parser.add_argument("--evaluator-model", type=str, default=None, help="Modelo LLM avaliador (Judge). Se omitido, usa o mesmo do --model.")
    args = parser.parse_args()

    run_evaluation_for_prompt(args.prompt, model_name=args.model, evaluator_model=args.evaluator_model)

if __name__ == "__main__":
    main()
