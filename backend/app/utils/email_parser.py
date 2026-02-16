import re
from bs4 import BeautifulSoup
from typing import Dict, Optional
import mailparser

class EmailParser:
    """Parse and extract content from emails"""
    
    @staticmethod
    def parse_plain_text(text: str) -> Dict[str, str]:
        """Parse plain text email"""
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Try to extract subject if present
        subject_match = re.search(r'^Subject:\s*(.+?)$', text, re.MULTILINE | re.IGNORECASE)
        subject = subject_match.group(1) if subject_match else ""
        
        # Try to extract sender
        from_match = re.search(r'^From:\s*(.+?)$', text, re.MULTILINE | re.IGNORECASE)
        sender = from_match.group(1) if from_match else ""
        
        # Clean content
        content = text
        if subject:
            content = re.sub(r'^Subject:.*?$', '', content, flags=re.MULTILINE | re.IGNORECASE)
        if sender:
            content = re.sub(r'^From:.*?$', '', content, flags=re.MULTILINE | re.IGNORECASE)
        
        content = content.strip()
        
        return {
            'subject': subject,
            'sender': sender,
            'content': content,
            'is_html': False
        }
    
    @staticmethod
    def parse_html(html: str) -> Dict[str, str]:
        """Parse HTML email"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'subject': '',
            'sender': '',
            'content': text,
            'is_html': True
        }
    
    @staticmethod
    def parse_email_file(file_path: str) -> Dict[str, str]:
        """Parse email from .eml file"""
        try:
            mail = mailparser.parse_from_file(file_path)
            
            return {
                'subject': mail.subject or '',
                'sender': mail.from_[0][1] if mail.from_ else '',
                'content': mail.text_plain[0] if mail.text_plain else mail.text_html[0] if mail.text_html else '',
                'date': str(mail.date) if mail.date else '',
                'attachments': [att['filename'] for att in mail.attachments] if mail.attachments else []
            }
        except Exception as e:
            print(f"Error parsing email file: {e}")
            return {
                'subject': '',
                'sender': '',
                'content': '',
                'error': str(e)
            }
    
    @staticmethod
    def extract_key_info(email_content: str) -> Dict[str, any]:
        """Extract key information from email"""
        # Extract amounts (donations)
        amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?', email_content)
        
        # Extract dates
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{4}-\d{2}-\d{2}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, email_content, re.IGNORECASE))
        
        # Extract email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_content)
        
        # Extract phone numbers
        phones = re.findall(r'(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', email_content)
        
        # Detect intent/category
        category = EmailParser.categorize_email(email_content)
        
        return {
            'amounts': amounts,
            'dates': dates,
            'emails': emails,
            'phones': phones,
            'category': category,
            'word_count': len(email_content.split())
        }
    
    @staticmethod
    def categorize_email(content: str) -> str:
        """Categorize email based on content"""
        content_lower = content.lower()
        
        categories = {
            'donation_request': ['donate', 'donation', 'contribute', 'support', 'give'],
            'thank_you': ['thank you', 'grateful', 'appreciation', 'thanks'],
            'event_invitation': ['event', 'invitation', 'join us', 'please attend'],
            'volunteer_request': ['volunteer', 'help needed', 'join our team'],
            'impact_report': ['impact', 'results', 'outcomes', 'achievements'],
            'grant_notification': ['grant', 'funding', 'award'],
            'general_update': ['update', 'news', 'announcement']
        }
        
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                return category
        
        return 'general'