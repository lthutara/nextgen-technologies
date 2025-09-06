from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import Article, RawArticle, ScrapingLog, get_db
from .arxiv_scraper import ArxivScraper
from .rss_connector import RSSConnector
from config.settings import settings

class ScraperManager:
    def __init__(self):
        self.connectors = {
            "arXiv": ArxivScraper,
            "RSS": RSSConnector
        }

    def scrape_category(self, category: str, db: Session, rss_feeds_override: Optional[List[str]] = None) -> Dict:
        results = {
            "category": category,
            "total_found": 0,
            "total_new": 0,
            "sources": {}
        }

        connectors_to_use = settings.CATEGORY_CONNECTORS.get(category, [])

        for connector_name in connectors_to_use:
            source_name = connector_name
            log_entry = ScrapingLog(
                source_name=source_name,
                category=category,
                started_at=datetime.utcnow()
            )
            try:
                if connector_name == "RSS":
                    feeds_to_use = []
                    if rss_feeds_override is not None:
                        feeds_to_use = rss_feeds_override
                    elif category in settings.RSS_FEEDS:
                        feeds_to_use = settings.RSS_FEEDS[category]
                    
                    if not feeds_to_use:
                        log_entry.status = "skipped"
                        log_entry.error_message = "No RSS feeds configured for category."
                        log_entry.completed_at = datetime.utcnow()
                        db.add(log_entry)
                        continue # Skip to next connector if no feeds

                    connector = self.connectors["RSS"](category, feeds_to_use)
                    articles = connector.fetch_articles()
                elif connector_name == "arXiv":
                    # Ensure arXiv is only used for categories it's configured for
                    if category not in settings.ARXIV_CATEGORIES:
                        log_entry.status = "skipped"
                        log_entry.error_message = "arXiv not configured for this category."
                        log_entry.completed_at = datetime.utcnow()
                        db.add(log_entry)
                        continue # Skip to next connector if not configured

                    connector = self.connectors["arXiv"](category)
                    articles = connector.scrape_articles()
                else:
                    log_entry.status = "error"
                    log_entry.error_message = f"Unknown connector: {connector_name}"
                    log_entry.completed_at = datetime.utcnow()
                    db.add(log_entry)
                    continue # Skip to next connector if unknown

                new_articles = 0
                for article_data in articles:
                    # Check if raw article already exists
                    existing_raw_article = db.query(RawArticle).filter(
                        RawArticle.source_url == article_data.source_url
                    ).first()
                    
                    if not existing_raw_article:
                        raw_article = RawArticle(
                            title=article_data.title,
                            content=article_data.content,
                            summary=article_data.summary,
                            source_url=article_data.source_url,
                            source_name=article_data.source_name,
                            category=article_data.category,
                            published_date=article_data.published_date,
                            image_url=article_data.image_url
                        )
                        db.add(raw_article)
                        new_articles += 1
                
                log_entry.articles_found = len(articles)
                log_entry.articles_new = new_articles
                log_entry.status = "success"
                log_entry.completed_at = datetime.utcnow()
                
                results["sources"][source_name] = {
                    "found": len(articles),
                    "new": new_articles
                }
                results["total_found"] += len(articles)
                results["total_new"] += new_articles

            except Exception as e:
                log_entry.status = "error"
                log_entry.error_message = str(e)
                log_entry.completed_at = datetime.utcnow()
                print(f"Error scraping {source_name} for {category}: {e}")
                
                results["sources"][source_name] = {
                    "found": 0,
                    "new": 0,
                    "error": str(e)
                }
            
            db.add(log_entry)

        db.commit()
        return results

    def scrape_all_categories(self) -> List[Dict]:
        results = []
        db = next(get_db())
        
        try:
            for category in settings.TECH_CATEGORIES:
                category_result = self.scrape_category(category, db)
                results.append(category_result)
                print(f"Scraped {category}: {category_result['total_new']} new articles")
        finally:
            db.close()
        
        return results