"""
Testes automatizados para validação de prompts.
"""
from pathlib import Path
from typing import Any, Dict, Iterator, Union

import pytest
import yaml

from src.utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompts(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def prompt_data() -> Dict[str, Any]:
    prompts = load_prompts(PROMPT_FILE)
    assert PROMPT_KEY in prompts, f"Prompt '{PROMPT_KEY}' não encontrado em {PROMPT_FILE}"
    return prompts[PROMPT_KEY]


def prompt_text(prompt_data: Dict[str, Any]) -> str:
    return "\n".join(
        str(prompt_data.get(field, ""))
        for field in ("description", "system_prompt", "user_prompt")
    )


def flatten_values(value: Any) -> Iterator[str]:
    if isinstance(value, dict):
        for item in value.values():
            yield from flatten_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from flatten_values(item)
    else:
        yield str(value)


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data: Dict[str, Any]) -> None:
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        is_valid, errors = validate_prompt_structure(prompt_data)

        assert "system_prompt" in prompt_data
        assert prompt_data["system_prompt"].strip()
        assert is_valid, errors

    def test_prompt_has_role_definition(self, prompt_data: Dict[str, Any]) -> None:
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data["system_prompt"].lower()
        role_terms = [
            "voce e",
            "você é",
            "product manager",
            "persona",
            "senior",
        ]

        assert any(term in system_prompt for term in role_terms)
        assert "product manager" in system_prompt

    def test_prompt_mentions_format(self, prompt_data: Dict[str, Any]) -> None:
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = prompt_text(prompt_data).lower()

        assert "markdown" in text
        assert "como um" in text
        assert "eu quero" in text
        assert "para que" in text

    def test_prompt_has_few_shot_examples(self, prompt_data: Dict[str, Any]) -> None:
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        text = prompt_text(prompt_data).lower()
        techniques = [
            technique.lower()
            for technique in prompt_data.get("techniques_applied", [])
        ]

        assert "few-shot learning" in techniques
        assert text.count("exemplo") >= 2
        assert "entrada:" in text
        assert "saida:" in text or "saída:" in text

    def test_prompt_no_todos(self, prompt_data: Dict[str, Any]) -> None:
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        all_text = "\n".join(flatten_values(prompt_data)).lower()

        assert "[todo]" not in all_text
        assert "todo:" not in all_text

    def test_minimum_techniques(self, prompt_data: Dict[str, Any]) -> None:
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])

        assert isinstance(techniques, list)
        assert len(techniques) >= 2
        assert all(str(technique).strip() for technique in techniques)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
