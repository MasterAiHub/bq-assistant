import bleach
import logging

logger = logging.getLogger(__name__)

class Sanitizer:
    """Handles input sanitization to prevent XSS attacks"""

    def __init__(self):
        self.allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'p', 'strong', 'ul'
        ]
        self.allowed_attributes = {
            'a': ['href', 'title'],
            'abbr': ['title'],
            'acronym': ['title']
        }

    def sanitize_html(self, html_content: str) -> str:
        """Sanitizes HTML content to remove dangerous tags and attributes."""
        try:
            clean_html = bleach.clean(
                html_content,
                tags=self.allowed_tags,
                attributes=self.allowed_attributes,
                strip=True
            )
            return clean_html
        except Exception as e:
            logger.error(f"HTML sanitization error: {str(e)}")
            return html_content

    def sanitize_text(self, text_content: str) -> str:
        """Sanitizes plain text content to prevent script injection."""
        try:
            # For plain text, we mainly want to escape HTML entities
            clean_text = bleach.clean(text_content, tags=[], attributes={}, strip=True)
            return clean_text
        except Exception as e:
            logger.error(f"Text sanitization error: {str(e)}")
            return text_content
