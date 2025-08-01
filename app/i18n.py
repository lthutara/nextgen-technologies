"""
Internationalization (i18n) support for NextGen Technologies Portal
Handles language detection, translation, and locale management
"""

from typing import Optional
from babel import Locale
from babel.support import Translations
import os
import json

class I18nManager:
    """Manages internationalization for the application"""
    
    def __init__(self):
        self.default_language = 'en'
        self.supported_languages = ['en', 'te']  # English, Telugu
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translation files for supported languages"""
        translations_dir = os.path.join(os.path.dirname(__file__), 'translations')
        
        for lang in self.supported_languages:
            translation_file = os.path.join(translations_dir, f'{lang}.json')
            if os.path.exists(translation_file):
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations[lang] = json.load(f)
            else:
                # Initialize empty translation dict if file doesn't exist
                self.translations[lang] = {}
    
    def get_translation(self, key: str, language: str = None) -> str:
        """Get translated text for a given key and language"""
        if not language:
            language = self.default_language
        
        if language not in self.supported_languages:
            language = self.default_language
        
        # Return translation if exists, otherwise return key itself
        return self.translations.get(language, {}).get(key, key)
    
    def get_language_name(self, lang_code: str) -> str:
        """Get display name for language code"""
        names = {
            'en': 'English',
            'te': 'తెలుగు'
        }
        return names.get(lang_code, lang_code)
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.supported_languages
    
    def detect_language_from_request(self, accept_language: str = None) -> str:
        """Detect preferred language from request headers"""
        if not accept_language:
            return self.default_language
        
        # Simple language detection from Accept-Language header
        for lang in self.supported_languages:
            if lang in accept_language.lower():
                return lang
        
        return self.default_language

# Global i18n instance
i18n_manager = I18nManager()

def get_text(key: str, language: str = None) -> str:
    """Shorthand function to get translated text"""
    return i18n_manager.get_translation(key, language)

def _(key: str, language: str = None) -> str:
    """Even shorter alias for translations"""
    return get_text(key, language)