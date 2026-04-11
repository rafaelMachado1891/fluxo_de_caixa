# Fluxo de Caixa

Projeto de engenharia de dados e analytics para estruturar o fluxo de caixa em uma base analitica confiavel, com pipeline de ingestao, modelagem em dbt, orquestracao com Airflow e uma camada de consulta em linguagem natural com FastAPI + Streamlit.

## Objetivo

Este projeto foi construido para transformar registros financeiros dispersos em um ambiente analitico centralizado, capaz de:

- consolidar entradas, saidas e saldos em uma unica base;
- reduzir retrabalho manual e inconsistencias;
- padronizar calculos financeiros;
- apoiar a tomada de decisao com dados rastreaveis;
- habilitar consultas rapidas sobre o fluxo de caixa por meio de um assistente financeiro.

## Arquitetura

![Arquitetura do projeto](especificacao_projeto/arquitetura.png)

De forma geral, a solucao esta organizada assim:

1. ingestao de dados com Python;
2. armazenamento central em PostgreSQL;
3. transformacao e modelagem com dbt;
4. orquestracao com Apache Airflow;
5. consumo analitico em dashboards;
6. consulta em linguagem natural por meio de API FastAPI e frontend Streamlit.

## Estrutura do repositorio

```text
backend/                API e assistente financeiro
src/                    pipeline de ingestao/carga
dags/                   DAG do Airflow
include/                funcoes auxiliares usadas pelo Airflow
dw_fluxo_caixa/         projeto dbt
```

## Como rodar

As instrucoes abaixo consideram o fluxo correto do projeto:

- [`src/docker-compose.yml`](src/docker-compose.yml): sobe PostgreSQL e pgAdmin;
- `astro dev start`: sobe o ambiente local do Airflow via Astro CLI.

### Pre-requisitos

- Python 3.12.4 recomendado
- Docker Desktop com Docker Compose
- Astro CLI instalada
- chave `API_KEY` da OpenAI para a camada de assistente

> Observacao: o arquivo [`.python-version`](.python-version) aponta para Python `3.12.4`. Se voce estiver usando outra versao, vale validar compatibilidade antes de instalar os pacotes.

### 1. Instale as dependencias Python

Se voce estiver no PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se voce estiver no Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Se o comando `python -m venv .venv` travar ou for interrompido, apague a pasta `.venv` incompleta e rode novamente.

### 2. Configure as variaveis de ambiente

Use o arquivo de exemplo como ponto de partida:

```powershell
Copy-Item .env_example .env
```

Depois ajuste os valores conforme o seu ambiente. O arquivo [`.env_example`](.env_example) cobre:

- backend local via `POSTGRES_*`;
- dbt/Airflow via `DBT_*`;
- chave `API_KEY` da OpenAI.

### 3. Suba o PostgreSQL e o pgAdmin

O banco PostgreSQL da solucao pode ser iniciado a partir de [`src/docker-compose.yml`](src/docker-compose.yml). Esse compose tambem sobe o pgAdmin e usa a rede Docker externa `postgres_fluxo_network`.

Se essa rede ainda nao existir, crie-a:

```powershell
docker network create postgres_fluxo_network
```

Depois suba os servicos de banco:

```powershell
docker compose -f src/docker-compose.yml up -d
```

Servicos disponibilizados:

- `postgres_fluxo` na porta `5440`;
- `pgadmin_fluxo` em `http://localhost:5050`.

### 4. Rode a orquestracao com Airflow via Astro

Com o banco em execucao, suba o projeto do Airflow com a Astro CLI:

```powershell
astro dev start
```

Esse comando cria o ambiente local do Airflow para o projeto atual e publica a interface em:

- `http://localhost:8080`

Se for a primeira execucao, o processo pode levar alguns minutos por causa da criacao das imagens e containers locais.

### 5. Configure a conexao do Airflow

O pipeline Python em [`src/pipeline.py`](src/pipeline.py) usa `BaseHook.get_connection("postgres_fluxo")`.

Este repositorio ja deixa a conexao `postgres_fluxo` definida em [`airflow_settings.yaml`](airflow_settings.yaml) para o ambiente local do Astro. Com isso, ao subir com `astro dev start`, o Airflow ja deve conseguir se conectar ao banco usando os valores padrao documentados no [`.env_example`](.env_example).

Se voce alterar usuario, senha, nome do banco ou porta interna do Postgres no compose, atualize tambem a conexao em [`airflow_settings.yaml`](airflow_settings.yaml).

### 6. Execute a DAG

A DAG principal esta em [`dags/dag.py`](dags/dag.py) e executa:

1. a carga dos CSVs para o PostgreSQL;
2. `dbt seed`;
3. `dbt run`.

Depois de subir o Airflow, a DAG pode ser disparada pela interface web.

### 7. Rodando a API localmente

Com o ambiente Python ativo e as variaveis configuradas:

```powershell
$env:PYTHONPATH="backend"
uvicorn main:app --app-dir backend --reload
```

A API responde em:

```text
POST http://127.0.0.1:8000/perguntar
```

### 8. Rodando o frontend Streamlit

Em outro terminal:

```powershell
streamlit run backend/app.py
```

O frontend envia perguntas para a API em `http://127.0.0.1:8000/perguntar`.

## Ordem recomendada de execucao

Para evitar erros de configuracao, rode nesta sequencia:

