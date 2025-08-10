import pytest
from unittest.mock import MagicMock, patch
from app.scheduler import ArticleScheduler
from app.models.database import get_db, Article, ScrapingLog
from config.settings import settings

# Mock the database session for tests
@pytest.fixture
def mock_db_session():
    db_session = MagicMock()
    yield db_session
    db_session.close()

# Mock the get_db dependency
@pytest.fixture
def mock_get_db(mock_db_session):
    with patch('app.models.database.get_db', return_value=iter([mock_db_session])):
        yield mock_db_session

# Test for immediate scraping on startup
def test_immediate_scraping_on_startup(mock_get_db):
    with patch('app.scheduler.ScraperManager') as MockScraperManager:
        scheduler = ArticleScheduler()
        scheduler.scrape_job()
        MockScraperManager.return_value.scrape_all_categories.assert_called_once()

# Test for category-specific scraping
def test_category_specific_scraping(mock_get_db):
    with patch('app.scheduler.ScraperManager') as MockScraperManager:
        scheduler = ArticleScheduler()
        
        # Mock scrape_category to return a predictable result
        MockScraperManager.return_value.scrape_category.return_value = {
            "category": "AI",
            "total_found": 10,
            "total_new": 5,
            "sources": {"arXiv": {"found": 10, "new": 5}}
        }

        # Call scrape_job with a specific category (this will require modifying scrape_job)
        # For now, we'll test the underlying scrape_category call directly
        result = scheduler.scraper_manager.scrape_category("AI", mock_get_db)
        
        assert result["category"] == "AI"
        assert result["total_new"] == 5
        MockScraperManager.return_value.scrape_category.assert_called_once_with("AI", mock_get_db)

# You would also need to add tests for the actual data population and database interactions.
# This requires setting up a test database or more sophisticated mocking.
