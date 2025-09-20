# NextGen Technologies - TODO

This file outlines the development plan for our next session.

## Priority 1: Implement RSS-Based Content Sourcing

Our main goal is to build a robust and reliable content pipeline using RSS feeds.


- [x] **Update `requirements.txt`:**
    - [x] Add `feedparser` to the list of dependencies.

- [ ] **Curate RSS Feeds:**
    - [ ] Research and add more high-quality RSS feeds for all technology categories defined in `config/settings.py`.
    - [ ] Investigate and debug 'Cybersecurity' RSS feeds.
    - [ ] **Note:** The 'Cybersecurity' RSS feeds might be failing because one or more of the URLs are invalid or unreachable. This could be causing the entire category to fail during scraping. The feeds need to be individually tested to identify the problematic source.


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
- [ ] **FIX: Images Not Loading on Homepage:** Despite replacing placeholder `.jpg`s with `.png`s and updating template paths, images are not loading. This is likely a server-side caching issue with Uvicorn or a static file serving problem. We need to ensure images load correctly for both scraped and manually added articles.

## New Priority Items (from user)

- [x] **Implement new curation stage for Content Preparation**
    - [x] Initial UI for 'Process' page with editable title, article type selection, and dynamic Content Structuring sections.
    - [x] AI Content Structuring endpoint (using summarization as placeholder) and save Content Structuring endpoint implemented.
    - [x] Database schema updated (RawArticle status, ArticleSection model) and migrations applied.
    - [ ] **Known Issues on /curation/process/{article_id} page:**
        - Jinja2 TemplateSyntaxError (resolved by overwriting file, but needs re-verification).
        - Original content not displayed (replaced with link).
        - AI-generated summary displayed in main Content Structuring section (as intended, but needs further refinement to extract specific sections).
        - 'Save Content Structuring' button feedback needs improvement (temporary text change implemented, needs verification).
- [ ] **Improve Curation Pipeline for Derived Content:**
    - [ ] Re-create new articles from derived content, avoiding original terminology.
    - [ ] Primary focus on Telugu version first.
    - [ ] Add translation to the curation pipeline.
- [ ] **Add More Connectors:**
    - [ ] YouTube summary (content simplification with idea and key points).
    - [ ] Research-type articles connector.
    - [ ] "How it works" articles connector.
    - [ ] Founder stories connector.
