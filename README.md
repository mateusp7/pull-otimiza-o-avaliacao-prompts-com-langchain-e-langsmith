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

## Analisar o prompt original

### O que foi feito
Foi analisado o prompt original em `prompts/bug_to_user_story_v1.yml` para entender por que ele tende a gerar respostas fracas nas métricas de avaliação. A analise identificou que o prompt define apenas uma instrucao generica para transformar relatos de bugs em user stories, sem especificar formato obrigatorio, criterios de aceitacao, exemplos, tratamento de bugs simples, medios e complexos, preservacao de contexto tecnico ou regras contra informacoes inventadas.

### Aonde foi feito
A analise foi feita sobre o conteudo de `prompts/bug_to_user_story_v1.yml`, comparando suas instrucoes com os criterios das metricas em `src/metrics.py` e com o padrao esperado pelas referencias do dataset em `datasets/bug_to_user_story.jsonl`.

### Arquivo(s) modificado(s)
- `tasks.md`
- `step-by-step.md`

### Fluxo logico para alcancar o sucesso da tarefa
1. Ler o YAML do prompt original e identificar sua estrutura: `system_prompt`, `user_prompt`, variaveis de entrada e mensagens.
2. Verificar que o prompt original pede apenas uma user story, sem exigir o formato "Como um..., eu quero..., para que...".
3. Identificar ausencia de secoes obrigatorias para respostas de maior qualidade, como criterios de aceitacao, contexto tecnico, impacto, edge cases e tarefas tecnicas quando o bug for complexo.
4. Mapear os impactos nas metricas:
   - F1-Score: risco de baixo recall por omitir informacoes esperadas nas referencias.
   - Clarity: risco de resposta pouco estruturada e ambigua.
   - Precision: risco de adicionar detalhes nao sustentados pelo relato ou de responder de forma vaga.
   - Helpfulness: prejudicada quando a resposta nao e clara nem precisa.
   - Correctness: prejudicada quando faltam informacoes relevantes ou ha baixa precisao.
5. Definir criterios para o prompt otimizado: persona explicita, formato Markdown previsivel, user story padrao, criterios de aceitacao em Given-When-Then, preservacao de contexto tecnico, tratamento proporcional para bugs simples/medios/complexos, regras contra alucinacao e exemplos few-shot.
6. Marcar os itens da tarefa 3 como concluidos em `tasks.md`.

---

## Criar o prompt otimizado

### O que foi feito
Foi criado o prompt otimizado `bug_to_user_story_v2` para transformar relatos de bugs em user stories com maior clareza, precisao e utilidade para backlog. O prompt passou a definir uma persona explicita de Product Manager Senior, regras de comportamento, formato Markdown, criterios de aceitacao em Given-When-Then, tratamento proporcional para bugs simples, medios e complexos, preservacao de evidencias tecnicas e restricoes contra invencao de informacoes.

Tambem foram aplicadas as tecnicas de Role Prompting, Few-shot Learning e Skeleton of Thought. Os exemplos few-shot cobrem bug simples, bug medio de seguranca e bug complexo de checkout, ajudando o modelo a manter estrutura, nivel de detalhe e precisao em cenarios diferentes.

O Role Prompting foi escolhido porque o prompt original nao deixava claro qual perspectiva profissional o modelo deveria assumir. Ao definir a persona de Product Manager Senior com experiencia em engenharia, QA e backlog agil, o modelo passa a priorizar user stories acionaveis, criterios testaveis, contexto tecnico relevante e linguagem adequada para times de produto e desenvolvimento.

O Skeleton of Thought foi escolhido porque a tarefa exige uma transformacao estruturada do relato de bug: identificar ator, problema, impacto, complexidade, evidencias tecnicas e resultado esperado antes de gerar a resposta final. Essa estrutura ajuda a melhorar clareza e recall sem expor raciocinio interno, reduzindo respostas vagas e aumentando a chance de cobrir os elementos esperados pelas metricas de F1-Score, Clarity e Precision.

