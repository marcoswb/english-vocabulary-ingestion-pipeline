from src.models.postgres import Postgres


class Vocabulary(Postgres):
    def __init__(self):
        super().__init__('vocabulary')

    def get_all_english_words(self):
        query = f"""
            select word
            from {self.schema}.{self.table_name}
        """
        result = self.select_without_header(query)
        return result
