import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from .base_scraper import BaseScraper, ScrapedArticle

class ArxivScraper(BaseScraper):
    def __init__(self, category: str):
        super().__init__("arXiv", category)
        self.base_url = "http://export.arxiv.org/api/query"
        self.category_map = {
            "AI": "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL",
            "Quantum Computing": "cat:quant-ph",
        }

    def get_article_links(self) -> List[str]:
        pass

    def extract_article_data(self, article_url: str):
        pass

    def scrape_articles(self, max_articles: int = 50) -> List[ScrapedArticle]:
        search_query = self.category_map.get(self.category)
        if not search_query:
            return []

        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_articles,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            namespace = '{http://www.w3.org/2005/Atom}'
            articles = []

            for entry in root.findall(f'{namespace}entry'):
                summary = entry.find(f'{namespace}summary').text.strip()
                article = ScrapedArticle(
                    title=entry.find(f'{namespace}title').text.strip(),
                    content=summary,
                    summary=summary[:200] + "..." if len(summary) > 200 else summary,
                    source_url=entry.find(f'{namespace}id').text.strip(),
                    source_name=self.source_name,
                    category=self.category,
                    published_date=datetime.strptime(entry.find(f'{namespace}published').text, '%Y-%m-%dT%H:%M:%SZ')
                )
                articles.append(article)
            
            return articles
        except requests.exceptions.RequestException as e:
            print(f"Error fetching arXiv data for {self.category}: {e}")
            return []
        except ET.ParseError as e:
            print(f"Error parsing arXiv XML for {self.category}: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred in ArxivScraper for {self.category}: {e}")
            return []
