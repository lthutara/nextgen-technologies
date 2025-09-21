
import json
from sqlalchemy.orm import Session
from app.models.database import RawArticle, ArticleSection
from app.scraping.content_extractor import extract_article_content
from app.services.summarizer import summarize_with_gemini
from config.settings import settings

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
            return {"Content Structuring": structured_json_str}
        return parsed_content

    def save_structured_content(self, article_id: int, article_title: str, article_type: str, sections_data: dict):
        raw_article = self.db.query(RawArticle).filter(RawArticle.id == article_id).first()
        if not raw_article:
            return None

        raw_article.title = article_title
        raw_article.status = "structured"
        raw_article.content_type = article_type
        self.db.add(raw_article)

        self.db.query(ArticleSection).filter(ArticleSection.raw_article_id == article_id).delete()

        for section_title, section_content in sections_data.items():
            article_section = ArticleSection(
                raw_article_id=article_id,
                section_title=section_title,
                section_content=section_content
            )
            self.db.add(article_section)

        self.db.commit()
        return raw_article
