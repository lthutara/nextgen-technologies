import urllib.parse
from pydantic_settings import BaseSettings
from typing import Optional

def google_news_url(keyword):
    encoded = urllib.parse.quote(keyword)
    return f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./nextgen_tech.db"
    
    # Application
    APP_NAME: str = "NextGen Technologies Portal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    GEMINI_API_KEY: Optional[str] = None
    
    # Scraping
    SCRAPING_INTERVAL_HOURS: int = 1 
    MAX_ARTICLES_PER_SOURCE: int = 50
    REQUEST_DELAY: float = 0.5
    
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
        "Tech News",
        "Semiconductors",
        "Robotics",
        "Linux & Open Source",
        "virtualization",
        "general_tech_aggregators"
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
        "Tech News": ["RSS"],
        "Semiconductors": ["RSS"],
        "Robotics": ["RSS"],
        "Linux & Open Source": ["RSS"],
        "virtualization": ["RSS"],
        "general_tech_aggregators": ["RSS"]
    }

    RSS_FEEDS: dict = {
        "AI": [
            "https://research.google/blog/rss",
            "https://news.microsoft.com/source/topics/ai/feed/",
            "https://bair.berkeley.edu/blog/feed.xml",
            "https://analyticsindiamag.com/feed/"
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
            "https://www.naval-technology.com/feed/",
            "https://www.pib.gov.in/RssMain.aspx?Mod=L3",
            "https://ddnews.gov.in/rss/defence",
            "https://www.indiandefencenews.in/feeds/posts/default"
        ],
        "Space Tech": [
            "https://www.nasa.gov/news/feed/",
            "https://www.esa.int/rss/ESA_News",
            "https://www.space.com/feeds/news",
            "https://spacenews.com/feed/",
            "https://www.universetoday.com/feed/",
            "https://www.isro.gov.in/feed",
            "https://mosdac.gov.in/rss.xml"
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
            "https://grahamcluley.com/feed/",
            "https://schneier.com/blog/atom.xml",
            "https://www.csoonline.com/feed",
            "https://www.bleepingcomputer.com/feed/",
            "https://www.crowdstrike.com/blog/feed/",
            "https://www.mandiant.com/resources/blog/rss.xml"
        ],
        "Start-ups": [
            "http://techcrunch.com/startups/feed/",
            "http://feeds.feedburner.com/venturebeat/",
            "https://www.wired.com/feed/rss",
            "https://producthunt.com/feed",
            "https://news.ycombinator.com/rss",
            "https://yourstory.com/feed",
            "https://inc42.com/feed"
        ],
        "Tech News": [
            "http://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss",
            "http://www.theverge.com/rss/index.xml",
            "http://feeds.arstechnica.com/arstechnica/index/",
            "https://www.engadget.com/rss.xml",
            "https://www.cnet.com/rss/news/",
            "https://www.techradar.com/rss",
            "https://economictimes.indiatimes.com/tech-bytes-rss-feed",
            "https://www.gadgets360.com/rss/news",
            "https://www.prnewswire.com/rss",
            "https://www.technologyreview.com/feed/",
            "https://news.mit.edu/rss/feed"
        ],
        "Semiconductors": [
            "https://www.semiconductor-today.com/rss.shtml",
            "https://sst.semiconductor-digest.com/feed/",
            "https://sst.semiconductor-digest.com/category/solid-state-technology/feed/",
            "https://sst.semiconductor-digest.com/category/packaging/feed/",
            "https://www.semiconductors.org/news-events/latest-news/feed/",
            "https://www.eetimes.com/tag/semiconductors/feed/",
            "https://semiengineering.com/feed/",
            "https://semiwiki.com/feed/",
            "https://www.techxplore.com/rss/tags/semiconductors/",
            "https://www.servethehome.com/feed/",
            "https://www.anandtech.com/rss/",
            "https://www.trendforce.com/rss/semiconductor",
            "https://www.digitimes.com/rss/daily.xml",
            "https://www.tomshardware.com/feeds/tag/semiconductors.xml",
            "https://chipsandcheese.com/feed/",
            "https://www.cnx-software.com/feed/"           
        ],
        "Robotics": [
            "https://robohub.org/feed",
            "https://www.therobotreport.com/feed/",
            "https://spectrum.ieee.org/feeds/topic/robotics",
            "https://news.mit.edu/topic/robotics/rss"
        ],
        "Linux & Open Source": [
            "https://www.kernel.org/feeds/kdist.xml",
            "https://lwn.net/headlines/rss",
            "https://www.phoronix.com/rss.php",
            "https://9to5linux.com/feed",
            "https://itsfoss.com/rss",
            "https://omgubuntu.co.uk/feed",
            "https://www.postgresql.org/news.rss",
            "https://blog.nginx.org/rss",
            "https://planet.mysql.com/rss20.xml",
            "https://opensource.googleblog.com/feeds/posts/default",
            "https://aws.amazon.com/blogs/opensource/feed/"
        ],
        "virtualization": [
            "https://www.yellow-bricks.com/feed/",
            "https://williamlam.com/feed",
            "https://virtualizationreview.com/rss-feeds/news.aspx",
            "https://www.qemu.org/feed.xml"
        ],
        "general_tech_aggregators": [
            google_news_url("Technology"),
            google_news_url("Semiconductor Industry"),
            google_news_url("Enterprise Software"),
            google_news_url("Artificial Intelligence"),
            google_news_url("Cloud Computing")
        ],
    } 
    
    CATEGORY_IMAGES: dict = {
        "AI": "/static/img/placeholder_ai.png",
        "Cloud Computing": "/static/img/placeholder_cloud.png",
        "Cybersecurity": "/static/img/placeholder_cyber.png",
        "Defence Tech": "/static/img/placeholder_defence.png",
        "Space Tech": "/static/img/placeholder_space.png",
        "Start-ups": "/static/img/placeholder_startup.png",
        "Quantum Computing": "/static/img/placeholder.png",
        "Renewable Energy": "/static/img/placeholder.png",
        "Tech News": "/static/img/placeholder.png",
        "Semiconductors": "/static/img/placeholder_general.png",
        "Robotics": "/static/img/placeholder_general.png",
        "Linux & Open Source": "/static/img/placeholder_general.png",
        "virtualization": "/static/img/placeholder_general.png",
        "general_tech_aggregators": "/static/img/placeholder_general.png",
        "DEFAULT": "/static/img/placeholder.png"
    }

    class Config:
        env_file = ".env"

settings = Settings()