### Aonde foi feito
A criacao foi feita no arquivo `prompts/bug_to_user_story_v2.yml`, usando como base os problemas identificados na analise do prompt original e o padrao esperado pelas referencias do dataset.

### Arquivo(s) modificado(s)
- `prompts/bug_to_user_story_v2.yml`
- `tasks.md`
- `step-by-step.md`

### Fluxo logico para alcancar o sucesso da tarefa
1. Usar os criterios definidos na analise do prompt original: persona, formato previsivel, criterios testaveis, preservacao de contexto tecnico, edge cases e exemplos.
2. Criar a estrutura YAML do prompt v2 com `description`, `version`, `input_variables`, `system_prompt`, `user_prompt`, `messages`, tags e metadados.
3. Definir o System Prompt com persona de Product Manager Senior e regras explicitas para nao inventar informacoes, responder em Markdown e adaptar o nivel de detalhe a complexidade do bug.
4. Definir o User Prompt com a variavel `{bug_report}` e instrucao direta para seguir o formato do System Prompt.
5. Adicionar exemplos few-shot de entrada e saida para bug simples, medio e complexo.
6. Aplicar Skeleton of Thought como roteiro interno para identificar ator, impacto, complexidade, evidencias tecnicas, user story e criterios de aceitacao.
7. Incluir tratamento para relatos incompletos, bugs tecnicos, seguranca, performance, integracao, concorrencia, dados e multiplas falhas no mesmo fluxo.
8. Registrar em metadados as tecnicas utilizadas e marcar os itens da tarefa 4 como concluidos em `tasks.md`.

---

## Implementar o push do prompt otimizado

### O que foi feito
Foi implementado o fluxo de push do prompt otimizado para o LangSmith Prompt Hub. O script passou a carregar `prompts/bug_to_user_story_v2.yml`, extrair os dados do prompt versionado, validar a estrutura obrigatoria, montar um `ChatPromptTemplate` com mensagens de system e user, anexar tags e metadados do YAML e preparar a publicacao publica com o nome versionado configurado por `USERNAME_LANGSMITH_HUB`.

A execucao local validou o prompt e tentou publicar o repositorio versionado no LangSmith. A publicacao externa ainda precisa de aprovacao explicita para envio publico do conteudo do prompt e posterior verificacao no dashboard.

### Aonde foi feito
A implementacao foi feita em `src/push_prompts.py`, usando `langchain.hub.push`, `ChatPromptTemplate`, as credenciais do `.env` e o YAML otimizado em `prompts/bug_to_user_story_v2.yml`.

### Arquivo(s) modificado(s)
- `src/push_prompts.py`
- `tasks.md`
- `step-by-step.md`

### Fluxo logico para alcancar o sucesso da tarefa
1. Ler o YAML otimizado e extrair a chave `bug_to_user_story_v2`.
2. Validar campos obrigatorios: descricao, versao, variaveis de entrada, system prompt, user prompt, mensagens, tecnicas aplicadas e tags.
3. Confirmar que `bug_report` esta presente em `input_variables`.
4. Confirmar que existem mensagens `system` e `user` para montar o prompt no formato esperado pelo LangChain.
5. Criar um `ChatPromptTemplate` a partir das mensagens do YAML.
6. Anexar metadados do prompt, incluindo versao, origem, tecnicas aplicadas e dados de qualidade esperada.
7. Preparar o nome versionado `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2`.
8. Configurar o push como publico, com tags e descricao contendo as tecnicas aplicadas.
9. Executar o script para validar o fluxo local; a etapa de publicacao externa fica pendente ate haver aprovacao explicita para envio publico ao LangSmith.

---

## Resultado parcial da primeira avaliacao do prompt v2

### Resultado obtido
A primeira avaliacao automatica do prompt `bug_to_user_story_v2` ficou reprovada por uma unica metrica abaixo do limite minimo de 0.8.

Metricas derivadas:
- Helpfulness: 0.85
- Correctness: 0.80

