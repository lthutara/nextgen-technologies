
import json
from sqlalchemy.orm import Session
from app.models.database import RawArticle, ArticleSection, Article
from app.curation.schemas import FinalArticleData

from config.settings import settings

from app.scraping.content_extractor import extract_article_content
from app.services.summarizer import summarize_with_gemini

class CurationService:
    def __init__(self, db: Session):
        self.db = db

    def summarize_article(self, article_id: int) -> str:
        raw_article = self.db.query(RawArticle).filter(RawArticle.id == article_id).first()
        if not raw_article:
            return None  # Or raise exception

        full_content = extract_article_content(raw_article.source_url)
        if not full_content:
            return "[Summarization failed: Could not extract content.]"

        new_summary = summarize_with_gemini(full_content)
        
        if not new_summary.startswith("[Summarization failed"):
            raw_article.summary = new_summary
            self.db.commit()
            self.db.refresh(raw_article)
        
        return new_summary

    def structure_content(self, article_id: int, article_type: str) -> dict:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured.")

        raw_article = self.db.query(RawArticle).filter(RawArticle.id == article_id).first()
        if not raw_article:
            return None

        prompts = {
            "News": "Structure the following news article into these sections: \"What is this about?\", \"Any change to existing feature/item?\", \"Brief background of the news.\", \"When is it expected to come?\", \"What value it might add?\", \"Competitor advantage.\" Also, provide a \"detailed Overall Summary\". Provide the output as a JSON object where keys are the section titles and values are the structured content.",
            "Research": "Structure the following research article into these sections: \"What is the research about?\", \"What are the key findings?\", \"What are the implications of the research?\", \"What are the limitations of the research?\" Also, provide a \"detailed Overall Summary\". Provide the output as a JSON object where keys are the section titles and values are the structured content.",
            "Analysis": "Structure the following analysis article into these sections: \"What is being analyzed?\", \"What are the main points of the analysis?\", \"What are the conclusions of the analysis?\", \"What are the recommendations?\" Also, provide a \"detailed Overall Summary\". Provide the output as a JSON object where keys are the section titles and values are the structured content.",
            "How-to": "Structure the following how-to article into these sections: \"What is the goal of this how-to?\", \"What are the prerequisites?\", \"What are the steps involved?\", \"What is the expected outcome?\" Also, provide a \"detailed Overall Summary\". Provide the output as a JSON object where keys are the section titles and values are the structured content."
        }

        if article_type not in prompts:
            raise ValueError(f"Unsupported article type for content structuring: {article_type}")

        full_prompt = f"{prompts[article_type]}\n\nArticle Content:\n{raw_article.content}"
        
        structured_json_str = summarize_with_gemini(full_prompt)
        
        parsed_content = None
        try:
            parsed_content = json.loads(structured_json_str)
        except json.JSONDecodeError:
            json_start = structured_json_str.find('```json')
            json_end = structured_json_str.rfind('```')
            if json_start != -1 and json_end != -1 and json_start < json_end:
                extracted_json_str = structured_json_str[json_start + len('```json'):json_end].strip()
                try:
                    parsed_content = json.loads(extracted_json_str)
                except json.JSONDecodeError:
                    pass
        
        if parsed_content is None:
            parsed_content = {"Content Structuring": structured_json_str}

        # Create bilingual structure
        bilingual_content = {}
        for title, content in parsed_content.items():
            # This is a placeholder for actual translation
            bilingual_content[title] = {
                "en": content,
                "te": f"{content}_te"
            }
        
        # The frontend will now receive a dictionary with 'en' and 'te' keys for each section
        return bilingual_content

    def save_structured_content(self, article_id: int, article_title: str, article_type: str, sections_data: dict):
        raw_article = self.db.query(RawArticle).filter(RawArticle.id == article_id).first()
        if not raw_article:
            return None

        raw_article.title = article_title
        raw_article.status = "structured"
        raw_article.content_type = article_type
        self.db.add(raw_article)

        self.db.query(ArticleSection).filter(ArticleSection.raw_article_id == article_id).delete()

        for section_title_en, content_versions in sections_data.items():
            content_en = None
            content_te = None

            if isinstance(content_versions, dict):
                # Handle the new format (when frontend is updated)
                content_en = content_versions.get('en')
                content_te = content_versions.get('te')
            elif isinstance(content_versions, str):
                # Handle the old format (from current frontend) for backward compatibility
                content_en = content_versions
                content_te = f"{content_versions}_te"  # Create placeholder

            article_section = ArticleSection(
                raw_article_id=article_id,
                section_title_en=section_title_en,
                section_content_en=content_en,
                section_title_te=f"{section_title_en}_te", # Placeholder for title translation
                section_content_te=content_te
            )
            self.db.add(article_section)

        self.db.commit()
        return raw_article

    def publish_final_article(self, raw_article_id: int, final_article_data: FinalArticleData):
        raw_article = self.db.query(RawArticle).filter(RawArticle.id == raw_article_id).first()
        if not raw_article:
            return None

        # Create new Article
        new_article = Article(
            title_en=final_article_data.title_en,
            summary_en=final_article_data.summary_en,
            content_en=final_article_data.content_en,
            title_te=final_article_data.title_te,
            summary_te=final_article_data.summary_te,
            content_te=final_article_data.content_te,
            image_url=final_article_data.image_url,
            source_url=final_article_data.source_url,
            source_name=final_article_data.source_name,
            category=final_article_data.category,
            published_date=final_article_data.published_date,
            scraped_date=datetime.utcnow(), # Use current UTC time for scraped_date
            is_active=True, # New articles are active by default
            content_type=final_article_data.content_type
        )
        self.db.add(new_article)

        # Update the raw article status instead of deleting
        raw_article.status = 'published'
        self.db.add(raw_article)

        self.db.commit()
        self.db.refresh(new_article)
        return new_article
