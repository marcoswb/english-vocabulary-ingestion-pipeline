from uuid import uuid4
import re
from bs4 import NavigableString
from src.utils.functions import get_current_timestamp

class Article:
    def __init__(self, source_id):
        self.article_id = uuid4()
        self.source_id = source_id
        self.url = ''
        self.published_at = ''
        self.collected_at = get_current_timestamp()
        self.title = ''
        self.description = ''
        self.full_text = ''
        self.author = ''
        self.language = "en"
        self.__allowed_tags = ['b', 'strong', 'i', 'em', 'blockquote']

    def add_text(self, paragraph):
        text = self.extract_text_with_format(paragraph)

        if paragraph.name == 'h2':
            text = f'<h3>{text}</h3>'

        self.full_text += self.format_text(text)

    @staticmethod
    def format_text(text):
        new_text = str(text).replace('“', '"').replace('”', '"')
        new_text = re.sub(r'"([^"]+)"', r'<i>"\1"</i>', new_text)

        return new_text

    def extract_text_with_format(self, paragraph):
        result = ''

        for child in paragraph.children:
            if isinstance(child, NavigableString):
                result += str(child)
            elif child.name in self.__allowed_tags:
                inner = self.extract_text_with_format(child)
                result += f"<{child.name}>{inner}</{child.name}>"
            else:
                result += self.extract_text_with_format(child)

        return result

    def to_dict(self):
        return {
            'article_id': str(self.article_id),
            'source_id': self.source_id,
            'url': self.url,
            'published_at': self.published_at,
            'collected_at': self.collected_at,
            'title': self.title,
            'description': self.description,
            'full_text': self.full_text,
            'author': self.author,
            'language': self.language
        }