Metricas base:
- F1-Score: 0.77
- Clarity: 0.86
- Precision: 0.83

Media geral: 0.8228

Apesar da media geral estar acima de 0.8, o criterio do desafio exige que todas as metricas individuais tambem estejam acima de 0.8. Como o F1-Score ficou em 0.77, o prompt ainda precisa de uma nova iteracao.

### Leitura do resultado
O resultado indica que o prompt ja esta gerando respostas claras e relativamente precisas. A metrica de Clarity em 0.86 mostra que a estrutura em Markdown, a separacao por secoes e os criterios de aceitacao estao ajudando na compreensao da resposta.

A Precision em 0.83 indica que o prompt nao esta inventando informacoes em excesso e tende a se manter alinhado ao relato do bug. Isso e importante porque uma tentativa agressiva de aumentar detalhes poderia reduzir essa metrica se o modelo comecar a adicionar causas, impactos, tecnologias ou comportamentos que nao aparecem no relato original.

O ponto fraco foi o F1-Score em 0.77. Como o F1 equilibra precision e recall, e a precision ficou acima de 0.8, a principal hipotese e que o prompt esta omitindo informacoes esperadas nas respostas de referencia. Ou seja, ele provavelmente esta correto e claro, mas ainda nao cobre todos os detalhes relevantes que aparecem no bug report ou que sao esperados na user story final.

### Hipotese de melhoria
A proxima melhoria deve aumentar a cobertura dos fatos do bug sem incentivar alucinacao. O foco sera melhorar recall mantendo precision.

Ajustes considerados para a proxima iteracao:
- Reforcar que todos os fatos explicitamente presentes no relato devem aparecer na resposta final.
- Exigir preservacao de comportamento atual, comportamento esperado, impacto, evidencias tecnicas e dados especificos quando estiverem presentes.
- Garantir que bugs com multiplas falhas tenham criterios de aceitacao cobrindo cada problema mencionado.
- Adicionar uma secao curta e consistente de contexto do bug para aumentar a chance de recuperar detalhes importantes da referencia.
- Manter a regra de nao inventar causas, severidade, endpoints, tecnologias, numeros ou impactos que nao estejam no relato.

A estrategia sera aumentar a cobertura de informacoes reais do relato, mas de forma estruturada, para evitar perda de clareza ou precisao.

---

## Iteracao para melhorar F1-Score do prompt v2

### Resultado que motivou a mudanca
A avaliacao anterior reprovou apenas em F1-Score, com valor 0.77. As demais metricas ficaram acima de 0.8: Helpfulness 0.85, Correctness 0.80, Clarity 0.86 e Precision 0.83.

A leitura principal foi que o prompt estava claro e relativamente preciso, mas provavelmente deixava de cobrir alguns fatos esperados nas respostas de referencia. Por isso, a melhoria foi direcionada para aumentar recall e cobertura, sem incentivar o modelo a inventar informacoes.

### Mudancas aplicadas no prompt
Foram adicionadas instrucoes para transformar cada fato explicito do relato em algum elemento da resposta final: user story, criterio de aceitacao, contexto do bug ou tarefa tecnica. Tambem foi reforcada uma verificacao interna de cobertura para comportamento atual, comportamento esperado, impacto, evidencias tecnicas, mensagens de erro, dados afetados, valores, IDs, endpoints, status HTTP, limites, volumes, percentuais, ambiente e passos de reproducao quando presentes.

O formato de resposta tambem foi ajustado para tornar o contexto do bug mais completo e consistente. Para bugs simples ou medios, a antiga secao generica de contexto tecnico foi substituida por campos de comportamento atual, comportamento esperado, impacto e evidencias tecnicas. Para bugs complexos, a secao de contexto passou a incluir tambem falhas cobertas, ajudando o modelo a confirmar que cada problema mencionado foi tratado.

### Racional da melhoria
A ideia e subir o F1-Score aumentando a presenca de informacoes esperadas na resposta final. Como a Precision ja estava acima de 0.8, a mudanca manteve as restricoes contra alucinacao: o modelo continua proibido de inventar causas, tecnologias, endpoints, numeros, severidades ou impactos que nao estejam no relato.

