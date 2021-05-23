from _datetime import datetime

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pymongo
from Article import Article

base_url = 'https://thehackernews.com/search/label/'
mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
hacker_news_db = mongo_client["hackernews"]
articles_collection = hacker_news_db["articles"]


categories = [{
    'name': 'Data Breach',
    'slug': 'data%20breach'
}, {
    'name': 'Cyber Attack',
    'slug': 'Cyber%20Attack'
}, {
    'name': 'Vulnerability',
    'slug': 'Vulnerability'
}, {
    'name': 'Malware',
    'slug': 'Malware'
}]
session = HTMLSession()


class ArticleScraper:
    category_url = ''
    category_name = ''
    category_slug = ''
    response = ''

    def __init__(self, category_url, category_slug, category_name):
        self.category_url = category_url
        self.category_name = category_name
        self.category_slug = category_slug
        self.response = session.get(self.category_url)

    def scrapeArticles(self):
        articles = self.response.html.find('.body-post')
        for post in articles:
            post_link = post.find('.story-link', first=True).attrs['href']
            post_title = post.find('.home-title', first=True).text
            post_image = post.find('.home-img-src', first=True).attrs['data-src']
            post_description = post.find('.home-desc', first=True).text
            article = Article(post_title, post_description, post_image, post_link, self.category_name, self.category_slug, datetime.today().strftime('%Y-%m-%d'))
            if not articles_collection.find({"title": post_title}).count() > 0:
                articles_collection.insert_one(article.__dict__)


def scrapeArticles():
    for category in categories:
        category_slug = category['slug']
        category_name = category['name']
        cateogry_scraper = ArticleScraper(f"{base_url}{category_slug}", category_slug, category_name)
        cateogry_scraper.scrapeArticles()


scrapeArticles()
