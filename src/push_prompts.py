"""
Script para enviar o prompt otimizado para o LangSmith Hub.
Requer LANGCHAIN_API_KEY configurada.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import load_prompt

load_dotenv()

def push_prompt():
    prompt_path = "prompts/bug_to_user_story_v2.yml"
    repo_handle = "bug-to-user-story-optimized" # Nome do repo no Hub
    
    if not os.path.exists(prompt_path):
        print(f"❌ Arquivo não encontrado: {prompt_path}")
        return

    print(f"📦 Carregando prompt de {prompt_path}...")
    try:
        prompt = load_prompt(prompt_path)
        
        print(f"🚀 Enviando para LangSmith Hub: {repo_handle}...")
        # Nota: Isso requer que a chave LANGCHAIN_API_KEY tenha permissão de escrita
        # e que o usuário esteja autenticado ou o repo seja público/privado corretamente.
        url = hub.push(repo_handle, prompt)
        
        print(f"✅ Prompt enviado com sucesso!")
        print(f"🔗 URL: {url}")
        
    except Exception as e:
        print(f"❌ Erro ao enviar prompt: {e}")

if __name__ == "__main__":
    push_prompt()
