# PIgrupo59
# Projeto Integrador do 1º trimestre de 2026 - GRUPO 25
## Integrantes
- FERNANDO CAMARA DE MORAES
- JHULLY CAROLINY RODRIGUES VIEIRA DA SILVA
- MURILO SANTOS DORIGO
- RAUL ALEXANDRE MARIA
- RONALDO KOJI YAMASAKI
- TAMIRES FERREIRA NUNES

## Tema do Projeto
Análise de Dados de Acidentes de Trânsito em Rodovias Federais no Estado de São Paulo

## Objetivo
O projeto tem como objetivo analisar dados de acidentes de trânsito ocorridos em rodovias federais no estado de São Paulo, buscando identificar padrões relacionados à ocorrência dos  acidentes, como horários, locais e tipos de veículos envolvidos.

## Planejamento
1) Definir o Tema do Projeto (até 08/03/2026)
2) Formular o Objetivo do Projeto (até 08/03/2026)
3) Criação e Organização do Repositório (até 15/03/2026)
4) Definir, coletar a base de dados original e fazer o upload da mesma no repositório, pasta 'data' (até 15/03/2026)
5) Descrever o processo de ETL (até 22/03/2026)
6) Detalhar o planejamento do dashboard (até 22/03/2026)

## Base de Dados

A base de dados utilizada neste projeto será obtida na plataforma Kaggle, que disponibiliza conjuntos de dados públicos para análise de dados.

Dataset utilizado:
https://www.kaggle.com/datasets/pedrogoncalv/brazilian-traffic-incidents-2007-to-2023

O dataset contém informações sobre acidentes de trânsito ocorridos no Brasil entre os anos de 2007 e 2023, incluindo dados como:

- data do acidente
- estado e município
- causa do acidente
- tipo de veículo envolvido
- gravidade do acidente
- horário da ocorrência

Para este projeto será realizado um recorte dos dados considerando principalmente os registros do estado de São Paulo, permitindo uma análise mais focada da ocorrência de acidentes na região.

---

## Planejamento do Processo ETL

### Extract (Extração)

Os dados serão obtidos a partir de um dataset público disponibilizado na plataforma Kaggle e serão importados para análise utilizando a linguagem Python.

### Transform (Transformação)

Durante essa etapa serão realizadas as seguintes ações utilizando a biblioteca Pandas:

- remoção de dados duplicados  
- tratamento de valores ausentes  
- padronização das informações  
- agrupamento de dados por região ou período  
- criação de métricas para análise  

### Load (Carga)

Após o tratamento dos dados, a base será armazenada em uma estrutura organizada para utilização na criação do dashboard.


## Planejamento das Tarefas

Para o desenvolvimento do projeto, as atividades serão divididas entre os integrantes do grupo da seguinte forma:

| Integrante | Responsabilidade |
|------------|------------------|
| Fernando Camara de Moraes | Organização do repositório e documentação
| Jhully Caroliny Rodrigues Vieira da Silva | Coleta e extração da base de dados
| Murilo Santos Dorigo | Limpeza e tratamento dos dados
| Raul Alexandre Maria | Transformação e organização dos dados
| Ronaldo Koji Yamasaki | Criação das métricas de análise 
| Tamires Ferreira Nunes | Planejamento do projeto e apoio na documentação 

## Objetivo da Análise

O objetivo do projeto é realizar uma análise exploratória dos dados de acidentes de trânsito no estado de São Paulo, buscando identificar padrões relacionados a fatores como:

- local do acidente  
- horário de ocorrência  
- tipo de veículo envolvido  
- frequência dos acidentes  

A partir dessa análise serão desenvolvidas visualizações em um dashboard que facilitem a interpretação dos dados e auxiliem na identificação de possíveis fatores de risco.


## Ideia Inicial do Dashboard
- quantidade de acidentes por cidade ou região
- horários com maior ocorrência de acidentes
- tipos de veículos mais envolvidos em acidentes
- evolução da quantidade de acidentes ao longo do tempo
- indicadores com métricas gerais sobre os acidentes
  
## Tecnologias
- Python
- Pandas
- Streamlit




