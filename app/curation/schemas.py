from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FinalArticleData(BaseModel):
    title_en: str
    summary_en: Optional[str]
    content_en: str
    title_te: Optional[str]
    summary_te: Optional[str]
    content_te: Optional[str]
    image_url: Optional[str]
    source_url: str
    source_name: str
    category: str
    published_date: Optional[datetime]
    content_type: Optional[str]
