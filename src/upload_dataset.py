"""
Script para fazer upload/sync do dataset local (JSONL) para o LangSmith.

Lê o arquivo datasets/bug_to_user_story.jsonl e sincroniza com o dataset
no LangSmith, adicionando apenas os exemplos que ainda não existem.
"""

import json
import os
import sys
import argparse
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()


def upload_dataset(
    jsonl_path: str = "datasets/bug_to_user_story.jsonl",
    dataset_name: str = "prompt-optimization-challenge-resolved-eval",
    force_recreate: bool = False
):
    """
    Sincroniza o dataset local com o LangSmith.
    
    Args:
        jsonl_path: Caminho do arquivo JSONL local
        dataset_name: Nome do dataset no LangSmith
        force_recreate: Se True, deleta e recria o dataset inteiro
    """
    # 1. Verificar chave
    if not os.getenv("LANGSMITH_API_KEY"):
        print("❌ LANGSMITH_API_KEY não configurada no .env")
        return

    # 2. Carregar dados locais
    if not os.path.exists(jsonl_path):
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
        return

    examples = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                examples.append(data)
            except json.JSONDecodeError as e:
                print(f"⚠️  Erro na linha {i}: {e}")
                continue

    print(f"📄 {len(examples)} exemplos carregados de {jsonl_path}")

    # 3. Conectar ao LangSmith
    client = Client()

    # 4. Verificar se dataset existe
    existing_dataset = None
    try:
        existing_dataset = client.read_dataset(dataset_name=dataset_name)
        print(f"📊 Dataset encontrado: '{dataset_name}' (ID: {existing_dataset.id})")
    except Exception:
        print(f"📊 Dataset '{dataset_name}' não encontrado. Será criado.")

    # 5. Se force_recreate, deletar e recriar
    if force_recreate and existing_dataset:
        print(f"🗑️  Deletando dataset existente...")
        client.delete_dataset(dataset_id=existing_dataset.id)
        existing_dataset = None
        print(f"✅ Dataset deletado.")

    # 6. Criar dataset se não existe
    if not existing_dataset:
        existing_dataset = client.create_dataset(
            dataset_name=dataset_name,
            description="Dataset de avaliação para Bug to User Story - 22 exemplos variados"
        )
        print(f"✅ Dataset criado: '{dataset_name}' (ID: {existing_dataset.id})")

    # 7. Verificar exemplos existentes
    existing_examples = list(client.list_examples(dataset_id=existing_dataset.id))
    existing_bugs = set()
    for ex in existing_examples:
        bug = ex.inputs.get("bug_report", "")
        existing_bugs.add(bug[:80])  # Usar primeiros 80 chars como chave

    print(f"📋 Exemplos já no LangSmith: {len(existing_examples)}")

    # 8. Upload apenas novos exemplos
    new_count = 0
    for example in examples:
        bug_report = example["inputs"]["bug_report"]
        
        # Verificar se já existe (pelos primeiros 80 chars)
        if bug_report[:80] in existing_bugs:
            continue

        # Upload
        # O campo se chama 'reference' no JSONL mas o LangSmith espera 'user_story'
        outputs = example["outputs"]
        # Normalizar: aceitar tanto 'reference' quanto 'user_story'
        if "reference" in outputs and "user_story" not in outputs:
            outputs["user_story"] = outputs.pop("reference")

        client.create_example(
            inputs=example["inputs"],
            outputs=outputs,
            dataset_id=existing_dataset.id
        )
        new_count += 1
        print(f"  ✅ Adicionado: {bug_report[:60]}...")

    # 9. Resumo
    print(f"\n{'='*50}")
    print(f"📊 Resumo:")
    print(f"   Já existiam: {len(existing_examples)}")
    print(f"   Novos adicionados: {new_count}")
    print(f"   Total agora: {len(existing_examples) + new_count}")
    print(f"{'='*50}")

    if new_count == 0:
        print("ℹ️  Nenhum novo exemplo para adicionar. Dataset já está sincronizado!")
    else:
        print(f"✅ Dataset '{dataset_name}' atualizado com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload dataset para LangSmith")
    parser.add_argument("--force", action="store_true", help="Deletar e recriar dataset")
    parser.add_argument("--dataset", type=str, default="prompt-optimization-challenge-resolved-eval")
    args = parser.parse_args()

    upload_dataset(force_recreate=args.force, dataset_name=args.dataset)
