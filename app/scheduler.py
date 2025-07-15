from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.scraping.scraper_manager import ScraperManager
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArticleScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scraper_manager = ScraperManager()
        
    def scrape_job(self):
        """Scheduled job to scrape articles"""
        try:
            logger.info("Starting scheduled article scraping...")
            results = self.scraper_manager.scrape_all_categories()
            
            total_new = sum(result['total_new'] for result in results)
            logger.info(f"Scheduled scraping completed. {total_new} new articles found.")
            
            return results
        except Exception as e:
            logger.error(f"Error in scheduled scraping: {e}")
            return None
    
    def start(self):
        """Start the scheduler"""
        self.scheduler.add_job(
            func=self.scrape_job,
            trigger=IntervalTrigger(hours=settings.SCRAPING_INTERVAL_HOURS),
            id='scrape_articles',
            name='Scrape tech articles',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info(f"Scheduler started. Articles will be scraped every {settings.SCRAPING_INTERVAL_HOURS} hours.")
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
    
    def get_next_run_time(self):
        """Get the next scheduled run time"""
        job = self.scheduler.get_job('scrape_articles')
        return job.next_run_time if job else None