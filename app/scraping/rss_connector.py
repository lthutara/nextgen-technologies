from typing import List, Optional
from time import mktime
from datetime import datetime
import feedparser
from app.scraping.base_scraper import BaseScraper, ScrapedArticle
from config.settings import settings

class RSSConnector(BaseScraper):
    def __init__(self, category: str, rss_feeds: List[str]):
        super().__init__("RSS", category)
        self.rss_feeds = rss_feeds

    def fetch_articles(self, max_articles: int = None) -> List[ScrapedArticle]:
        limit = max_articles or settings.MAX_ARTICLES_PER_SOURCE
        # Ensure we fetch at least 1 article per feed to avoid 0 if limit < num_feeds
        max_articles_per_feed = max(1, limit // len(self.rss_feeds))
        articles = []

        for feed_url in self.rss_feeds:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:max_articles_per_feed]:
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime.fromtimestamp(mktime(entry.published_parsed))

                article = ScrapedArticle(
                    title=entry.title,
                    content=entry.get('summary', ''),  # Using summary as content for now
                    summary=entry.get('summary', ''),
                    source_url=entry.link,
                    source_name=self.source_name,
                    category=self.category,
                    published_date=published_date
                )
                articles.append(article)
        return articles

    def get_article_links(self) -> List[str]:
        # Not needed for RSS feeds as we get all data at once
        return []

    def extract_article_data(self, article_url: str) -> Optional[ScrapedArticle]:
        # Not needed for RSS feeds as we get all data at once
        return None
