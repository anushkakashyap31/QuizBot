from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional
import os

Base = declarative_base()

class User(Base):
    """User model for local database (alternative to Firebase)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Statistics
    total_quizzes = Column(Integer, default=0)
    total_score = Column(Float, default=0.0)
    average_score = Column(Float, default=0.0)
    last_quiz_date = Column(DateTime, nullable=True)
    
    # Relationships
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResultDB", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(uid={self.uid}, email={self.email})>"


class Quiz(Base):
    """Quiz model"""
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(String(255), ForeignKey("users.uid"), nullable=False)
    
    # Quiz content
    email_context = Column(Text, nullable=False)
    questions_json = Column(JSON, nullable=False)  # Store questions as JSON
    
    # Metadata
    num_questions = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="quizzes")
    result = relationship("QuizResultDB", back_populates="quiz", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Quiz(quiz_id={self.quiz_id}, user_id={self.user_id})>"


class QuizResultDB(Base):
    """Quiz result model"""
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(String(255), unique=True, index=True, nullable=False)
    quiz_id = Column(String(255), ForeignKey("quizzes.quiz_id"), nullable=False)
    user_id = Column(String(255), ForeignKey("users.uid"), nullable=False)
    
    # Results
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    results_json = Column(JSON, nullable=False)  # Store detailed results as JSON
    summary = Column(Text, nullable=True)
    
    # Metadata
    completed_at = Column(DateTime, default=datetime.utcnow)
    time_taken_seconds = Column(Integer, nullable=True)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="result")
    user = relationship("User", back_populates="quiz_results")
    
    def __repr__(self):
        return f"<QuizResult(quiz_id={self.quiz_id}, score={self.score})>"


class DonorEmail(Base):
    """Donor email storage model"""
    __tablename__ = "donor_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(String(255), ForeignKey("users.uid"), nullable=False)
    
    # Email content
    subject = Column(String(500), nullable=True)
    sender = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(100), nullable=True)  # e.g., "donation_request", "thank_you", etc.
    
    # Vector embedding info (reference to vector DB)
    vector_db_id = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<DonorEmail(email_id={self.email_id}, subject={self.subject})>"


class UserProgress(Base):
    """User progress tracking model"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.uid"), nullable=False)
    
    # Progress metrics
    topic = Column(String(255), nullable=False)  # e.g., "donor_relations", "fundraising"
    total_attempts = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    
    # Timestamps
    first_attempt = Column(DateTime, default=datetime.utcnow)
    last_attempt = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, topic={self.topic})>"


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quizbot.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=True  # Set to False in production
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")

def drop_db():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("✓ Database tables dropped")

# Database utility functions
class DatabaseService:
    """Database service for CRUD operations"""
    
    @staticmethod
    def create_user(db, uid: str, email: str, full_name: str):
        """Create a new user"""
        user = User(
            uid=uid,
            email=email,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_uid(db, uid: str):
        """Get user by UID"""
        return db.query(User).filter(User.uid == uid).first()
    
    @staticmethod
    def get_user_by_email(db, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user_stats(db, uid: str, quiz_score: float):
        """Update user statistics after quiz completion"""
        user = db.query(User).filter(User.uid == uid).first()
        if user:
            user.total_quizzes += 1
            user.total_score += quiz_score
            user.average_score = user.total_score / user.total_quizzes
            user.last_quiz_date = datetime.utcnow()
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def save_quiz(db, quiz_data: dict):
        """Save a quiz to database"""
        quiz = Quiz(**quiz_data)
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        return quiz
    
    @staticmethod
    def get_quiz(db, quiz_id: str):
        """Get quiz by ID"""
        return db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    
    @staticmethod
    def save_quiz_result(db, result_data: dict):
        """Save quiz result"""
        result = QuizResultDB(**result_data)
        db.add(result)
        db.commit()
        db.refresh(result)
        
        # Mark quiz as completed
        quiz = db.query(Quiz).filter(Quiz.quiz_id == result_data['quiz_id']).first()
        if quiz:
            quiz.is_completed = True
            db.commit()
        
        return result
    
    @staticmethod
    def get_user_history(db, uid: str, limit: int = 50):
        """Get user's quiz history"""
        results = db.query(QuizResultDB).filter(
            QuizResultDB.user_id == uid
        ).order_by(
            QuizResultDB.completed_at.desc()
        ).limit(limit).all()
        
        return results
    
    @staticmethod
    def get_user_analytics(db, uid: str):
        """Get user analytics"""
        user = db.query(User).filter(User.uid == uid).first()
        if not user:
            return None
        
        # Get all results
        results = db.query(QuizResultDB).filter(
            QuizResultDB.user_id == uid
        ).order_by(
            QuizResultDB.completed_at.desc()
        ).all()
        
        # Calculate analytics
        total_questions = sum(r.total_questions for r in results)
        correct_answers = sum(r.correct_answers for r in results)
        accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Get improvement trend (last 10 quizzes)
        recent_results = results[:10]
        improvement_trend = [
            {
                'quiz_number': len(results) - i,
                'score': r.score,
                'date': r.completed_at.isoformat()
            }
            for i, r in enumerate(reversed(recent_results))
        ]
        
        return {
            'total_quizzes': user.total_quizzes,
            'average_score': user.average_score,
            'total_questions_answered': total_questions,
            'accuracy_rate': accuracy_rate,
            'improvement_trend': improvement_trend,
            'recent_quizzes': [
                {
                    'quiz_id': r.quiz_id,
                    'score': r.score,
                    'completed_at': r.completed_at.isoformat()
                }
                for r in results[:5]
            ]
        }
    
    @staticmethod
    def save_donor_email(db, email_data: dict):
        """Save donor email"""
        email = DonorEmail(**email_data)
        db.add(email)
        db.commit()
        db.refresh(email)
        return email
    
    @staticmethod
    def update_user_progress(db, uid: str, topic: str, is_correct: bool):
        """Update user progress for a topic"""
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == uid,
            UserProgress.topic == topic
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=uid,
                topic=topic
            )
            db.add(progress)
        
        progress.total_attempts += 1
        if is_correct:
            progress.correct_answers += 1
        
        progress.accuracy_rate = (progress.correct_answers / progress.total_attempts) * 100
        progress.last_attempt = datetime.utcnow()
        
        db.commit()
        db.refresh(progress)
        return progress

db_service = DatabaseService()