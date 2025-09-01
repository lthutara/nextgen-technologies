from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./nextgen_tech.db"
    
    # Application
    APP_NAME: str = "NextGen Technologies Portal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Scraping
    SCRAPING_INTERVAL_HOURS: int = 0.01 
    MAX_ARTICLES_PER_SOURCE: int = 10
    REQUEST_DELAY: float = 1.0
    
    # Categories
    TECH_CATEGORIES: list = [
        "AI",
        "Quantum Computing", 
        "Defence Tech",
        "Space Tech",
        "Renewable Energy",
        "Cloud Computing",
        "Cybersecurity",
        "Start-ups",
        "Tech News"
    ]

    ARXIV_CATEGORIES: list = [
        "AI",
        "Quantum Computing"
    ]

    CATEGORY_CONNECTORS: dict = {
        "AI": ["RSS", "arXiv"],
        "Quantum Computing": ["RSS", "arXiv"],
        "Defence Tech": ["RSS"],
        "Space Tech": ["RSS"],
        "Renewable Energy": ["RSS"],
        "Cloud Computing": ["RSS"],
        "Cybersecurity": ["RSS"],
        "Start-ups": ["RSS"],
        "Tech News": ["RSS"]
    }

    RSS_FEEDS: dict = {
        "AI": [
            "https://research.google/blog/rss",
            "https://news.microsoft.com/source/topics/ai/feed/",
            "https://bair.berkeley.edu/blog/feed.xml"
        ],
        "Quantum Computing": [
            "https://quantumcomputingreport.com/feed/",
            "https://www.sciencedaily.com/rss/computers_math/quantum_computers.xml",
            "https://thequantuminsider.com/feed/",
            "https://www.insidehpc.com/tag/quantum-computing/feed/"
        ],
        "Defence Tech": [
            "http://defence-blog.com/feed",
            "https://www.defenseone.com/rss/all/",
            "https://breakingdefense.com/feed/",
            "https://www.army-technology.com/feed/",
            "https://www.airforce-technology.com/feed/",
            "https://www.naval-technology.com/feed/"
        ],
        "Space Tech": [
            "https://www.nasa.gov/news/feed/",
            "https://www.esa.int/rss/ESA_News",
            "https://www.space.com/feeds/news",
            "https://spacenews.com/feed/",
            "https://www.universetoday.com/feed/"
        ],
        "Renewable Energy": [
            "https://www.renewableenergyworld.com/feed/",
            "https://cleantechnica.com/feed/",
            "https://www.alternative-energy-news.info/feed/",
            "https://www.rechargenews.com/rss",
            "https://www.theguardian.com/environment/renewableenergy/rss"
        ],
        "Cloud Computing": [
            "https://www.cloudtech.com/feed/",
            "https://www.cioreview.com/rss/category/cloud-computing.xml",
            "https://www.techrepublic.com/rssfeeds/topic/cloud-computing/",
            "https://www.cloudtweaks.com/feed/",
            "https://www.computerworld.com/category/cloud-computing/index.rss",
            "https://www.theregister.com/headlines.atom",
            "https://www.zdnet.com/topic/cloud/rss.xml",
            "https://www.infoq.com/cloud-computing/feed/rss/"
        ],
        "Cybersecurity": [
            "https://thehackernews.com/feeds/posts/default",
            "https://krebsonsecurity.com/feed/",
            "https://www.darkreading.com/rss_simple.asp",
            "https://grahamcluley.com/feed/",
            "https://schneier.com/blog/atom.xml",
            "https://isc.sans.edu/rssfeed.html",
            "https://www.csoonline.com/feed",
            "https://www.bleepingcomputer.com/feed/",
            "https://www.crowdstrike.com/blog/feed/",
            "https://www.paloaltonetworks.com/blog/feed/",
            "https://www.mandiant.com/resources/blog/rss.xml",
            "https://crypto.stanford.edu/rss.xml"
        ],
        "Start-ups": [
            "http://techcrunch.com/startups/feed/",
            "http://feeds.feedburner.com/venturebeat/",
            "https://www.wired.com/feed/rss",
            "https://producthunt.com/feed",
            "https://news.ycombinator.com/rss"
        ],
        "Tech News": [
            "http://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss",
            "http://www.theverge.com/rss/index.xml",
            "http://feeds.arstechnica.com/arstechnica/index/",
            "https://www.engadget.com/rss.xml",
            "https://www.cnet.com/rss/news/",
            "https://www.techradar.com/rss"
        ]
    }
    
    class Config:
        env_file = ".env"

settings = Settings()
