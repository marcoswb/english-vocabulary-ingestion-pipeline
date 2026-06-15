from src.models.postgres import Postgres


class CandidateWords(Postgres):
    def __init__(self):
        super().__init__('candidate_words')

    def insert_line(self, word, frequency, zipf_score, score):
        cursor = self.connection.cursor()

        base_sql = f'INSERT INTO {self.schema}.{self.table_name}(word, frequency, zipf_score, score, active) VALUES (%s, %s, %s, %s, true) RETURNING id'
        cursor.execute(base_sql, (word, frequency, zipf_score, score))

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
