"""
Funções auxiliares para o projeto de otimização de prompts.
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def load_yaml(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Carrega arquivo YAML.

    Args:
        file_path: Caminho do arquivo YAML

    Returns:
        Dicionário com conteúdo do YAML ou None se erro
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Erro ao parsear YAML: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return None


def save_yaml(data: Dict[str, Any], file_path: str) -> bool:
    """
    Salva dados em arquivo YAML.

    Args:
        data: Dados para salvar
        file_path: Caminho do arquivo de saída

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        output_file = Path(file_path)
        # Garantir que o diretório pai exista
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2)

        return True
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return False


def check_env_vars(required_vars: list) -> bool:
    """
    Verifica se variáveis de ambiente obrigatórias estão configuradas.

    Args:
        required_vars: Lista de variáveis obrigatórias

    Returns:
        True se todas configuradas, False caso contrário
    """
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Variáveis de ambiente faltando:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nConfigure-as no arquivo .env antes de continuar.")
        return False

    return True


def format_score(score: float, threshold: float = 0.9) -> str:
    """
    Formata score com indicador visual de aprovação.

    Args:
        score: Score entre 0.0 e 1.0
        threshold: Limite mínimo para aprovação

    Returns:
        String formatada com score e símbolo
    """
    symbol = "✓" if score >= threshold else "✗"
    return f"{score:.2f} {symbol}"


def print_section_header(title: str, char: str = "=", width: int = 50):
    """
    Imprime cabeçalho de seção formatado.

    Args:
        title: Título da seção
        char: Caractere para a linha
        width: Largura da linha
    """
    print("\n" + char * width)
    print(title)
    print(char * width + "\n")


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Extrai JSON de uma resposta de LLM que pode conter texto adicional.

    Args:
        response_text: Texto da resposta do LLM

    Returns:
        Dicionário extraído ou None se não encontrar JSON válido
    """
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Tentar encontrar JSON no meio do texto
        # Procura pelo primeiro '{' e pelo último '}'
        start = response_text.find('{')
        end = response_text.rfind('}') + 1

        if start != -1 and end > start:
            try:
                json_str = response_text[start:end]
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
                
        # Tentar consertar JSONs mal formatados comuns (ex: markdown code blocks)
        if "```json" in response_text:
            try:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except:
                pass

    return None


def get_llm(model: Optional[str] = None, temperature: float = 0.0):
    """
    Retorna uma instância de LLM configurada baseada no provider.
    Prioriza configuração do .env ou defaults do Google GenAI.
    Retorna uma instância de LLM com fallback automático de providers.
    Ordem de preferência:
    1. Google (GEMINI_API_KEY ou GOOGLE_API_KEY)
    2. OpenAI (OPENAI_API_KEY)
    """
    # 1. Tentar Google Gemini primeiro (Preferência do User)
    google_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    # Se o usuário forçou um provider via env, respeitar (mas cair no fallback se falhar setup?)
    # A regra do usuário foi: "Se a chave da Google estiver configurada, ela é a default."
    
    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            default_model = 'gemini-2.0-flash'
            model_name = model or os.getenv('LLM_MODEL', default_model)
            
            # Ajuste para garantir que não estamos usando modelo OpenAI com Google
            if "gpt" in model_name:
                model_name = default_model

            print(f"🤖 Usando Provider: Google | Modelo: {model_name}")
            return ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                google_api_key=google_key
            )
        except ImportError:
            print("⚠️  Biblioteca langchain-google-genai não encontrada.")
            pass # Tentar OpenAI

    # 2. Se não tem Google ou falhou, tentar OpenAI
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            default_model = 'gpt-4o'
            model_name = model or os.getenv('LLM_MODEL', default_model)

            # Ajuste para garantir que não estamos usando modelo Gemini com OpenAI
            if "gemini" in model_name:
                model_name = default_model

            print(f"🤖 Usando Provider: OpenAI | Modelo: {model_name}")
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=openai_key
            )
        except ImportError:
            print("⚠️  Biblioteca langchain-openai não encontrada.")
            pass

    # 3. Se chegou aqui, não tem chaves configuradas
    raise ValueError(
        "❌ Nenhuma chave de API encontrada!\n"
        "Configure no .env uma das opções:\n"
        "   - GOOGLE_API_KEY (Recomendado: gemini-2.0-flash)\n"
        "   - OPENAI_API_KEY (Fallback: gpt-4o)"
    )


def get_eval_llm(model: Optional[str] = None, temperature: float = 0.0):
    """
    Retorna LLM auto-configurado para avaliação.
    """
    # Para avaliação, geralmente queremos modelos mais robustos.
    # Se estivermos no Google -> gemini-2.0-flash (ou o solicitado)
    # Se OpenAI -> gpt-4o
    return get_llm(model=model, temperature=temperature)
