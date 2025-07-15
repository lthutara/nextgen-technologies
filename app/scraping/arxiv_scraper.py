import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
from .base_scraper import BaseScraper, ScrapedArticle

class ArxivScraper(BaseScraper):
    def __init__(self, category: str):
        super().__init__("arXiv", category)
        self.base_url = "http://export.arxiv.org/api/query"
        self.category_map = {
            "AI": "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL",
            "Quantum Computing": "cat:quant-ph",
            "Defence Tech": "cat:cs.CR+OR+cat:cs.CY",
            "Space Tech": "cat:astro-ph+OR+cat:physics.space-ph",
            "Renewable Energy": "cat:physics.soc-ph+OR+cat:cond-mat.mtrl-sci"
        }
    
    def get_article_links(self) -> List[str]:
        search_query = self.category_map.get(self.category, "cat:cs.AI")
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': 50,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            links = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                if id_elem is not None:
                    links.append(id_elem.text)
            
            return links
        except Exception as e:
            print(f"Error fetching arXiv links: {e}")
            return []
    
    def extract_article_data(self, article_url: str) -> Optional[ScrapedArticle]:
        try:
            # Extract arXiv ID from URL
            arxiv_id = article_url.split('/')[-1]
            
            # Get article details from API
            params = {
                'search_query': f'id:{arxiv_id}',
                'start': 0,
                'max_results': 1
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            entry = root.find('{http://www.w3.org/2005/Atom}entry')
            
            if entry is None:
                return None
            
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            
            published_date = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ')
            
            # Get full text URL
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            return ScrapedArticle(
                title=title,
                content=summary,  # For now, using summary as content
                summary=summary[:200] + "..." if len(summary) > 200 else summary,
                source_url=article_url,
                source_name=self.source_name,
                category=self.category,
                published_date=published_date
            )
            
        except Exception as e:
            print(f"Error extracting arXiv article {article_url}: {e}")
            return None