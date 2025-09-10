# NextGen Technologies - TODO

This file outlines the development plan for our next session.

## Priority 1: Implement RSS-Based Content Sourcing

Our main goal is to build a robust and reliable content pipeline using RSS feeds.

- [ ] **Finalize `RSSConnector`:**
    - [ ] Create the `app/scraping/rss_connector.py` file.
    - [ ] Implement the logic to fetch and parse multiple RSS feeds using the `feedparser` library.

- [ ] **Update `requirements.txt`:**
    - [ ] Add `feedparser` to the list of dependencies.

- [ ] **Integrate into `ScraperManager`:**
    - [ ] Modify `app/scraping/scraper_manager.py` to use the new `RSSConnector`.
    - [ ] Update the logic to allow different connectors (RSS, arXiv) to be used for different categories.

- [ ] **Curate RSS Feeds:**
    - [ ] Research and add more high-quality RSS feeds for all technology categories defined in `config/settings.py`.
    - [ ] Investigate and debug 'Cybersecurity' RSS feeds.

- [ ] **Test the Full Pipeline:**
    - [ ] Run the `scrape_all_categories()` function and verify that articles from RSS feeds are being correctly added to the database.

## Priority 2: Content Extraction from Links

Once we have links from RSS feeds, we need a way to get the full article content.

- [ ] **Create a Generic Content Extractor:**
    - [ ] Develop a utility function that takes a URL and uses `requests` and `BeautifulSoup` to extract the main article title and body.
    - [ ] This will replace the current behavior of using the summary as the content.

## Testing Strategy

- [ ] **Strengthen Unit Tests:** Refactor existing scraper tests to be true unit tests that use mock data (local files) instead of live network calls.
- [ ] **Implement API Integration Tests:** This is a high priority. Create a new `tests/test_api.py` file to test the API endpoints using FastAPI's `TestClient` and a temporary in-memory database.
- [ ] **Develop End-to-End (E2E) Tests:** As a future goal, create a few critical E2E tests for key user journeys (e.g., approving an article and seeing it on the homepage) using a tool like Selenium or Playwright.

## Architectural Roadmap

- [ ] **Implement a Two-Stage Content Pipeline:** Decouple scraping from curation for better quality control and resource management.
    - [ ] **Database:** Create a new `raw_articles` table to serve as a staging area for all incoming content.
    - [ ] **Connectors:** Modify all existing data sources (RSS, arXiv) to save their findings to the `raw_articles` table.
    - [ ] **Curation UI:** Build a new admin interface to review, filter, and select content from the `raw_articles` table.
    - [ ] **Promotion Logic:** Implement the functionality to "promote" a curated raw article to the main, user-facing `articles` table.

- [ ] **Refactor to a Unified Connectors Architecture:** Reorganize the data acquisition modules for better scalability and clarity.
    - [ ] **Create `app/connectors/` directory:** This will be the new home for all data source modules.
    - [ ] **Relocate Existing Sources:** Move the current scraping logic into `app/connectors/scraping/`.
    - [ ] **Rename Manager:** Rename `ScraperManager` to a more generic `ConnectorManager` and place it in `app/connectors/`.
    - [ ] **Establish a "Bypass" for Trusted Sources:** The manager should allow specific, high-quality connectors (e.g., a research project) to write directly to the main `articles` table, bypassing the `raw_articles` staging area.

## Future Ideas (Post-MVP)

- [ ] **Implement Admin Review Workflow:** Add a human-in-the-loop process for content approval.
    - [ ] **Database:** Add a `status` column to the `Article` model (e.g., `pending_review`, `approved`, `rejected`).
    - [ ] **Scraper:** Ensure new articles are saved with the `pending_review` status by default.
    - [ ] **User API:** Update all user-facing queries to only `filter` for articles with `status == 'approved'`.
    - [x] **Admin UI:** Create a new `/admin` page to list all articles pending review. (Note: A simple version for triggering scrapes has been created. The full review UI is at `/curation`.)
    - [ ] **Admin API:** Create new endpoints to `approve` or `reject` articles, which will update their status in the database.
- [ ] **Implement article summarization:** Generate concise summaries from full article content.
- [ ] **YouTube Summarization:** Explore implementing the YouTube video summarization feature.
- [ ] **Email Newsletters:** Re-evaluate the email newsletter connector with strict security protocols.
- [ ] **Rename Category:** Change "Renewable Energy" to "EV and Renewable Energy" across the application (config, scrapers, templates).
- [ ] **Content Differentiation:** Implement a mechanism to classify articles by type (e.g., 'in-depth article', 'news brief', 'research paper').

## UI/UX Enhancements

- [ ] **Improve Overall Color Theme:** Refine the website's color palette for a more cohesive and visually appealing experience.
- [ ] **Add Images to Articles:** Integrate relevant images within article content to enhance visual engagement.
- [ ] **Hero Section Image Sourcing:** Implement logic to display a category-specific stock image (or a general stock image) in the hero section, instead of relying on images extracted from the latest article.

## New Priority Items (from user)

- [ ] **Improve Curation Pipeline for Derived Content:**
    - [ ] Re-create new articles from derived content, avoiding original terminology.
    - [ ] Primary focus on Telugu version first.
    - [ ] Add translation to the curation pipeline.
- [ ] **Add More Connectors:**
    - [ ] YouTube summary (content simplification with idea and key points).
    - [ ] Research-type articles connector.
    - [ ] "How it works" articles connector.
    - [ ] Founder stories connector.