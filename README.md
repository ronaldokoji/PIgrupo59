# PIgrupo59

Dashboard academico em Streamlit para analise de acidentes em rodovias federais com foco no estado de Sao Paulo e benchmark nacional.

## Visao do projeto

O repositorio usa a base publica de acidentes da PRF disponibilizada no Kaggle:

https://www.kaggle.com/datasets/pedrogoncalv/brazilian-traffic-incidents-2007-to-2023

O app final trabalha com dois recortes derivados da base local versionada:

- `SP`: recorte principal usado nas metricas e filtros do dashboard
- `Brasil`: benchmark nacional calculado sobre o mesmo periodo disponivel localmente

## Estrutura

- `streamlit_app.py`: entrypoint recomendado para o Streamlit Cloud
- `app/dashboard.py`: interface do dashboard
- `src/etl.py`: pipeline para gerar as bases tratadas
- `data/base_original.csv`: base original do projeto
- `data/base_tratada.csv`: base tratada de SP
- `data/base_brasil_tratada.csv`: base tratada do Brasil para benchmark

## Metricas personalizadas

O dashboard inclui metricas operacionais derivadas apenas dos campos presentes na base:

- total de acidentes, mortes e feridos graves
- taxa de fatalidade por acidente
- taxa de acidentes graves por acidente
- indice de severidade
- rodovias mais criticas por severidade media
- municipios mais criticos por severidade media
- janelas horarias mais criticas
- ranking de causas com maior taxa de acidentes graves
- contraste entre uso urbano e nao urbano

Indice de severidade adotado:

`5 x mortos + 3 x feridos graves + 1 x feridos leves`

## Como executar localmente

1. Instale as dependencias:

```bash
pip install -r requirements.txt
```

2. Gere as bases tratadas:

```bash
python src/etl.py
```

3. Rode o app:

```bash
streamlit run streamlit_app.py
```

## Deploy no Streamlit Cloud

Ao criar o app no Streamlit Cloud:

- selecione este repositorio
- defina o arquivo principal como `streamlit_app.py`
- mantenha `requirements.txt` na raiz

Nao ha dependencia de segredos, APIs externas ou tokens para o funcionamento basico do dashboard.
