import google.generativeai as genai
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarize_with_gemini(prompt: str) -> str:
    """
    Generates content using the Google Gemini API.
    """
    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in settings. Cannot generate content.")
        return "[Generation failed: API key not configured]"

    if not prompt or prompt.isspace():
        logger.warning("Prompt is empty. Returning empty response.")
        return ""

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.5))
        
        text_response = response.text
        logger.info(f"Successfully generated content of length {len(text_response)}.")
        return text_response

    except Exception as e:
        logger.error(f"An error occurred while generating content with Gemini: {e}")
        return f"[Generation failed: {e}]"
