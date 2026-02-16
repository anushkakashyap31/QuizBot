from typing import Dict, List, Any
import json
from datetime import datetime
import hashlib
import secrets

def generate_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix"""
    random_str = secrets.token_hex(8)
    if prefix:
        return f"{prefix}_{random_str}"
    return random_str

def hash_text(text: str) -> str:
    """Generate hash of text"""
    return hashlib.sha256(text.encode()).hexdigest()

def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat() if dt else None

def parse_datetime(date_str: str) -> datetime:
    """Parse ISO datetime string"""
    try:
        return datetime.fromisoformat(date_str)
    except:
        return None

def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage safely"""
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)

def sanitize_email_content(content: str) -> str:
    """Sanitize email content for processing"""
    # Remove excessive whitespace
    content = " ".join(content.split())
    # Limit length
    max_length = 10000
    if len(content) > max_length:
        content = content[:max_length] + "..."
    return content

def extract_topics_from_text(text: str) -> List[str]:
    """Extract potential topics from text (simple version)"""
    keywords = {
        'donation': 'fundraising',
        'donor': 'donor_relations',
        'volunteer': 'volunteer_management',
        'impact': 'impact_measurement',
        'grant': 'grant_writing',
        'budget': 'financial_management',
        'program': 'program_development',
        'community': 'community_engagement',
        'marketing': 'marketing_outreach',
        'event': 'event_planning'
    }
    
    text_lower = text.lower()
    found_topics = set()
    
    for keyword, topic in keywords.items():
        if keyword in text_lower:
            found_topics.add(topic)
    
    return list(found_topics) if found_topics else ['general']

def format_quiz_for_frontend(quiz: Any) -> Dict:
    """Format quiz object for frontend consumption"""
    return {
        'quiz_id': quiz.quiz_id,
        'user_id': quiz.user_id,
        'email_context': quiz.email_context[:500],  # Truncate for preview
        'questions': [
            {
                'id': q.id,
                'question_text': q.question_text,
                'options': q.options,
                'difficulty': q.difficulty
            }
            for q in quiz.questions
        ],
        'num_questions': len(quiz.questions),
        'created_at': format_datetime(quiz.created_at)
    }

def format_result_for_frontend(result: Any) -> Dict:
    """Format quiz result for frontend"""
    return {
        'quiz_id': result.quiz_id,
        'user_id': result.user_id,
        'score': result.score,
        'total_questions': result.total_questions,
        'correct_answers': result.correct_answers,
        'results': [
            {
                'question_id': r.question_id,
                'question_text': r.question_text,
                'selected_answer': r.selected_answer,
                'correct_answer': r.correct_answer,
                'is_correct': r.is_correct,
                'explanation': r.explanation
            }
            for r in result.results
        ],
        'summary': result.summary,
        'completed_at': format_datetime(result.completed_at),
        'grade': get_grade(result.score),
        'performance': get_performance_label(result.score)
    }

def get_grade(score: float) -> str:
    """Get letter grade from score"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def get_performance_label(score: float) -> str:
    """Get performance label from score"""
    if score >= 90:
        return 'Excellent'
    elif score >= 80:
        return 'Very Good'
    elif score >= 70:
        return 'Good'
    elif score >= 60:
        return 'Fair'
    else:
        return 'Needs Improvement'

def validate_quiz_answers(quiz_questions: List[Dict], user_answers: List[Dict]) -> bool:
    """Validate that user provided answers for all questions"""
    question_ids = {q['id'] for q in quiz_questions}
    answer_ids = {a['question_id'] for a in user_answers}
    return question_ids == answer_ids