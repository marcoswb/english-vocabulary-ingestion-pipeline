from src.scrapers.base import BaseScraper
from datetime import datetime, timedelta
from src.models.article import Article

class CBC:

    def __init__(self):
        self.__base_url = 'https://www.cbc.ca'
        self.__articles_titles = []

    def extract(self, max_articles=20):
        main_page = BaseScraper(f'{self.__base_url}/news')
        main_page.load_page()
        articles = []

        for item in main_page.get_itens('a.cardText'):
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

            article = Article('cbc')
            article.url = url

            article_page = BaseScraper(url)
            article_page.load_page()

            div_title = article_page.get_itens('h1.detailHeadline')
            if div_title:
                article.title = div_title[0].get_text(strip=True)
            else:
                continue

            if article.title in self.__articles_titles:
                continue

            divs_text = article_page.get_itens('.story > p, .story > h2')
            if not divs_text:
                continue

            div_byline_details = article_page.get_itens('.bylineDetails')
            if div_byline_details:
                for element in div_byline_details:
                    if 'Posted' in element.get_text():
                        article.published_at = format_time(element.get_text(strip=True))
                        break

            div_contribuitors = article_page.get_itens('.authorText')
            if div_contribuitors:
                contribuitors = ''
                for contributor in div_contribuitors:
                    contribuitors += contributor.get_text(strip=True) + ' '
                article.author = contribuitors

            for paragraph in divs_text:
                article.add_text(paragraph)

            articles.append(article.to_dict())
            self.__articles_titles.append(article.title)

            if len(articles) == max_articles:
                break

        return articles


def format_time(time_str):
    try:
        time_str = time_str.split('Posted: ')[1].strip()

        if 'AM' in time_str:
            time_str = time_str.split('AM')[0].strip() + ' AM'
        elif 'PM' in time_str:
            time_str = time_str.split('PM')[0].strip() + ' PM'

        datetime_obj = datetime.strptime(time_str, "%b %d, %Y %I:%M %p")
        return datetime_obj.isoformat(timespec='microseconds')
    except (ValueError, IndexError):
        return None
