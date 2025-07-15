# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NextGen Technologies Portal is a Python-based web application that aggregates and displays the latest technological advances from research papers and tech news sources. The application focuses on five key areas: AI, Quantum Computing, Defence Tech, Space Tech, and Renewable Energy.

## Architecture

**Tech Stack:**
- Backend: FastAPI with SQLAlchemy ORM
- Database: PostgreSQL 
- Web Scraping: BeautifulSoup4, Scrapy, Selenium
- Frontend: HTML/CSS/JavaScript with Bootstrap 5
- Scheduler: APScheduler for automated data collection
- Future: Python-babel for internationalization (Telugu translation planned)

**Key Components:**
- `app/scraping/`: Web scraping modules with base scraper class and source-specific scrapers
- `app/models/`: Database models for articles and scraping logs
- `app/api/`: FastAPI routes and web interface
- `app/templates/`: Jinja2 HTML templates
- `app/scheduler.py`: Automated scraping scheduler
- `config/settings.py`: Centralized configuration management

## Common Development Commands

**Setup and Installation:**
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run the application
python run.py
```

**Database Operations:**
```bash
# The application automatically creates tables on startup
# Database models are in app/models/database.py
```

**Testing Scraping:**
```bash
# Test scraping via API endpoints
curl -X POST "http://localhost:8000/api/scrape"
curl -X POST "http://localhost:8000/api/scrape?category=AI"
```

**Development Server:**
```bash
# Run with auto-reload
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Key Features

- **Web Scraping**: Automated collection from arXiv and other research sources
- **Categorization**: Articles organized by technology domains
- **Scheduled Updates**: Background scraping every 24 hours (configurable)
- **REST API**: JSON endpoints for articles and scraping logs
- **Web Interface**: Clean, responsive UI with category filtering
- **Duplicate Prevention**: URL-based deduplication of articles

## Adding New Scrapers

1. Create new scraper class inheriting from `BaseScraper` in `app/scraping/`
2. Implement `get_article_links()` and `extract_article_data()` methods
3. Add scraper to `ScraperManager` in `app/scraping/scraper_manager.py`
4. Update category mapping in scraper if needed

## Database Schema

**Articles Table:**
- id, title, content, summary, source_url, source_name
- category, published_date, scraped_date, is_active

**Scraping Logs Table:**
- id, source_name, category, articles_found, articles_new
- status, error_message, started_at, completed_at

## Configuration

Key settings in `config/settings.py`:
- `SCRAPING_INTERVAL_HOURS`: Frequency of automated scraping
- `MAX_ARTICLES_PER_SOURCE`: Limit per scraping run
- `TECH_CATEGORIES`: List of technology categories
- `DATABASE_URL`: PostgreSQL connection string

## API Endpoints

- `GET /`: Main web interface
- `GET /category/{category}`: Category-specific view
- `GET /api/articles`: JSON API for articles
- `POST /api/scrape`: Trigger manual scraping
- `GET /api/logs`: View scraping logs

## Future Enhancements

- User authentication system
- Bookmarking functionality
- Advanced search and filtering
- Telugu language translation using Python-babel
- Additional scraping sources (IEEE, Nature, etc.)
- Admin panel for content management