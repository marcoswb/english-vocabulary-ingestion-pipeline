import requests
from bs4 import BeautifulSoup


class BaseScraper:

    def __init__(self, website_link):
        self.__website_link = website_link
        self.__soup_data = None

    def get_website_link(self):
        return self.__website_link

    def load_page(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.get_website_link(), headers=headers)
        self.__soup_data = BeautifulSoup(response.text, 'html.parser')

    def get_itens(self, select_item):
        try:
            return self.__soup_data.select(select_item)
        except:
            return []

    @staticmethod
    def is_link(str_link):
        if str(str_link).startswith('http'):
            return True

        return False

    @staticmethod
    def is_internal_link(str_link):
        if str(str_link).startswith('/') and str(str_link).count('/') > 1:
            return True

        return False
