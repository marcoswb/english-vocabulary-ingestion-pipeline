import logging

from src.controllers.extract_news_articles import ExtractArticles
from src.controllers.build_vocabulary_dataset import BuildVocabularyDataset

def main():
    logging.info("Starting pipeline")

    extract_articles = ExtractArticles()
    extract_articles.run()

    build_vocabulary_dataset = BuildVocabularyDataset()
    build_vocabulary_dataset.run()

    logging.info("Pipeline completed")


if __name__ == "__main__":

    logging.basicConfig(
        filename="logs/pipeline.log",
        level=logging.INFO,
    )

    main()