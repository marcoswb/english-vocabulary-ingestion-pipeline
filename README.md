# 🧠 English Vocabulary Ingestion Pipeline

Pipeline ETL responsável por **alimentar automaticamente o banco de
dados do bot English Vocabulary Trainer**, coletando textos de sites de
notícias, extraindo palavras relevantes e inserindo novos vocábulos de
forma periódica.

Este projeto utiliza **Apache Airflow, Python, SQL e AWS**, simulando
uma arquitetura moderna de engenharia de dados aplicada a um produto
real.

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

Automatizar a ingestão de novas palavras em inglês a partir de textos
reais (notícias), garantindo que o bot de aprendizado: - receba
vocabulário atualizado - evite palavras duplicadas - priorize palavras
relevantes e frequentes - mantenha histórico e rastreabilidade do
processo

------------------------------------------------------------------------

## 🧱 Arquitetura Geral

Sites de Notícias / APIs\
↓\
Extract (Python)\
↓\
Amazon S3 (Raw Text / Staging)\
↓\
Transform (NLP)\
↓\
Filtragem de Palavras Novas\
↓\
Banco de Dados do Bot (Postgres / SQLite)

Orquestração feita com **Apache Airflow**.

------------------------------------------------------------------------

## 🛠️ Stack Tecnológica

-   Python 3.11+
-   Apache Airflow
-   AWS (S3, RDS, Secrets Manager)
-   SQL
-   NLP (spaCy ou NLTK)
-   Docker

------------------------------------------------------------------------

## 🔄 Pipeline ETL

### Extract

-   Coleta textos de RSS feeds, APIs ou sites públicos
-   Armazena textos brutos no S3

### Transform

-   Limpeza
-   Tokenização
-   Stopwords
-   Lematização
-   Frequência
-   Remoção de duplicados

### Load

-   Inserção das novas palavras no banco do bot
-   Registro de metadados

------------------------------------------------------------------------

## ⏱️ Frequência

-   Inicial: semanal
-   Evolução: coleta diária + inserção semanal

------------------------------------------------------------------------

## 🚀 Evoluções Futuras

-   Classificação por nível
-   Tradução automática
-   Exemplos de frases
-   Dashboard analítico

------------------------------------------------------------------------
## ⚙️ Airflow Variables

| Variable Name     | Description                        | Example Value                |
|------------------|----------------------------------|------------------------------|
| S3_BUCKET_NAME   | S3 bucket to store raw articles  | english-vocab-pipeline       |
------------------------------------------------------------------------

## 🔌 Airflow Connections

The following Airflow connection must be configured:

### aws_default

- Name: aws_default
- Type: Amazon Web Services
- Required fields:
  - Access Key
  - Secret Key
------------------------------------------------------------------------

## 👤 Autor

Marcos Warmling Berti

------------------------------------------------------------------------

## 📄 Licença

MIT
