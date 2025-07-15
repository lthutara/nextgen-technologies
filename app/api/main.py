from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Article, ScrapingLog, get_db, create_tables
from app.scraping.scraper_manager import ScraperManager
from config.settings import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Initialize database
create_tables()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.is_active == True).order_by(Article.scraped_date.desc()).limit(20).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "categories": settings.TECH_CATEGORIES
    })

@app.get("/category/{category}", response_class=HTMLResponse)
async def category_page(category: str, request: Request, db: Session = Depends(get_db)):
    if category not in settings.TECH_CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    articles = db.query(Article).filter(
        Article.category == category,
        Article.is_active == True
    ).order_by(Article.scraped_date.desc()).limit(50).all()
    
    return templates.TemplateResponse("category.html", {
        "request": request,
        "articles": articles,
        "category": category,
        "categories": settings.TECH_CATEGORIES
    })

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

@app.post("/api/scrape")
async def trigger_scraping(category: Optional[str] = None):
    scraper_manager = ScraperManager()
    
    if category:
        if category not in settings.TECH_CATEGORIES:
            raise HTTPException(status_code=400, detail="Invalid category")
        
        db = next(get_db())
        try:
            result = scraper_manager.scrape_category(category, db)
            return {"success": True, "result": result}
        finally:
            db.close()
    else:
        results = scraper_manager.scrape_all_categories()
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