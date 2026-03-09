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

    def to_dict(self):
        return {
            'article_id': str(self.article_id),
            'source_id': self.source_id,
            'url': self.url,
            'published_at': self.published_at,
            'collected_at': self.collected_at,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'full_text': self.full_text,
            'author': self.author,
            'category': self.category,
            'language': self.language
        }
