from uuid import uuid4

class ArticleModel:
    def __init__(self):
        self.article_id = uuid4()
        self.source_id = ''
        self.url = ''
        self.published_at = ''
        self.collected_at = ''
        self.title = ''
        self.description = ''
        self.content = ''
        self.full_text = ''
        self.author = ''
        self.category = ''
        self.language = "en"
