# NextGen Technologies Portal

> A technology content analysis and creation platform that transforms English-language articles into high-quality, insightful content for Telugu-speaking audiences.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

NextGen Technologies Portal is a sophisticated content transformation platform designed to make technology accessible and understandable for Telugu-speaking audiences. Instead of simple aggregation, the platform uses a human-in-the-loop system, powered by AI, to analyze, dissect, and reconstruct English-language tech articles into new, insightful content in Telugu.

Our unique workflow allows editors to classify content (e.g., as 'News' or 'Research'), perform a deep analysis to understand its core components, and then create fresh articles that deliver maximum value and clarity to our readers.

### ✨ Key Features

- **✍️ Advanced Content Creation**: A human-in-the-loop workflow for transforming raw articles into new, high-value content in Telugu.
- **🧠 AI-Powered Analysis**: Employs AI to dissect articles into structured insights (e.g., 'What is it?', 'What's new?', 'What's the impact?'), with analysis tailored to the content type.
- **🏷️ Rich Content Classification**: Support for multiple article types, including:
    - `news_brief`
    - `research_deep_dive`
    - `explanatory_article`
    - `founder_story`
    - `startup_story`
- **🌐 Telugu-First Approach**: Primarily focused on creating high-quality, original content for the Telugu-speaking community.
- **🔄 Automated Content Sourcing**: Gathers raw articles from multiple tech sources to feed the curation pipeline.
- **📱 Responsive Design**: A clean, mobile-first user interface for both readers and editors.

### 🏷️ Technology Categories

- **🤖 Artificial Intelligence** - ML, Deep Learning, AI applications
- **🚀 Start-ups** - Funding news, emerging companies, innovation
- **🛡️ Cybersecurity** - Security threats, protection technologies
- **☁️ Cloud Computing** - Cloud services, serverless, DevOps
- **⚛️ Quantum Computing** - Quantum research and applications
- **🌱 Renewable Energy** - Clean tech, sustainability innovations
- **🛡️ Defence Technology** - Military tech, autonomous systems
- **🚀 Space Technology** - Space exploration, satellite tech
- **📰 Tech News** - Industry updates, product launches

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, APScheduler
- **Database**: PostgreSQL (production) / SQLite (development)
- **Web Scraping**: BeautifulSoup4, Scrapy, Selenium
- **Frontend**: Bootstrap 5, Jinja2, HTML/CSS/JavaScript
- **Internationalization**: Flask-Babel (planned)
- **Deployment**: Docker, Uvicorn

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lthutara/nextgen-technologies.git
cd nextgen-technologies
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations (optional for development)
# The application works with default SQLite settings
```

### 5. Launch the Application

```bash
# Start the application
python run.py
```

The application will be available at: **http://localhost:8000**

## 🎯 Usage

### Web Interface

1. **Home Page**: View latest tech news from all categories
2. **Category Pages**: Browse articles by specific technology domain
3. **Manual Updates**: Click "Update Articles" to fetch fresh content
4. **Navigation**: Use the top menu to explore different sections

### API Endpoints

```bash
# Get all articles
GET http://localhost:8000/api/articles

# Get articles by category
GET http://localhost:8000/api/articles?category=AI

# Trigger manual scraping
POST http://localhost:8000/api/scrape

# View scraping logs
GET http://localhost:8000/api/logs
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database Configuration
DATABASE_URL=sqlite:///./nextgen_tech.db

# Application Settings
DEBUG=True
APP_NAME="NextGen Technologies Portal"
APP_VERSION="1.0.0"

# Scraping Configuration
SCRAPING_INTERVAL_HOURS=24
MAX_ARTICLES_PER_SOURCE=50
REQUEST_DELAY=1.0
```

### Categories Configuration

Edit `config/settings.py` to modify technology categories:

```python
TECH_CATEGORIES = [
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
```

## 🔍 Development

### Project Structure

```
nextgen-technologies/
├── app/
│   ├── api/                 # FastAPI routes and endpoints
│   ├── models/             # Database models and schemas
│   ├── scraping/           # Web scraping modules
│   ├── static/             # CSS, JS, and static assets
│   └── templates/          # Jinja2 HTML templates
├── config/                 # Configuration settings
├── database/              # Database migrations (if any)
├── requirements.txt       # Python dependencies
├── run.py                # Application entry point
└── CLAUDE.md             # Development instructions
```

### Adding New Scrapers

1. Create a new scraper class in `app/scraping/`
2. Inherit from `BaseScraper`
3. Implement required methods:
   - `get_article_links()`
   - `extract_article_data()`
4. Register scraper in `ScraperManager`

### Running in Development Mode

```bash
# Run with auto-reload
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

## ⚙️ Production Deployment

### Using Docker (Coming Soon)

```bash
# Build Docker image
docker build -t nextgen-tech .

# Run container
docker run -p 8000:8000 nextgen-tech
```

### Database Setup for Production

1. Set up PostgreSQL database
2. Update `DATABASE_URL` in environment variables
3. Run database migrations (if applicable)

## 🌐 Multilingual Support (Planned)

The platform is being developed with Telugu language support:

- **UI Translation**: Complete interface in Telugu
- **Content Summaries**: Key insights translated
- **Language Toggle**: Easy switching between languages
- **Cultural Context**: Relevant local tech news

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact & Support

- **General Inquiries**: info@nextgentech.portal
- **Technical Support**: support@nextgentech.portal
- **Content Suggestions**: content@nextgentech.portal
- **Partnerships**: partnerships@nextgentech.portal

## 🙏 Acknowledgments

- [arXiv.org](https://arxiv.org/) for research paper access
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Bootstrap](https://getbootstrap.com/) for responsive UI components
- Open source community for various tools and libraries

## 📈 Roadmap

- [x] Core aggregation platform
- [x] Web interface and API
- [x] Multiple technology categories
- [ ] Telugu language integration
- [ ] User accounts and personalization
- [ ] Mobile application
- [ ] Advanced search and filtering
- [ ] Community features

---

**Made with ❤️ for the global tech community and Telugu-speaking audiences**
