1. Preparar o ambiente e as credenciais
   1.1 [X] Criar e ativar um ambiente virtual Python 3.9+
   1.2 [X] Instalar as dependencias do projeto com `pip install -r requirements.txt`
   1.3 [X] Configurar o arquivo `.env` a partir do `.env.example`
   1.4 [X] Informar as credenciais necessarias do LangSmith
   1.5 [X] Informar a API key do provedor de LLM escolhido, OpenAI ou Gemini

2. Implementar o pull do prompt inicial
   2.1 [ ] Analisar o esqueleto existente em `src/pull_prompts.py`
   2.2 [ ] Conectar ao LangSmith usando as credenciais configuradas
   2.3 [ ] Fazer pull do prompt `leonanluppi/bug_to_user_story_v1`
   2.4 [ ] Salvar o prompt localmente em `prompts/bug_to_user_story_v1.yml`
   2.5 [ ] Executar `python src/pull_prompts.py` para validar o fluxo de pull

3. Analisar o prompt original
   3.1 [ ] Ler o arquivo `prompts/bug_to_user_story_v1.yml`
   3.2 [ ] Identificar problemas de clareza, precisao, formato e comportamento esperado
   3.3 [ ] Mapear quais metricas podem ser impactadas pelos problemas encontrados
   3.4 [ ] Definir os criterios que o prompt otimizado deve atender

4. Criar o prompt otimizado
   4.1 [ ] Criar o arquivo `prompts/bug_to_user_story_v2.yml`
   4.2 [ ] Definir corretamente mensagens de System Prompt e User Prompt
   4.3 [ ] Incluir uma persona clara para o modelo
   4.4 [ ] Escrever instrucoes especificas para transformar bugs em user stories
   4.5 [ ] Definir regras explicitas de comportamento e formato de resposta
   4.6 [ ] Aplicar Few-shot Learning com exemplos claros de entrada e saida
   4.7 [ ] Aplicar pelo menos uma tecnica adicional, como Chain of Thought, Skeleton of Thought ou Role Prompting
   4.8 [ ] Incluir tratamento para edge cases
   4.9 [ ] Registrar metadados no YAML com as tecnicas utilizadas

5. Implementar os testes de validacao
   5.1 [ ] Analisar o esqueleto existente em `tests/test_prompts.py`
   5.2 [ ] Implementar `test_prompt_has_system_prompt`
   5.3 [ ] Implementar `test_prompt_has_role_definition`
   5.4 [ ] Implementar `test_prompt_mentions_format`
   5.5 [ ] Implementar `test_prompt_has_few_shot_examples`
   5.6 [ ] Implementar `test_prompt_no_todos`
   5.7 [ ] Implementar `test_minimum_techniques`
   5.8 [ ] Executar `pytest tests/test_prompts.py`
   5.9 [ ] Corrigir o prompt ou os testes caso alguma validacao falhe

6. Implementar o push do prompt otimizado
   6.1 [ ] Analisar o esqueleto existente em `src/push_prompts.py`
   6.2 [ ] Ler o prompt otimizado de `prompts/bug_to_user_story_v2.yml`
   6.3 [ ] Fazer push para o LangSmith com o nome versionado `{seu_username}/bug_to_user_story_v2`
   6.4 [ ] Enviar metadados como tags, descricao e tecnicas utilizadas
   6.5 [ ] Executar `python src/push_prompts.py`
   6.6 [ ] Verificar no dashboard do LangSmith se o prompt foi publicado
   6.7 [ ] Tornar o prompt publico

7. Executar a avaliacao automatica
   7.1 [ ] Executar `python src/evaluate.py`
   7.2 [ ] Verificar as metricas Helpfulness, Correctness, F1-Score, Clarity e Precision
   7.3 [ ] Confirmar se todas as metricas estao com pontuacao maior ou igual a 0.8
   7.4 [ ] Confirmar se a media das cinco metricas tambem esta maior ou igual a 0.8

8. Iterar ate atingir os criterios de aprovacao
   8.1 [ ] Analisar as metricas abaixo de 0.8
   8.2 [ ] Consultar traces do LangSmith para entender falhas de resposta
   8.3 [ ] Ajustar o prompt em `prompts/bug_to_user_story_v2.yml`
   8.4 [ ] Fazer novo push do prompt otimizado
   8.5 [ ] Executar nova avaliacao
   8.6 [ ] Repetir o ciclo ate todas as metricas atingirem pelo menos 0.8
   8.7 [ ] Registrar as iteracoes e os aprendizados do processo

9. Documentar o processo no README
   9.1 [ ] Criar ou atualizar a secao "Tecnicas Aplicadas (Fase 2)"
   9.2 [ ] Descrever as tecnicas escolhidas e suas justificativas
   9.3 [ ] Incluir exemplos praticos de aplicacao das tecnicas
   9.4 [ ] Criar ou atualizar a secao "Resultados Finais"
   9.5 [ ] Adicionar link publico do dashboard do LangSmith
   9.6 [ ] Adicionar screenshots ou evidencias das avaliacoes
   9.7 [ ] Criar tabela comparativa entre prompt v1 e prompt v2
   9.8 [ ] Criar ou atualizar a secao "Como Executar"
   9.9 [ ] Documentar pre-requisitos, dependencias e comandos de execucao

10. Preparar as evidencias e a entrega final
    10.1 [ ] Confirmar que o repositorio contem todo o codigo-fonte implementado
    10.2 [ ] Confirmar que `prompts/bug_to_user_story_v2.yml` esta completo e funcional
    10.3 [ ] Confirmar que `README.md` esta atualizado com tecnicas, resultados e execucao
    10.4 [ ] Confirmar que o dashboard ou screenshots do LangSmith mostram o dataset com 15 exemplos
    10.5 [ ] Confirmar que as execucoes do prompt v2 mostram notas maiores ou iguais a 0.8
    10.6 [ ] Confirmar que ha tracing detalhado de pelo menos 3 exemplos
    10.7 [ ] Publicar ou manter o fork do repositorio como publico no GitHub
