from src.scrapers.base import BaseScraper
from datetime import datetime, timedelta
from src.models.article import Article

class TheGuardian:

    def __init__(self):
        self.__base_url = 'https://www.theguardian.com'
        self.__articles_titles = []

    def extract(self):
        main_page = BaseScraper(f'{self.__base_url}/international')
        main_page.load_page()
        articles = []

        for item in main_page.get_itens('a.dcr-idxb0f'):
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

            if not url.startswith(f'{self.__base_url}/world/'):
                continue

            article = Article('the_guardian')
            article.url = url

            article_page = BaseScraper(url)
            article_page.load_page()

            div_title = article_page.get_itens('h1.dcr-l0wuod')
            if div_title:
                article.title = div_title[0].get_text(strip=True)
            else:
                continue

            if article.title in self.__articles_titles:
                continue

            divs_text = article_page.get_itens('p.dcr-1s160rg')
            if not divs_text:
                continue

            div_time_published = article_page.get_itens('.dcr-10i63lj')
            if div_time_published:
                article.published_at = format_time(div_time_published[0].get_text(strip=True))

            div_contribuitors = article_page.get_itens('.dcr-15wyqgv')
            if div_contribuitors:
                contribuitors = ''
                for contributor_div in div_contribuitors:
                    author_links = contributor_div.find_all('a', attrs={'rel': 'author'})
                    for link in author_links:
                        contribuitors += link.get_text(strip=True) + ' '
                article.author = contribuitors.strip()

            for paragraph in divs_text:
                article.add_text(paragraph)

            articles.append(article.to_dict())
            self.__articles_titles.append(article.title)

            if len(articles) == BaseScraper.MAX_ARTICLES:
                break

        return articles


def format_time(time_str):
    try:
        dt = datetime.strptime(time_str, '%a %d %b %Y %H.%M %Z')
        return dt.isoformat(timespec='microseconds')
    except ValueError:
        return None
