import sys
import os
from sqlalchemy.orm import Session
from app.scraping.scraper_manager import ScraperManager
from app.models.database import get_db, create_tables, Article, ScrapingLog
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_space_tech_scrape():
    print("\n--- Running test scrape for category: Space Tech ---")
    
    create_tables()
    
    db: Session = next(get_db())
    scraper_manager = ScraperManager()
    
    try:
        results = scraper_manager.scrape_category("Space Tech", db)
        db.commit()
        print("\n--- Scrape Results ---")
        print(f"Category: {results['category']}")
        print(f"Total Found: {results['total_found']}")
        print(f"Total New: {results['total_new']}")
        print("Sources:")
        for source_name, data in results['sources'].items():
            print(f"  - {source_name}: Found={data['found']}, New={data['new']}, Error={data.get('error', 'None')}")
        
        print("\n--- Sample Articles (last 5 new) ---")
        articles = db.query(Article).filter(Article.category == "Space Tech").order_by(Article.scraped_date.desc()).limit(5).all()
        if articles:
            for article in articles:
                print(f"  Title: {article.title}")
                print(f"  Source URL: {article.source_url}")
                print(f"  Content (first 100 chars): {article.content[:100]}...")
                print("-" * 20)
        else:
            print("No articles found for this category.")
            
    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred during scrape: {e}")
    finally:
        db.close()
    
    print("--- Test scrape for Space Tech finished ---\n")

if __name__ == "__main__":
    test_space_tech_scrape()
