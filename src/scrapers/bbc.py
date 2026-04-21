from src.scrapers.base import BaseScraper
from datetime import datetime, timedelta
from src.models.article import Article

class BBC:

    def __init__(self):
        self.__base_url = 'https://www.bbc.com'
        self.__articles_titles = []

    def extract(self):
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
                    contribuitors += contributor.get_text(strip=True) + ' '
                article.author = contribuitors

            for paragraph in divs_text:
                article.add_text(paragraph)

            articles.append(article.to_dict())
            self.__articles_titles.append(article.title)

            if len(articles) == BaseScraper.MAX_ARTICLES:
                break

        return articles


def format_time(time_str):
    try:
        if 'ago' in time_str:
            time_str = time_str.replace(' ago', '')

            if 'minute' in time_str:
                minutes = int(time_str.replace(' minutes', '').replace(' minute', ''))
                dt = datetime.now() - timedelta(minutes=minutes)
            elif 'hour' in time_str:
                hours = int(time_str.replace(' hours', '').replace(' hour', ''))
                dt = datetime.now() - timedelta(hours=hours)
            elif 'day' in time_str:
                days = int(time_str.replace(' days', '').replace(' day', ''))
                dt = datetime.now() - timedelta(days=days)
            else:
                return None

            return dt.isoformat()

        return None
    except ValueError:
        return None
