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

- [ ] **Test the Full Pipeline:**
    - [ ] Run the `scrape_all_categories()` function and verify that articles from RSS feeds are being correctly added to the database.

## Priority 2: Content Extraction from Links

Once we have links from RSS feeds, we need a way to get the full article content.

- [ ] **Create a Generic Content Extractor:**
    - [ ] Develop a utility function that takes a URL and uses `requests` and `BeautifulSoup` to extract the main article title and body.
    - [ ] This will replace the current behavior of using the summary as the content.

## Priority 4: Systematic Feed Testing and Categorization

Our goal is to ensure all configured RSS feeds are working as expected and to categorize problematic ones.

- [ ] **Refactor Test Scripts:**
    - [ ] Modify individual category test scripts (e.g., `tests/test_ai_scrape.py`) to:
        - Focus on logging the success/failure of *each individual article's content extraction* from *each feed*.
        - Save the content of *all* successfully extracted articles to separate files for inspection (e.g., `ai_article_1.txt`).
- [ ] **Systematically Test Each Category:**
    - [ ] For each category (AI, Quantum Computing, Defence Tech, Space Tech, Renewable Energy, Cloud Computing, Cybersecurity, Start-ups, Tech News):
        - Run its dedicated test script.
        - Analyze the detailed logs for each feed.
        - Inspect the saved article files to verify content.
- [ ] **Categorize Feeds:** Based on testing, categorize each feed as:
    - **Working:** Successfully extracts content.
    - **Problematic (Access Issue):** Fails with 403 or similar access errors.
    - **Problematic (No Content/Empty Feed):** Feed is parsed but yields no entries or empty content.
    - **Outdated:** Feed provides entries, but content is old/irrelevant.
- [ ] **Update `config/settings.py`:** Remove problematic feeds and potentially search for better alternatives.

## Future Ideas (Post-MVP)

- [ ] **Implement article summarization:** Generate concise summaries from full article content.
- [ ] **YouTube Summarization:** Explore implementing the YouTube video summarization feature.
- [ ] **Email Newsletters:** Re-evaluate the email newsletter connector with strict security protocols.
