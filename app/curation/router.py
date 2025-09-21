
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Article, RawArticle, ArticleSection, get_db
from app.i18n import get_text
from config.settings import settings
from pydantic import BaseModel
from datetime import datetime
from app.curation.services import CurationService

# Helper function from main.py - consider moving to a shared utility module later
def get_template_context(request: Request, **kwargs):
    # A simplified context for now. In a real scenario, this would be shared.
    def _(key: str) -> str:
        return get_text(key, 'en') # Assuming 'en' for simplicity in this module
    
    context = {
        "request": request,
        "categories": settings.TECH_CATEGORIES,
        "current_language": 'en',
        "supported_languages": ['en', 'te'],
        "_": _,
        **kwargs
    }
    return context

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

router = APIRouter()

@router.get("/curation", response_class=HTMLResponse)
async def curation_page(request: Request, db: Session = Depends(get_db)):
    # This import is here to avoid circular dependency issues if templates are moved
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    context = get_template_context(request)
    return templates.TemplateResponse("curation.html", context)

@router.get("/curation/process/{article_id}", response_class=HTMLResponse)
async def process_article_page(article_id: int, request: Request, db: Session = Depends(get_db)):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    context = get_template_context(request, article=article)
    return templates.TemplateResponse("process.html", context)

@router.get("/api/raw_articles", response_model=List[RawArticleResponse])
async def get_raw_articles(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    raw_articles = db.query(RawArticle).order_by(RawArticle.scraped_date.desc()).offset(offset).limit(limit).all()
    return raw_articles

@router.post("/api/raw_articles/{article_id}/approve")
async def approve_raw_article(article_id: int, db: Session = Depends(get_db)):
    raw_article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not raw_article:
        raise HTTPException(status_code=404, detail="Raw article not found")

    article = Article(
        title=raw_article.title,
        content=raw_article.content,
        summary=raw_article.summary,
        source_url=raw_article.source_url,
        source_name=raw_article.source_name,
        category=raw_article.category,
        published_date=raw_article.published_date,
        scraped_date=raw_article.scraped_date,
        image_url=raw_article.image_url,
        content_type=raw_article.content_type
    )
    db.add(article)
    db.delete(raw_article)
    db.commit()
    return {"success": True, "message": "Raw article approved and moved to articles!"}

@router.post("/api/raw_articles/{article_id}/reject")
async def reject_raw_article(article_id: int, db: Session = Depends(get_db)):
    raw_article = db.query(RawArticle).filter(RawArticle.id == article_id).first()
    if not raw_article:
        raise HTTPException(status_code=404, detail="Raw article not found")

    db.delete(raw_article)
    db.commit()
    return {"success": True, "message": "Raw article rejected!"}

@router.post("/api/raw_articles/{article_id}/summarize")
async def summarize_raw_article(article_id: int, db: Session = Depends(get_db)):
    service = CurationService(db)
    new_summary = service.summarize_article(article_id)
    if new_summary is None:
        raise HTTPException(status_code=404, detail="Raw article not found")
    if new_summary.startswith("[Summarization failed"):
        raise HTTPException(status_code=500, detail=new_summary)
    return {"success": True, "message": "Article summarized successfully!", "new_summary": new_summary}

@router.post("/api/raw_articles/{article_id}/structure_content_ai")
async def structure_content_ai(article_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    article_type = data.get("article_type")
    if not article_type:
        raise HTTPException(status_code=400, detail="Missing article_type.")

    service = CurationService(db)
    try:
        structured_content = service.structure_content(article_id, article_type)
        if structured_content is None:
            raise HTTPException(status_code=404, detail="Raw article not found")
        return {"success": True, "structured_sections": structured_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error during AI content structuring: {e}")
        raise HTTPException(status_code=500, detail=f"AI content structuring failed: {e}")

@router.post("/api/raw_articles/{article_id}/save_structured_content")
async def save_structured_content(article_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    article_title = data.get("article_title")
    article_type = data.get("article_type")
    sections_data = data.get("sections")

    if not article_title or not article_type or not sections_data:
        raise HTTPException(status_code=400, detail="Missing article_title, article_type or sections data")

    service = CurationService(db)
    updated_article = service.save_structured_content(article_id, article_title, article_type, sections_data)
    
    if updated_article is None:
        raise HTTPException(status_code=404, detail="Raw article not found")

    return {"success": True, "message": "Structured sections saved and article status updated!"}
