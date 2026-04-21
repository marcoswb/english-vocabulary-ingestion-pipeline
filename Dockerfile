FROM apache/airflow:2.9.0

RUN pip install nltk
RUN python -m nltk.downloader stopwords

USER airflow