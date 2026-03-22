# AutMiniETL

[Read in English](README.md)

O AutMiniETL e uma mini plataforma ETL em Python que:

- Coleta dados (API, scraping ou mock local)
- Transforma dados com Pandas
- Carrega dados em SQLite (padrao) ou PostgreSQL
- Gera relatorios automaticos
- Mantem logs de execucao e versoes de dataset
- Oferece um dashboard simples em Streamlit

## Estrutura do projeto

```
autminietl/
  __init__.py
  collect.py
  config.py
  db.py
  load.py
  logger.py
  pipeline.py
  report.py
  transform.py
run_pipeline.py
scheduler_app.py
dashboard.py
requirements.txt
.env.example
```

## Configuracao

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

## Executar uma vez

```bash
python run_pipeline.py --source mock
```

Fontes disponiveis: `mock`, `api`, `scrape`.

## Executar agendador

```bash
python scheduler_app.py
```

O agendador executa usando `DEFAULT_SOURCE` a cada `SCHEDULE_MINUTES`.

## Abrir dashboard

```bash
streamlit run dashboard.py
```

## Banco de dados

URL padrao do banco:

```env
DATABASE_URL=sqlite:///data/autminietl.db
```

Para PostgreSQL, configure por exemplo:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/autminietl
```

## Tabelas principais

- `etl_runs`: logs de execucao (status, duracao, erros)
- `dataset_versions`: versoes de dataset por hash de conteudo
- `records`: registros transformados vinculados a uma versao
