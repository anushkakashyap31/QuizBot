from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional, Dict, Union, Any
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    uid: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DonorEmail(BaseModel):
    email_content: str
    subject: Optional[str] = None
    sender: Optional[str] = None

class Question(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    difficulty: str

class QuizGenerate(BaseModel):
    donor_email: str
    num_questions: int = 5

class Quiz(BaseModel):
    quiz_id: str
    user_id: str
    email_context: str
    questions: List[Question]
    created_at: Union[datetime, str, Any]  # Accept datetime, string, or any type
    
    @field_validator('created_at', mode='before')
    @classmethod
    def parse_created_at(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                return datetime.now()
        return v

class Answer(BaseModel):
    question_id: str
    selected_answer: str

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[Answer]

class QuestionResult(BaseModel):
    question_id: str
    question_text: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str

class QuizResult(BaseModel):
    quiz_id: str
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    results: List[QuestionResult]
    summary: str
    completed_at: datetime

class ProgressStats(BaseModel):
    total_quizzes: int
    average_score: float
    total_questions_answered: int
    accuracy_rate: float
    improvement_trend: List[Dict]
    topic_performance: Dict[str, float]