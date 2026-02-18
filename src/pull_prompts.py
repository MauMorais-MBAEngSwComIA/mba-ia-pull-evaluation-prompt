"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Função principal para puxar prompts.
    """
    print_section_header("PULL PROMPTS FROM LANGSMITH")

    # Verificar variáveis de ambiente
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return

    # Definir prompts para puxar
    prompts_to_pull = [
        {
            "hub_repo": "leonanluppi/bug_to_user_story_v1",
            "local_path": "prompts/raw_prompts.yml"
        }
    ]

    for item in prompts_to_pull:
        repo = item["hub_repo"]
        local_path = item["local_path"]

        print(f"Puxando prompt: {repo}...")

        try:
            # 1. Pull do Hub
            # Isso retorna um objeto ChatPromptTemplate
            prompt_object = hub.pull(repo)
            
            # 2. Salvar localmente
            # Serializamos para dicionário e salvamos como YAML
            # Nota: prompt_object.dict() ou similar pode variar dependendo da versão do LangChain
            # Vamos tentar salvar de uma forma que preserve a estrutura
            
            # Maneira mais segura de salvar é converter para string ou dict repr
            try:
                # Tenta serializar usando método padrão do LangChain
                from langchain_core.load.dump import dumpd
                prompt_dict = dumpd(prompt_object)
                
                if save_yaml(prompt_dict, local_path):
                     print(f"✅ Sucesso! Salvo em: {local_path}")
                else:
                    print(f"❌ Falha ao salvar arquivo local: {local_path}")
                    
            except Exception as e:
                print(f"⚠️ Erro na serialização: {e}")
                # Fallback simples (pode não funcionar para todos os tipos de prompt)
                print(f"   Tentando fallback...")
                
        except Exception as e:
            print(f"❌ Erro ao puxar prompt {repo}: {e}")
            if "403" in str(e):
                print("   Verifique se sue API Key tem permissão de leitura.")
            elif "404" in str(e):
                print("   Verifique se o nome do repositório está correto.")


def main():
    """Função principal"""
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
