from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from config.settings import settings

@dataclass
class ScrapedArticle:
    title: str
    content: str
    summary: str
    source_url: str
    source_name: str
    category: str
    published_date: Optional[datetime] = None

class BaseScraper(ABC):
    def __init__(self, source_name: str, category: str):
        self.source_name = source_name
        self.category = category
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def make_request(self, url: str, delay: bool = True) -> Optional[BeautifulSoup]:
        try:
            if delay:
                time.sleep(settings.REQUEST_DELAY)
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    @abstractmethod
    def get_article_links(self) -> List[str]:
        pass
    
    @abstractmethod
    def extract_article_data(self, article_url: str) -> Optional[ScrapedArticle]:
        pass
    
    def scrape_articles(self, max_articles: int = None) -> List[ScrapedArticle]:
        max_articles = max_articles or settings.MAX_ARTICLES_PER_SOURCE
        
        article_links = self.get_article_links()[:max_articles]
        articles = []
        
        for link in article_links:
            article_data = self.extract_article_data(link)
            if article_data:
                articles.append(article_data)
                
        return articles