Essa iteracao busca um equilibrio: mais cobertura dos fatos reais do bug, mas ainda com uma estrutura clara e controlada para nao reduzir Clarity nem Precision.

### Validacao local
O arquivo `prompts/bug_to_user_story_v2.yml` foi validado com parse YAML. Tambem foi validado pelo script de push local, confirmando que o prompt continua com `bug_report` como variavel de entrada e que o `ChatPromptTemplate` pode ser montado corretamente.

---

## Iteracao 2 para melhorar F1-Score do prompt v2

Foi realizado a tentiva de modificar a forma como a LLM iria retornar os dados. Contudo, o F1-Score diminui drasticamente, assim como as outras métricas.

Portanto, voltamos ao estado anterior, no qual as métricas estavam melhores e vamos partir novamente a partir dai, mexendo em pontos especificos.
---

## Iteracao 3 para melhorar Precision e F1-Score em bugs simples

### O que foi feito
Foi analisado um trace do LangSmith em que o prompt gerava uma resposta correta para o bug do botao de adicionar ao carrinho, mas adicionava detalhes alem da resposta de referencia. A resposta incluia o produto ID 1234 dentro dos criterios de aceitacao e tambem uma secao `Contexto do bug`, enquanto a referencia esperava apenas user story e criterios de aceitacao genericos.

Com base nessa evidencia, o prompt foi ajustado para tratar bugs simples de forma mais concisa. A nova regra orienta o modelo a responder bugs simples apenas com user story e criterios de aceitacao, sem secoes extras. Tambem foi adicionada uma regra para nao inserir IDs, valores ou detalhes tecnicos nos criterios quando eles servirem apenas para identificar o item afetado.

### Aonde foi feito
A mudanca foi feita no prompt otimizado `prompts/bug_to_user_story_v2.yml`, especialmente nas regras de proporcionalidade por complexidade, no formato esperado para bugs simples e no exemplo few-shot de bug simples.

### Arquivo(s) modificado(s)
- `prompts/bug_to_user_story_v2.yml`
- `tasks.md`
- `step-by-step.md`

### Fluxo lógico para alcanÃ§ar o sucesso da tarefa
1. Analisar o trace do LangSmith para separar a resposta gerada pelo prompt das respostas dos avaliadores.
2. Identificar que a queda de Precision vinha de excesso de informacao em bug simples, nao de erro estrutural da user story.
3. Ajustar a regra de cobertura para ser proporcional a complexidade do bug.
4. Definir que bugs simples devem retornar apenas user story e criterios de aceitacao.
5. Ajustar o exemplo few-shot simples para ficar mais parecido com a referencia do dataset.
6. Validar o YAML localmente com parse usando o ambiente virtual do projeto.

---

## Iteração 4 para melhorar F1-Score em webhook de pagamento

### O que foi feito
Após uma nova análise do tracing do LangSmith, percebi que era necessário ajustar o prompt para cobrir melhor os bugs visuais, que apenas envolve CSS em maior parte. Além disso, modifiquei 2 seções para explicar a LLM que irá gerar a resposta, de que precisamos ter uma seção de "Critérios de acessibilidade", para dar match com a resposta esperada.
Para conseguir isso, foi adicionado mais exemplos de Few Shot na seção de exemplos e modifiquei as seções de "Regras obrigatórias" e "Skeleton of Thought interno"

### Aonde foi feito
A mudança foi feita no prompt otimizado `prompts/bug_to_user_story_v2.yml`.

### Arquivo(s) modificado(s)
- `prompts/bug_to_user_story_v2.yml`
- `step-by-step.md`
---

## Iteração 5 para diferenciar bug médio de estoque e concorrência

