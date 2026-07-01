"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_KEY = "bug_to_user_story_v2"
PROMPT_FILE = Path("prompts/bug_to_user_story_v2.yml")


def get_prompt_data(yaml_data: dict) -> dict:
    """Extrai os dados do prompt do YAML local."""
    if PROMPT_KEY in yaml_data:
        return yaml_data[PROMPT_KEY]

    return yaml_data


def build_chat_prompt(prompt_data: dict) -> ChatPromptTemplate:
    """Cria um ChatPromptTemplate a partir da estrutura YAML."""
    messages = prompt_data.get("messages") or [
        {"role": "system", "template": prompt_data.get("system_prompt", "")},
        {"role": "user", "template": prompt_data.get("user_prompt", "{bug_report}")},
    ]

    prompt_messages = [
        (message["role"], message["template"])
        for message in messages
        if message.get("role") and message.get("template")
    ]

    prompt = ChatPromptTemplate.from_messages(prompt_messages)
    prompt.metadata = {
        "version": prompt_data.get("version"),
        "source": prompt_data.get("source"),
        "techniques_applied": prompt_data.get("techniques_applied", []),
        **prompt_data.get("metadata", {}),
    }
    prompt.tags = prompt_data.get("tags", [])

    return prompt


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
        repo_full_name = f"{username}/{prompt_name}"
        techniques = prompt_data.get("techniques_applied", [])
        tags = prompt_data.get("tags", [])
        description = prompt_data.get("description", "")

        if techniques:
            description = (
                f"{description}\n\n"
                f"Técnicas aplicadas: {', '.join(techniques)}."
            ).strip()

        prompt = build_chat_prompt(prompt_data)

        print(f"Publicando prompt: {repo_full_name}")
        prompt_url = hub.push(
            repo_full_name,
            prompt,
            api_url=os.getenv("LANGSMITH_ENDPOINT"),
            api_key=os.getenv("LANGSMITH_API_KEY"),
            new_repo_is_public=True,
            new_repo_description=description,
            tags=tags,
        )

        print(f"Prompt publicado com sucesso: {prompt_url}")
        print("O prompt foi enviado como público no LangSmith Hub.")
        return True
    except Exception as exc:
        print(f"Erro ao publicar o prompt '{prompt_name}': {exc}")
        print("Verifique as credenciais do LangSmith, o username do Hub e a conexão com a internet.")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    required_fields = [
        "description",
        "version",
        "input_variables",
        "system_prompt",
        "user_prompt",
        "messages",
        "techniques_applied",
        "tags",
    ]

    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: {field}")

    if not str(prompt_data.get("system_prompt", "")).strip():
        errors.append("system_prompt está vazio")

    if not str(prompt_data.get("user_prompt", "")).strip():
        errors.append("user_prompt está vazio")

    input_variables = prompt_data.get("input_variables", [])
    if "bug_report" not in input_variables:
        errors.append("input_variables deve conter bug_report")

    techniques = prompt_data.get("techniques_applied", [])
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("techniques_applied deve listar pelo menos 2 técnicas")

    messages = prompt_data.get("messages", [])
    roles = {message.get("role") for message in messages if isinstance(message, dict)}
    if "system" not in roles:
        errors.append("messages deve conter uma mensagem system")
    if "user" not in roles:
        errors.append("messages deve conter uma mensagem user")

    full_prompt_text = "\n".join(
        str(prompt_data.get(field, ""))
        for field in ["system_prompt", "user_prompt", "description"]
    )
    if re.search(r"\[(?:\s*)TODO(?:\s*)\]|\bTODO\b", full_prompt_text, re.IGNORECASE):
        errors.append("prompt contém TODO pendente")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DO PROMPT OTIMIZADO")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    yaml_data = load_yaml(str(PROMPT_FILE))
    if not yaml_data:
        return 1

    prompt_data = get_prompt_data(yaml_data)
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    print("Prompt validado com sucesso.")
    success = push_prompt_to_langsmith(PROMPT_KEY, prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