1. copie [`.env_example`](.env_example) para `.env`;
2. crie a rede Docker `postgres_fluxo_network`, se necessario;
3. suba PostgreSQL e pgAdmin com `docker compose -f src/docker-compose.yml up -d`;
4. suba o Airflow com `astro dev start`;
5. execute a DAG `dag_executar_pipeline`;
6. inicie a API FastAPI e o frontend Streamlit, se quiser usar o assistente.

## Solucao de problemas

### `Activate.ps1` nao funciona no Git Bash

O comando abaixo e de PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

No Git Bash, use:

```bash
source .venv/Scripts/activate
```

### `Could not open requirements file`

Esse erro normalmente acontece quando o terminal nao esta na raiz do projeto. Antes de instalar, confirme se arquivos como [`README.md`](README.md) e [`requirements.txt`](requirements.txt) aparecem no diretorio atual.

### `python -m venv .venv` foi interrompido

Se a criacao do ambiente virtual parar no meio, remova a pasta `.venv` e tente outra vez. Uma criacao incompleta faz a ativacao falhar depois.

## Fluxo de execucao do projeto

1. os dados de origem sao ingeridos por scripts Python;
2. a carga inicial popula tabelas brutas no PostgreSQL;
3. o dbt organiza os dados em camadas `raw`, `staging`, `intermediate` e `marts`;
4. o Airflow orquestra a sequencia de execucao;
5. os dados modelados alimentam analises financeiras e dashboards;
6. o assistente financeiro consulta os dados modelados para responder perguntas do usuario.

## Motivacao do desenvolvimento

O projeto nasce de um problema comum em empresas: o controle de fluxo de caixa muitas vezes fica espalhado entre planilhas, relatorios manuais, ERPs e registros contabeis que nao conversam entre si.

Esse contexto gera efeitos diretos:

- consolidacao manual de dados;
- maior risco de erro operacional;
- baixa confiabilidade para analises historicas;
- pouca previsibilidade financeira;
- muito tempo gasto para gerar relatorios.

A proposta desta solucao e substituir esse processo fragmentado por uma arquitetura de dados que centraliza informacoes, padroniza regras de negocio e transforma movimentacoes financeiras em inteligencia analitica.

## Problema de negocio

O fluxo de caixa e um dos principais instrumentos de controle financeiro porque permite:

- acompanhar liquidez;
- antecipar periodos de maior pressao sobre o caixa;
- apoiar decisoes sobre custos, investimentos e planejamento;
- identificar desequilibrios entre entradas e saidas;
- reduzir dependencia de analises reativas.

Com dados descentralizados, a empresa perde visibilidade e passa a tomar decisoes com menos confianca. O projeto foi desenvolvido justamente para corrigir isso.

## Fontes e uso dos dados

Segundo a especificacao do projeto, os dados de fluxo de caixa podem vir de:

- sistemas de gestao empresarial;
- planilhas financeiras;
- extratos bancarios;
- relatorios contabeis;
- registros operacionais recorrentes de pagamentos e recebimentos.

Esses dados sao utilizados por areas financeiras, administrativas e gestao para:

- acompanhar entradas e saidas;
- medir saldo operacional;
- avaliar saldos inicial e final;
- planejar curto e medio prazo;
- antecipar risco de liquidez.

## Modelagem analitica

O projeto segue uma arquitetura em camadas no dbt:

- `raw`: preserva os dados na forma original;
- `staging`: aplica padronizacao inicial;
- `intermediate`: concentra regras de negocio e enriquecimento;
- `marts`: disponibiliza modelos finais para consumo analitico.

Na camada final, a organizacao segue abordagem dimensional, com fatos e dimensoes para facilitar consultas, rastreabilidade e escalabilidade.

Exemplos de entidades modeladas no repositorio:

- fatos de lancamentos;
- dimensao calendario;
- dimensao clientes;
- dimensao instituicoes;
- dimensao plano de contas;
- dimensao saldo inicial.

## Indicadores de negocio

Os principais KPIs descritos na especificacao sao:

- entradas;
- saidas;
- saldo operacional;
- saldo inicial;
- saldo final;
- distribuicao por conta e banco;
- analises mensais e acumuladas;
- visoes projetadas de entradas e saidas.

Esses indicadores respondem perguntas como:

- o caixa esta aumentando ou diminuindo?
- as entradas cobrem as saidas?
- onde estao concentrados os maiores gastos?
- existe risco de falta de liquidez?
- como o saldo evolui ao longo do tempo?

## Assistente financeiro

O repositorio tambem inclui uma camada de consulta em linguagem natural:

- a API em [`backend/main.py`](backend/main.py) recebe perguntas;
- o planner interpreta a intencao da pergunta;
- as metricas consultam o banco;
- o frontend em [`backend/app.py`](backend/app.py) exibe a resposta no Streamlit.

Pelo codigo atual, o assistente foi pensado para responder de forma deterministica sobre metricas financeiras, reduzindo o risco de respostas alucinadas e aproximando a IA de um motor analitico guiado por regras.

## Stack utilizada

- Python
- PostgreSQL
- pgAdmin
- dbt
- Apache Airflow
- Docker
- FastAPI
- Streamlit
- OpenAI API


## Dependencias operacionais

Para a execucao completa do projeto, tambem entram em cena as ferramentas e servicos da arquitetura:

- PostgreSQL
- pgAdmin
- Apache Airflow
- dbt
- Docker e Docker Compose
- OpenAI API, usada pelo assistente financeiro
