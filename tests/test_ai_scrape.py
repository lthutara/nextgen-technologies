import sys
import os
from sqlalchemy.orm import Session
from app.scraping.scraper_manager import ScraperManager
from app.models.database import get_db, create_tables, Article, ScrapingLog
from config.settings import settings # Added
import logging # Added

# Configure logging for the test script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Added

# Add the project root to the sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define AI RSS feeds directly for testing
AI_RSS_FEEDS = [
    "https://research.google/blog/rss",
    "https://blogs.nvidia.com/blog/category/ai/feed/",
    "https://news.microsoft.com/source/topics/ai/feed/",
    "https://bair.berkeley.edu/blog/feed.xml",
    "https://towardsdatascience.com/feed",
    "https://machinelearningmastery.com/blog/feed/"
]

def test_ai_scrape():
    print("\n--- Running test scrape for category: AI ---")
    
    # Ensure tables exist (for local SQLite testing)
    create_tables()
    
    db: Session = next(get_db())
    scraper_manager = ScraperManager()
    
    try:
        # Pass AI_RSS_FEEDS directly to scrape_category
        results = scraper_manager.scrape_category("AI", db, rss_feeds_override=AI_RSS_FEEDS)
        db.commit() # Commit changes to the database
        
        print("\n--- Scrape Results ---")
        print(f"Category: {results['category']}")
        print(f"Total Found: {results['total_found']}")
        print(f"Total New: {results['total_new']}")
        print("Sources:")
        for source_name, data in results['sources'].items():
            print(f"  - {source_name}: Found={data['found']}, New={data['new']}, Error={data.get('error', 'None')}")
        
        print("\n--- Verifying and Saving Articles ---")
        # Fetch all articles for the category to inspect
        all_articles = db.query(Article).filter(Article.category == "AI").order_by(Article.scraped_date.desc()).all()
        
        successful_articles_saved_count = 0
        for i, article in enumerate(all_articles):
            if "Error fetching content" not in article.content: # Check for successful content extraction
                print(f"  Processing article {i+1}: {article.title}")
                
                # Sanitize source_name for filename
                safe_source_name = "".join(c for c in article.source_name if c.isalnum() or c in (' ', '.', '_')).rstrip()
                file_name = f"ai_article_{successful_articles_saved_count + 1}_{safe_source_name}.txt"
                
                try:
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(f"Title: {article.title}\n")
                        f.write(f"Source URL: {article.source_url}\n\n")
                        f.write(article.content)
                    print(f"  Content saved to {file_name}")
                    successful_articles_saved_count += 1
                except Exception as file_e:
                    print(f"  Error saving article {article.title} to file: {file_e}")
            else:
                print(f"  Skipping article {i+1} due to content extraction error: {article.title}")
        
        if successful_articles_saved_count == 0:
            print("No successful articles found and saved for this category.")
            
    except Exception as e:
        db.rollback() # Rollback in case of error
        print(f"An unexpected error occurred during scrape: {e}")
    finally:
        db.close()
    
    print("--- Test scrape for AI finished ---\n")

if __name__ == "__main__":
    test_ai_scrape()
