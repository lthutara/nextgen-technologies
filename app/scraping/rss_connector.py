import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from app.scraping.base_scraper import ScrapedArticle

class RSSConnector:
    def __init__(self, category: str, rss_feeds: Dict[str, str]):
        self.category = category
        self.rss_feeds = rss_feeds

    def fetch_articles(self) -> List[ScrapedArticle]:
        articles = []
        for source_name, feed_url in self.rss_feeds.items():
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    published_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6])

                    article = ScrapedArticle(
                        title=entry.title,
                        content=entry.summary,  # Placeholder, will be replaced by content extractor
                        summary=entry.summary,
                        source_url=entry.link,
                        source_name=source_name,
                        category=self.category,
                        published_date=published_date
                    )
                    articles.append(article)
            except Exception as e:
                print(f"Error fetching RSS feed from {feed_url}: {e}")
        return articles