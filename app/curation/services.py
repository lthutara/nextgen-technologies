
import json
from datetime import datetime
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

        prompt = f"""
        Summarize the following article in a concise and informative way, capturing the key points.
        The summary should be suitable for a tech news platform.
        
        Article:
        ---
        {full_content}
        ---
        
        Summary:
        """
        new_summary = summarize_with_gemini(prompt)
        
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

        # First, extract the full content from the source URL
        full_content = extract_article_content(raw_article.source_url)
        if not full_content or full_content.isspace():
            # Fallback to the stored content if extraction fails
            full_content = raw_article.content

        # Common fields for all article types
        common_fields = {
            "Major Highlights": "List 5-10 key takeaways or top highlights from the article.",
            "Key Technologies & Keywords": "Identify major technologies, companies, or keywords mentioned.",
            "Scoring & Evaluation": {
                "Relevance Score": "Score from 1-10 for target tech audience.",
                "Popularity Score": "How much buzz/interest this topic generally generates (1-10).",
                "Breakthrough Score": "Is this a significant advancement or just routine news? (1-10).",
                "Translation Recommendation": "Should we invest time in a high-quality Telugu translation? (Yes/No/Maybe and why)."
            },
            "Verification & Sources": "Suggest 2-3 specific search queries to find more authoritative blog posts or 'top 10' lists on this topic for manual verification."
        }

        prompts = {
            "News": {
                "Topic Overview": "What is this news about in one sentence?",
                "Changes & Updates": "What has changed? Any new features or updates?",
                "Context & Background": "Brief background info to help the reader understand the context.",
                "Expected Timeline": "When is this expected to be released or implemented?",
                "Value Proposition": "What is the primary value or impact of this news?",
                "Competitive Landscape": "How does this compare to competitors or existing solutions?",
                **common_fields,
                "Detailed Summary": "A comprehensive summary of the entire news piece."
            },
            "Research": {
                "Research Goal": "What problem is this research trying to solve?",
                "Methodology": "Briefly describe how the research was conducted.",
                "Key Findings": "What are the most important results?",
                "Impact & Implications": "How does this research change the field?",
                "Limitations": "What are the stated or apparent limitations of the work?",
                **common_fields,
                "Detailed Summary": "A comprehensive technical summary of the research."
            },
            "Analysis": {
                "Subject of Analysis": "What specific trend, company, or tech is being analyzed?",
                "Core Arguments": "What are the main points or arguments made in the analysis?",
                "Data & Evidence": "What evidence is provided to support the claims?",
                "Future Outlook": "What does the analysis predict for the future?",
                "Recommendations": "What actions are suggested based on this analysis?",
                **common_fields,
                "Detailed Summary": "A comprehensive summary of the analysis."
            },
            "How-to": {
                "Objective": "What will the reader achieve by following this guide?",
                "Prerequisites": "What tools, knowledge, or setup is required?",
                "Step-by-Step Breakdown": "Outline the main phases or steps of the process.",
                "Troubleshooting & Tips": "Mention common pitfalls or helpful advice.",
                "Final Result": "What is the end state after following the guide?",
                **common_fields,
                "Detailed Summary": "A comprehensive summary of the how-to guide."
            }
        }

        if article_type not in prompts:
            raise ValueError(f"Unsupported article type for content structuring: {article_type}")

        # Construct a detailed instruction for the JSON output
        fields_desc = json.dumps(prompts[article_type], indent=2)
        full_prompt = f"""
        You are an expert tech content analyst. Analyze the following article and structure it according to the requested fields.
        
        REQUIRED FIELDS AND INSTRUCTIONS:
        {fields_desc}
        
        OUTPUT FORMAT:
        You must output a VALID JSON object where the keys are the field names exactly as listed above.
        The values should be your detailed analysis based on the article content.
        Do not include any markdown formatting (like ```json) in your response, just the raw JSON object.
        
        ARTICLE CONTENT:
        ---
        {full_content}
        ---
        """
        
        structured_json_str = summarize_with_gemini(full_prompt)
        
        # Clean the output if necessary (Gemini sometimes adds markdown even if told not to)
        if "```json" in structured_json_str:
            structured_json_str = structured_json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in structured_json_str:
            structured_json_str = structured_json_str.split("```")[1].split("```")[0].strip()
        
        parsed_content = None
        try:
            parsed_content = json.loads(structured_json_str)
        except json.JSONDecodeError:
            print(f"Failed to parse AI JSON response: {structured_json_str[:200]}...")
            parsed_content = {"Content Structuring": structured_json_str}

        # Create bilingual structure
        bilingual_content = {}
        for title, content in parsed_content.items():
            # If content is a dict (like in Scoring & Evaluation), flatten or stringify it for simplicity in the UI for now
            if isinstance(content, dict):
                content_str = "\n".join([f"{k}: {v}" for k, v in content.items()])
            else:
                content_str = str(content)
                
            bilingual_content[title] = {
                "en": content_str,
                "te": f"{content_str}_te" # Placeholder for actual translation
            }
        
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
