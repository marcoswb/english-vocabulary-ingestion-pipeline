from src.models.postgres import Postgres


class CandidateWordsSentences(Postgres):
    def __init__(self):
        super().__init__('candidate_words_sentences')

    def insert_line(self, id_word, sentence):
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(id_word, sentence) VALUES (%s, %s) RETURNING id'
        cursor.execute(base_sql, (id_word, sentence))

        new_id = cursor.fetchone()[0]
        self.connection.commit()

        return new_id

    def get_all_english_words(self):
        query = f"""
            select word
            from {self.schema}.{self.table_name}
        """
        result = self.select_without_header(query)
        return result
