from fastapi import FastAPI, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Article, ScrapingLog, get_db, create_tables
from app.scraping.scraper_manager import ScraperManager
from app.i18n import i18n_manager, get_text
from config.settings import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize database
create_tables()

# Language detection helper
def get_user_language(request: Request, lang_cookie: str = Cookie(None)) -> str:
    """Detect user's preferred language from cookie or headers"""
    # First check cookie
    if lang_cookie and i18n_manager.is_supported_language(lang_cookie):
        return lang_cookie
    
    # Then check Accept-Language header
    accept_language = request.headers.get('accept-language', '')
    detected = i18n_manager.detect_language_from_request(accept_language)
    return detected

# Template context helper
def get_template_context(request: Request, language: str = None, **kwargs):
    """Get common template context with translations"""
    if not language:
        language = get_user_language(request)
    
    # Create translation function for templates
    def _(key: str) -> str:
        return get_text(key, language)
    
    context = {
        "request": request,
        "categories": settings.TECH_CATEGORIES,
        "current_language": language,
        "supported_languages": i18n_manager.supported_languages,
        "_": _,
        **kwargs
    }
    return context

# Language switching route
@app.get("/set-language/{language}")
async def set_language(language: str, request: Request):
    """Set user's preferred language"""
    if not i18n_manager.is_supported_language(language):
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    # Redirect back to previous page or home
    referer = request.headers.get('referer', '/')
    response = RedirectResponse(url=referer, status_code=302)
    response.set_cookie(key="lang", value=language, max_age=30*24*60*60)  # 30 days
    return response

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db), lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    articles = db.query(Article).filter(Article.is_active == True).order_by(Article.scraped_date.desc()).limit(20).all()
    
    context = get_template_context(request, language, articles=articles)
    return templates.TemplateResponse("index.html", context)

@app.get("/category/{category}", response_class=HTMLResponse)
async def category_page(category: str, request: Request, db: Session = Depends(get_db), lang: str = Cookie(None)):
    if category not in settings.TECH_CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    language = get_user_language(request, lang)
    articles = db.query(Article).filter(
        Article.category == category,
        Article.is_active == True
    ).order_by(Article.scraped_date.desc()).limit(50).all()
    
    context = get_template_context(request, language, articles=articles, category=category)
    return templates.TemplateResponse("category.html", context)

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request, lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    context = get_template_context(request, language)
    return templates.TemplateResponse("about.html", context)

@app.get("/how-it-works", response_class=HTMLResponse)
async def how_it_works_page(request: Request, lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    context = get_template_context(request, language)
    return templates.TemplateResponse("how_it_works.html", context)

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request, lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    context = get_template_context(request, language)
    return templates.TemplateResponse("contact.html", context)

@app.get("/api/articles")
async def get_articles(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Article).filter(Article.is_active == True)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.order_by(Article.scraped_date.desc()).offset(offset).limit(limit).all()
    
    return {
        "articles": [
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "source_url": article.source_url,
                "source_name": article.source_name,
                "category": article.category,
                "published_date": article.published_date,
                "scraped_date": article.scraped_date
            }
            for article in articles
        ]
    }

from app.scheduler import ArticleScheduler

# Initialize scheduler
scheduler = ArticleScheduler()

@app.post("/api/scrape")
async def trigger_scraping(category: Optional[str] = None):
    if category and category not in settings.TECH_CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    results = scheduler.scrape_job(category=category)
    return {"success": True, "results": results}

@app.get("/api/logs")
async def get_scraping_logs(db: Session = Depends(get_db)):
    logs = db.query(ScrapingLog).order_by(ScrapingLog.started_at.desc()).limit(50).all()
    return {
        "logs": [
            {
                "id": log.id,
                "source_name": log.source_name,
                "category": log.category,
                "articles_found": log.articles_found,
                "articles_new": log.articles_new,
                "status": log.status,
                "error_message": log.error_message,
                "started_at": log.started_at,
                "completed_at": log.completed_at
            }
            for log in logs
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)