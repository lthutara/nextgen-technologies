import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_article_content(url: str) -> str:
    """
    Fetches the content from a URL and extracts the main article text.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Try to find the main <article> tag
        article_tag = soup.find('article')
        if article_tag:
            text_container = article_tag
        else:
            # 2. As a fallback, look for common main content divs
            main_content = (soup.find('main') or
                           soup.find('div', id='main-content') or
                           soup.find('div', class_='post-content') or
                           soup.find('div', class_='article-body') or
                           soup.find('div', id='content'))
            if main_content:
                text_container = main_content
            else:
                # 3. If all else fails, use the whole body
                text_container = soup.body

        if not text_container:
            logger.warning(f"Could not find a suitable text container for {url}")
            return ""

        # Extract text from all paragraph tags within the container
        paragraphs = text_container.find_all('p')
        full_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        logger.info(f"Successfully extracted content from {url}. Length: {len(full_text)} chars.")
        return full_text

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return ""
    except Exception as e:
        logger.error(f"An error occurred during content extraction for {url}: {e}")
        return ""