import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_article_content(url: str) -> str:
    """
    Fetches the content from a URL and extracts the main article text.
    It specifically handles pages that might have multiple 'rich-text' divs and concatenates them.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Strategy 1: Find all 'rich-text' divs and combine them (for Google Research Blog)
        rich_text_divs = soup.find_all('div', class_='rich-text')
        if rich_text_divs:
            all_paragraphs = []
            for div in rich_text_divs:
                paragraphs = div.find_all('p')
                all_paragraphs.extend([p.get_text(strip=True) for p in paragraphs])
            full_text = '\n'.join(all_paragraphs)
            logger.info(f"Successfully extracted content using 'rich-text' strategy from {url}. Length: {len(full_text)} chars.")
            return full_text

        # Strategy 2: Fallback to finding a single main content container
        container = (soup.find('article') or
                     soup.find('main') or
                     soup.find('div', id='main-content') or
                     soup.find('div', class_='post-content') or
                     soup.find('div', class_='article-body') or
                     soup.find('div', id='content'))

        if container:
            paragraphs = container.find_all('p')
            full_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
            logger.info(f"Successfully extracted content using fallback strategy from {url}. Length: {len(full_text)} chars.")
            return full_text

        # Strategy 3: If no specific container is found, use the whole body
        logger.warning(f"Could not find a specific content container for {url}. Falling back to body.")
        paragraphs = soup.body.find_all('p')
        full_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        logger.info(f"Successfully extracted content from body of {url}. Length: {len(full_text)} chars.")
        return full_text

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return ""
    except Exception as e:
        logger.error(f"An error occurred during content extraction for {url}: {e}")
        return ""