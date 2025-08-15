import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def extract_article_content(url: str) -> tuple[str, str]:
    """
    Extracts the main title and body content from a given URL.
    """
    try:
        logger.info(f"Attempting to extract content from: {url}") # Added
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        logger.info(f"Successfully fetched {url}. Status: {response.status_code}") # Added
        soup = BeautifulSoup(response.text, 'html.parser')
        logger.info(f"Parsed HTML for {url}.") # Added

        title = soup.find('h1')
        if title:
            title = title.get_text(strip=True)
        else:
            title = soup.find('title')
            if title:
                title = title.get_text(strip=True)
            else:
                title = "No Title Found"

        # Attempt to find the main content based on common patterns
        # This is a simplified approach and might need refinement for specific sites
        content_tags = ['article', 'main', 'div', 'p']
        main_content = []
        
        for tag_name in content_tags:
            for tag in soup.find_all(tag_name):
                # Heuristic: Look for tags with significant text content
                text = tag.get_text(separator=' ', strip=True)
                if len(text.split()) > 50:  # Arbitrary threshold for "main content"
                    main_content.append(text)
            if main_content:
                break # Stop after finding some content

        if not main_content:
            # Fallback: get all paragraph text
            for p_tag in soup.find_all('p'):
                text = p_tag.get_text(separator=' ', strip=True)
                if text:
                    main_content.append(text)

        full_content = "\n\n".join(main_content)
        if not full_content:
            full_content = "Could not extract main content."

        return title, full_content

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return "Error fetching content", f"Failed to fetch content from {url}: {e}"
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {e}")
        return "Error extracting content", f"An unexpected error occurred: {e}"
