from src.scrapers.base import BaseScraper
from src.models.article import Article
from src.utils.functions import format_time

class BBC:

    def __init__(self):
        self.__base_url = 'https://www.bbc.com'
        self.__articles_titles = []

    def extract(self, max_articles=5):
        main_page = BaseScraper(self.__base_url)
        main_page.load_page()
        articles = []

        for item in main_page.get_itens('a.sc-8a623a54-0'):
            link = str(item['href'])
            if main_page.is_link(link):
                if link.startswith(self.__base_url):
                    check_url = link.replace(self.__base_url, '')
                    if not main_page.is_internal_link(check_url):
                        continue

                url = str(link)
            elif main_page.is_internal_link(link):
                url = f'{self.__base_url}{link}'
            else:
                continue

            if not url.startswith(self.__base_url):
                continue

            article = Article('bbc')
            article.url = url

            article_page = BaseScraper(url)
            article_page.load_page()

            div_title = article_page.get_itens('[data-component="headline-block"]')
            if div_title:
                article.title = div_title[0].get_text(strip=True)
            else:
                continue

            if article.title in self.__articles_titles:
                continue

            divs_text = article_page.get_itens('[data-component="text-block"] p, [data-component="subheadline-block"] h2')
            if not divs_text:
                continue

            div_time_published = article_page.get_itens('.sc-3adb3607-2')
            if div_time_published:
                article.published_at = format_time(div_time_published[0].get_text(strip=True))

            div_contribuitors = article_page.get_itens('.sc-3adb3607-8')
            if div_contribuitors:
                contribuitors = ''
                for contributor in div_contribuitors:
                    print(contributor)
                    contribuitors += contributor.get_text(strip=True) + ' '
                article.author = contribuitors

            for paragraph in divs_text:
                article.add_text(paragraph)

            articles.append(article.to_dict())
            self.__articles_titles.append(article.title)

            if len(articles) == max_articles:
                break

        return articles
