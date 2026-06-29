# Documentacao das etpaas

## Pull do Prompt inicial do LangSmith

### O que foi feito
Foi implementado o fluxo de pull do prompt inicial no LangSmith Prompt Hub. O script valida a credencial do LangSmith, conecta no LangSmith, busca o prompt `leonanluppi/bug_to_user_story_v1`, converte o objeto retornado pelo LangChain para uma estrutura YAML simples e salva o resultado em `prompts/bug_to_user_story_v1.yml`.

### Aonde foi feito
A implementacao foi feita no script `src/pull_prompts.py`, usando `langchain.hub.pull`, `langsmith.Client` e os helpers existentes em `src/utils.py`.

### Arquivo(s) modificado(s)
- `src/pull_prompts.py`
- `prompts/bug_to_user_story_v1.yml`
- `tasks.md`
- `step-by-step.md`

### Fluxo logico para alcancar o sucesso da tarefa
1. Leitura da documentação do LangSmith para buscar prompts no Hub.
2. Analisar o esqueleto de `src/pull_prompts.py` e os helpers disponiveis em `src/utils.py`.
3. Implementar validacao de `LANGSMITH_API_KEY` antes de acessar o LangSmith.
4. Instanciar `Client()` para confirmar a configuracao do LangSmith.
5. Executar `hub.pull("leonanluppi/bug_to_user_story_v1")` para obter o prompt inicial.
6. Extrair `system_prompt`, `user_prompt`, `input_variables` e mensagens do prompt retornado.
7. Salvar o YAML em `prompts/bug_to_user_story_v1.yml`.
8. Executar `.\.venv\Scripts\python.exe -B src\pull_prompts.py` para validar o fluxo completo.

---