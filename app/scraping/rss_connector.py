import feedparser
from typing import List, Dict, Optional
from datetime import datetime
from app.scraping.base_scraper import ScrapedArticle
from app.scraping.content_extractor import extract_article_content
import urllib.parse
import logging

logger = logging.getLogger(__name__)

class RSSConnector:
    def __init__(self, category: str, rss_feeds: List[str]):
        self.category = category
        self.rss_feeds = rss_feeds
        logger.info(f"Initialized RSSConnector for category {category} with {len(rss_feeds)} feeds.")

    def fetch_articles(self) -> List[ScrapedArticle]:
        articles = []
        for feed_url in self.rss_feeds:
            logger.info(f"Fetching feed from: {feed_url}")
            try:
                feed = feedparser.parse(feed_url)
                logger.info(f"Feed {feed_url} parsed. Found {len(feed.entries)} entries.")
                # Derive source_name from the feed_url's domain
                parsed_url = urllib.parse.urlparse(feed_url)
                source_name = parsed_url.netloc.replace('www.', '').split('.')[0].capitalize()

                for entry in feed.entries:
                    published_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6])

                    logger.info(f"Processing entry: {entry.title} from {entry.link}")
                    # Extract full content using the new utility
                    full_title, full_content = extract_article_content(entry.link)
                    logger.info(f"Content extraction for {entry.link} returned title: {full_title[:50]}... and content length: {len(full_content)}")

                    # Use the extracted full_title if available, otherwise fallback to entry.title
                    final_title = full_title if full_title and full_title != "No Title Found" else entry.title
                    
                    article = ScrapedArticle(
                        title=final_title,
                        content=full_content,
                        summary=entry.summary,
                        source_url=entry.link,
                        source_name=source_name,
                        category=self.category,
                        published_date=published_date
                    )
                    articles.append(article)
            except Exception as e:
                logger.error(f"Error fetching RSS feed from {feed_url}: {e}")
        logger.info(f"Finished fetching articles for category {self.category}. Total articles collected: {len(articles)}")
        return articles