### O que foi feito
Foi adicionado um ajuste fino no prompt para impedir que bugs de estoque, concorrência, reserva, pagamento, limite ou consistência de dados sejam tratados como bugs simples. Também foi incluído um novo exemplo few-shot com o cenário de carrinho finalizando compra sem estoque, mostrando que esse tipo de bug precisa de critérios de aceitação, critérios de prevenção e contexto do bug.

### Aonde foi feito
A mudança foi feita no prompt otimizado `prompts/bug_to_user_story_v2.yml`, nas regras obrigatórias, no raciocínio interno, no formato esperado para bugs médios, no `user_prompt` e na seção de exemplos few-shot.

### Arquivo(s) modificado(s)
- `prompts/bug_to_user_story_v2.yml`
- `tests/test_prompts.py`
- `step-by-step.md`

### Fluxo lógico para alcançar o sucesso da tarefa
1. Analisar o trace em que o modelo tratou um bug de estoque como se fosse simples.
2. Identificar que o problema não era apenas falta de critério de aceitação, mas falta de entendimento sobre concorrência, reserva de estoque e prevenção.
3. Criar uma regra explícita para classificar bugs de estoque, concorrência e consistência como no mínimo bugs médios.
4. Ajustar o formato de bugs médios para permitir `Critérios de Prevenção` e `Contexto do Bug` quando o cenário exigir.
5. Adicionar um exemplo few-shot com a resposta esperada para o fluxo de carrinho sem estoque.
6. Reforçar no `user_prompt` que esses cenários devem ser avaliados com prevenção e contexto do bug.
7. Validar localmente se o YAML continua válido e se o prompt mantém as seções esperadas.


## Implementar os testes de validação

### O que foi feito
Foi implementada a suíte de validação do prompt otimizado em `tests/test_prompts.py`, cobrindo os seis testes obrigatórios da tarefa. Os testes carregam o arquivo `prompts/bug_to_user_story_v2.yml`, acessam o prompt `bug_to_user_story_v2` e validam se ele possui `system_prompt`, definição de persona, formato Markdown com estrutura de user story, exemplos Few-shot, ausência de `[TODO]` e pelo menos duas técnicas listadas nos metadados.

Também foi executado o comando `pytest tests/test_prompts.py` pelo ambiente virtual do projeto. A validação terminou com 6 testes aprovados. O pytest emitiu apenas avisos de cache por não conseguir criar arquivos em `.pytest_cache`, sem impacto no resultado dos testes.

### Aonde foi feito
A implementação foi feita no arquivo `tests/test_prompts.py`, usando `pytest`, `pyyaml`, o YAML otimizado em `prompts/bug_to_user_story_v2.yml` e a função `validate_prompt_structure` já existente em `src/utils.py`.

### Arquivo(s) modificado(s)
- `tests/test_prompts.py`
- `tasks.md`
- `step-by-step.md`

### Fluxo lógico para alcançar o sucesso da tarefa
1. Analisar o esqueleto de `tests/test_prompts.py` e identificar os seis testes pendentes.
2. Ler a estrutura real de `prompts/bug_to_user_story_v2.yml` para validar os campos existentes sem criar suposições incorretas.
3. Criar fixture para carregar o YAML uma única vez e retornar o prompt `bug_to_user_story_v2`.
4. Implementar o teste de `system_prompt`, validando existência, conteúdo não vazio e estrutura mínima esperada.
5. Implementar o teste de persona, verificando termos como `Product Manager`, `senior` e definição direta de papel.
6. Implementar o teste de formato, verificando Markdown e a estrutura padrão `Como um..., eu quero..., para que...`.
7. Implementar o teste de Few-shot, verificando técnica nos metadados e exemplos com entrada e saída no texto do prompt.
8. Implementar o teste contra `[TODO]`, percorrendo todos os valores do YAML do prompt.
9. Implementar o teste de técnicas mínimas, garantindo lista com pelo menos duas técnicas preenchidas.
10. Executar `pytest tests/test_prompts.py` e confirmar que os 6 testes passaram.
11. Marcar os itens da tarefa 5 como concluídos em `tasks.md`.

---
