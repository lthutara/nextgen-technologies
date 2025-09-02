import google.generativeai as genai
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarize_with_gemini(text_to_summarize: str) -> str:
    """
    Summarizes the given text using the Google Gemini API.
    """
    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in settings. Cannot summarize.")
        return "[Summarization failed: API key not configured]"

    if not text_to_summarize or text_to_summarize.isspace():
        logger.warning("Text to summarize is empty. Returning empty summary.")
        return ""

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        Summarize the following article in a concise and informative way, capturing the key points.
        The summary should be suitable for a tech news platform.
        
        Article:
        ---
        {text_to_summarize}
        ---
        
        Summary:
        """
        
        response = model.generate_content(prompt)
        
        summary = response.text
        logger.info(f"Successfully generated summary of length {len(summary)}.")
        return summary

    except Exception as e:
        logger.error(f"An error occurred while summarizing with Gemini: {e}")
        return f"[Summarization failed: {e}]"
