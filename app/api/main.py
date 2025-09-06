from fastapi import FastAPI, Depends, HTTPException, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Article, RawArticle, ScrapingLog, get_db, create_tables
from app.scraping.scraper_manager import ScraperManager
from app.i18n import i18n_manager, get_text
from config.settings import settings
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager
from app.scheduler import ArticleScheduler
from app.scraping.content_extractor import extract_article_content
from app.services.summarizer import summarize_with_gemini

# --- Scheduler and Lifespan Management ---
scheduler = ArticleScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage scheduler startup and shutdown."""
    print("INFO:     Starting up application...")
    
    # Run a quick initial scrape on startup for faster development
    print("INFO:     Running initial scrape for 'Tech News' category...")
    try:
        scheduler.scrape_job(category="Tech News")
        print("INFO:     Initial scrape completed.")
    except Exception as e:
        print(f"ERROR:    Initial scrape failed: {e}")

    # Start the scheduler for regular updates
    print("INFO:     Starting scheduler for periodic updates...")
    scheduler.start()
    
    yield
    
    # Shutdown
    print("INFO:     Shutting down application and scheduler...")
    scheduler.stop()

class RawArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    summary: Optional[str]
    source_url: str
    source_name: str
    category: str
    published_date: Optional[datetime]
    scraped_date: datetime

    class Config:
        from_attributes = True

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)

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

@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article_page(article_id: int, request: Request, db: Session = Depends(get_db), lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    article = db.query(Article).filter(Article.id == article_id, Article.is_active == True).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    context = get_template_context(request, language, article=article)
    return templates.TemplateResponse("article.html", context)

@app.get("/curation", response_class=HTMLResponse) # New endpoint for curation UI
async def curation_page(request: Request, db: Session = Depends(get_db), lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    context = get_template_context(request, language)
    return templates.TemplateResponse("curation.html", context)

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
                "content": article.content,
                "source_url": article.source_url,
                "source_name": article.source_name,
                "category": article.category,
                "published_date": article.published_date,
                "scraped_date": article.scraped_date
            }
            for article in articles
        ]
    }

@app.get("/api/raw_articles", response_model=List[RawArticleResponse]) # New endpoint
async def get_raw_articles(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    raw_articles = db.query(RawArticle).order_by(RawArticle.scraped_date.desc()).offset(offset).limit(limit).all()
    return raw_articles

@app.post("/api/raw_articles/{article_id}/approve") # New endpoint for approving raw articles
async def approve_raw_article(article_id: int, db: Session = Depends(get_db)):
    raw_article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not raw_article:
        raise HTTPException(status_code=404, detail="Raw article not found")

    # Create a new Article from RawArticle data
    article = Article(
        title=raw_article.title,
        content=raw_article.content,
        summary=raw_article.summary,
        source_url=raw_article.source_url,
        source_name=raw_article.source_name,
        category=raw_article.category,
        published_date=raw_article.published_date,
        scraped_date=raw_article.scraped_date
    )
    db.add(article)
    db.delete(raw_article) # Delete raw article after approval
    db.commit()
    return {"success": True, "message": "Raw article approved and moved to articles!"}

@app.post("/api/raw_articles/{article_id}/reject") # New endpoint for rejecting raw articles
async def reject_raw_article(article_id: int, db: Session = Depends(get_db)):
    raw_article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not raw_article:
        raise HTTPException(status_code=404, detail="Raw article not found")

    db.delete(raw_article) # Delete raw article
    db.commit()
    return {"success": True, "message": "Raw article rejected!"}


@app.post("/api/raw_articles/{article_id}/summarize")
async def summarize_raw_article(article_id: int, db: Session = Depends(get_db)):
    raw_article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not raw_article:
        raise HTTPException(status_code=404, detail="Raw article not found")

    # Step 1: Extract full content
    full_content = extract_article_content(raw_article.source_url)
    if not full_content:
        raise HTTPException(status_code=500, detail="Failed to extract article content.")

    # Step 2: Summarize the content
    new_summary = summarize_with_gemini(full_content)
    if new_summary.startswith("[Summarization failed"):
        raise HTTPException(status_code=500, detail=new_summary)

    # Step 3: Update the database
    raw_article.summary = new_summary
    db.commit()
    db.refresh(raw_article)

    return {"success": True, "message": "Article summarized successfully!", "new_summary": new_summary}

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


# --- Admin Panel ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, lang: str = Cookie(None)):
    language = get_user_language(request, lang)
    context = get_template_context(request, language, tech_categories=settings.TECH_CATEGORIES)
    return templates.TemplateResponse("admin.html", context)


@app.post("/admin/scrape/{category}")
async def admin_scrape_category(category: str):
    if category not in settings.TECH_CATEGORIES:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        # Run in background?
        scheduler.scrape_job(category=category)
        return {"success": True, "message": f"Scraping for '{category}' started."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin/clear_raw_articles")
async def admin_clear_raw_articles(db: Session = Depends(get_db)):
    try:
        num_deleted = db.query(RawArticle).delete()
        db.commit()
        return {"success": True, "message": f"{num_deleted} raw articles deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
