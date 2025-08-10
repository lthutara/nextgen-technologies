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

## Future Ideas (Post-MVP)

- [ ] **YouTube Summarization:** Explore implementing the YouTube video summarization feature.
- [ ] **Email Newsletters:** Re-evaluate the email newsletter connector with strict security protocols.
