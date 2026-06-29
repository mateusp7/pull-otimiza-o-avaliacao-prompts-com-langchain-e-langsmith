"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serializacao nativa do LangChain para extrair prompts.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_FILE = Path("prompts/bug_to_user_story_v1.yml")


def _get_message_template(message) -> str:
    """Extrai o texto de um template de mensagem do LangChain."""
    prompt = getattr(message, "prompt", None)
    if prompt is not None and hasattr(prompt, "template"):
        return prompt.template

    if hasattr(message, "template"):
        return message.template

    return str(message)


def _get_message_role(message) -> str:
    """Normaliza o tipo da mensagem para os campos usados no YAML."""
    class_name = message.__class__.__name__.lower()

    if "system" in class_name:
        return "system"
    if "human" in class_name or "user" in class_name:
        return "user"
    if "ai" in class_name or "assistant" in class_name:
        return "assistant"

    return "unknown"


def serialize_prompt(prompt) -> dict:
    """
    Converte o prompt retornado pelo LangSmith Hub para um dicionario YAML.

    O arquivo local usa uma estrutura simples para facilitar a analise e a
    criacao da versao otimizada nas proximas tarefas.
    """
    prompt_data = {
        "description": "Prompt inicial para converter relatos de bugs em User Stories",
        "source": PROMPT_NAME,
        "version": "v1",
        "input_variables": list(getattr(prompt, "input_variables", [])),
    }

    messages = getattr(prompt, "messages", None)
    if messages:
        extracted_messages = []

        for message in messages:
            role = _get_message_role(message)
            template = _get_message_template(message)
            extracted_messages.append({"role": role, "template": template})

            if role == "system" and "system_prompt" not in prompt_data:
                prompt_data["system_prompt"] = template
            elif role == "user" and "user_prompt" not in prompt_data:
                prompt_data["user_prompt"] = template

        prompt_data["messages"] = extracted_messages
    elif hasattr(prompt, "template"):
        prompt_data["system_prompt"] = prompt.template
        prompt_data["user_prompt"] = "{bug_report}"
    else:
        prompt_data["system_prompt"] = str(prompt)
        prompt_data["user_prompt"] = "{bug_report}"

    prompt_data.setdefault("system_prompt", "")
    prompt_data.setdefault("user_prompt", "{bug_report}")

    return {"bug_to_user_story_v1": prompt_data}


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt inicial no LangSmith Hub e salva em YAML local.

    Returns:
        True se o pull e a gravacao local forem concluidos com sucesso.
    """
    print_section_header("PULL DO PROMPT INICIAL")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    try:
        Client()
        print("Conexao com LangSmith configurada.")

        print(f"Puxando prompt: {PROMPT_NAME}")
        prompt = hub.pull(PROMPT_NAME)

        prompt_yaml = serialize_prompt(prompt)

        print(f"Salvando prompt em: {OUTPUT_FILE}")
        if not save_yaml(prompt_yaml, str(OUTPUT_FILE)):
            return False

        print("Prompt salvo com sucesso.")
        return True
    except Exception as exc:
        print(f"Erro ao fazer pull do prompt '{PROMPT_NAME}': {exc}")
        print("Verifique as credenciais do LangSmith, o acesso ao Prompt Hub e a conexao com a internet.")
        return False


def main():
    """Função principal."""
    success = pull_prompts_from_langsmith()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
