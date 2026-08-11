from src.scrapers.base import BaseScraper
from datetime import datetime, timedelta
from src.models.article import Article

class BBC:

    def __init__(self):
        self.__base_url = 'https://www.bbc.com'
        self.__articles_titles = []
        self.__main_page = BaseScraper(self.__base_url)

    def _get_articles_to_extract(self):
        self.__main_page.load_page()
        return self.__main_page.get_itens('a.Anchor-styles__AnchorStyled-sc-651d33db-0')

    def _get_link_from_item(self, item):
        link = str(item['href'])
        if self.__main_page.is_link(link):
            if link.startswith(self.__base_url):
                check_url = link.replace(self.__base_url, '')
                if not self.__main_page.is_internal_link(check_url):
                    return None

            return str(link)
        elif self.__main_page.is_internal_link(link):
            return f'{self.__base_url}{link}'

        return None

    @staticmethod
    def _get_title_article(article_page):
        div_title = article_page.get_itens('[data-component="headline-block"]')
        if div_title:
            return div_title[0].get_text(strip=True)

        return None

    @staticmethod
    def _get_divs_text(article_page):
        return article_page.get_itens('[data-component="text-block"] p, [data-component="subheadline-block"] h2')

    @staticmethod
    def _get_time_published_article(article_page):
        div_time_published = article_page.get_itens('.Byline-styles__TimeContainerStyled-sc-66f6383-2 hcsYRh')
        if div_time_published:
            return format_time(div_time_published[0].get_text(strip=True))

        return None

    @staticmethod
    def _get_contribuitors_article(article_page):
        div_contribuitors = article_page.get_itens('.Byline-styles__AuthorNameStyled-sc-66f6383-8')
        if div_contribuitors:
            contribuitors = ''
            for contributor in div_contribuitors:
                contribuitors += contributor.get_text(strip=True) + ' '
            return contribuitors

        return None

    def extract(self):
        extracted_articles = self._get_articles_to_extract()

        articles = []
        for item in extracted_articles:
            url = self._get_link_from_item(item)

            if not url or not url.startswith(self.__base_url):
                continue

            article_page = BaseScraper(url)
            article_page.load_page()

            article = Article('bbc')
            article.url = url
            article.published_at = self._get_time_published_article(article_page)
            article.author = self._get_contribuitors_article(article_page)

            article.title = self._get_title_article(article_page)
            if not article.title or article.title in self.__articles_titles:
                continue

            divs_text = self._get_divs_text(article_page)
            if not divs_text:
                continue

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
