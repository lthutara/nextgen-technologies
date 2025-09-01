import pytest
from pathlib import Path
from app.scraping.rss_connector import RSSConnector
from unittest.mock import patch, Mock
from app.scraping.arxiv_scraper import ArxivScraper

def test_rss_connector_parsing():
    """
    Tests that the RSSConnector can correctly parse a local mock RSS feed,
    including handling entries with missing summaries.
    """
    # Construct the path to the mock file
    mock_file_path = Path(__file__).parent / "mock_data/mock_rss_feed.xml"
    
    # Instantiate the connector with the local file path
    # feedparser can handle file paths directly
    connector = RSSConnector(category="Test", rss_feeds=[str(mock_file_path)])
    
    # Fetch articles
    articles = connector.fetch_articles()
    
    # 1. Assert that both articles were parsed
    assert len(articles) == 2
    
    # Find the articles in the list (order isn't guaranteed)
    article1 = next((a for a in articles if a.title == "Test Article 1"), None)
    article2 = next((a for a in articles if a.title == "Test Article 2 (No Summary)"), None)
    
    assert article1 is not None
    assert article2 is not None

    # 2. Assert that the complete article was parsed correctly
    assert article1.title == "Test Article 1"
    assert article1.summary == "This is the summary for test article 1."
    assert article1.content == "This is the summary for test article 1."
    assert article1.source_url == "http://example.com/article1"
    
    # 3. Assert that the article with the missing summary was handled correctly
    assert article2.title == "Test Article 2 (No Summary)"
    assert article2.summary == ""
    assert article2.content == ""
    assert article2.source_url == "http://example.com/article2"

def test_arxiv_scraper_parsing():
    """
    Tests that the ArxivScraper can correctly parse a local mock XML file.
    """
    # Read the mock XML data
    mock_file_path = Path(__file__).parent / "mock_data/mock_arxiv_response.xml"
    with open(mock_file_path, 'r') as f:
        mock_xml_content = f.read()

    # Mock the response from requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = mock_xml_content.encode('utf-8') # Encode to bytes
    mock_response.raise_for_status = Mock()

    # Use patch to replace requests.get
    with patch('app.scraping.arxiv_scraper.requests.get', return_value=mock_response) as mock_get:
        # Instantiate the scraper
        scraper = ArxivScraper(category="AI")
        
        # Scrape articles
        articles = scraper.scrape_articles()
        
        # 1. Assert that the mock API was called correctly
        mock_get.assert_called_once()
        
        # 2. Assert that both articles were parsed
        assert len(articles) == 2
        
        # 3. Assert that the articles were parsed correctly
        article1 = articles[0]
        assert article1.title == "Test Arxiv Article 1"
        assert article1.summary == "This is the summary for test arxiv article 1. It is a great paper."
        assert article1.source_url == "http://arxiv.org/abs/2308.08888"
        
        article2 = articles[1]
        assert article2.title == "Test Arxiv Article 2"
        assert article2.summary == "This is the summary for test arxiv article 2. It is also a great paper."
        assert article2.source_url == "http://arxiv.org/abs/2308.09999"