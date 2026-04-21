FROM apache/airflow:2.9.0

RUN pip install wordfreq
RUN pip install spacy
RUN pip install nltk
RUN python -m nltk.downloader stopwords
RUN python -m spacy download en_core_web_sm

USER airflow