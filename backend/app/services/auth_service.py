import firebase_admin
from firebase_admin import credentials, auth, db
from app.config import settings
from typing import Optional, Dict
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Initialize Firebase
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': settings.FIREBASE_DATABASE_URL
})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.db = db.reference()
    
    def verify_firebase_token(self, id_token: str) -> Optional[Dict]:
        """Verify Firebase ID token with clock skew tolerance"""
        try:
            # Add 5 seconds of clock skew tolerance to handle system clock drift
            decoded_token = auth.verify_id_token(
                id_token,
                clock_skew_seconds=5  # ← ADD THIS LINE
            )
            return decoded_token
        except auth.ExpiredIdTokenError:
            print("Token verification error: Token has expired")
            return None
        except auth.InvalidIdTokenError as e:
            print(f"Token verification error: Invalid token - {str(e)}")
            return None
        except Exception as e:
            print(f"Token verification error: {e}")
            return None
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def get_user_profile(self, uid: str) -> Optional[Dict]:
        """Get user profile from Firebase Realtime Database"""
        user_ref = self.db.child('users').child(uid)
        return user_ref.get()
    
    def create_user_profile(self, uid: str, email: str, full_name: str) -> Dict:
        """Create user profile in Firebase"""
        user_data = {
            'uid': uid,
            'email': email,
            'full_name': full_name,
            'created_at': datetime.now().isoformat(),
            'total_quizzes': 0,
            'total_score': 0.0
        }
        
        user_ref = self.db.child('users').child(uid)
        user_ref.set(user_data)
        return user_data
    
    def save_quiz_result(self, user_id: str, quiz_result: Dict):
        """Save quiz result to Firebase"""
        quiz_id = quiz_result['quiz_id']
        
        # Save to user's history
        history_ref = self.db.child('quiz_history').child(user_id).child(quiz_id)
        history_ref.set(quiz_result)
        
        # Update user stats
        user_ref = self.db.child('users').child(user_id)
        user_data = user_ref.get() or {}
        
        total_quizzes = user_data.get('total_quizzes', 0) + 1
        total_score = user_data.get('total_score', 0.0) + quiz_result['score']
        
        user_ref.update({
            'total_quizzes': total_quizzes,
            'total_score': total_score,
            'average_score': total_score / total_quizzes,
            'last_quiz_date': datetime.now().isoformat()
        })
    
    def get_user_history(self, user_id: str) -> list:
        """Get user's quiz history"""
        history_ref = self.db.child('quiz_history').child(user_id)
        history = history_ref.get() or {}
        
        # Convert to list and sort by date
        history_list = []
        for quiz_id, data in history.items():
            history_list.append(data)
        
        history_list.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
        return history_list
    
    def get_user_analytics(self, user_id: str) -> Dict:
        """Get user analytics and progress"""
        user_ref = self.db.child('users').child(user_id)
        user_data = user_ref.get() or {}
        
        history = self.get_user_history(user_id)
        
        # Calculate analytics
        total_quizzes = len(history)
        total_questions = sum(h.get('total_questions', 0) for h in history)
        correct_answers = sum(h.get('correct_answers', 0) for h in history)
        
        accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Get recent performance trend (last 10 quizzes)
        recent_scores = [h.get('score', 0) for h in history[:10]]
        
        # Calculate improvement trend
        improvement_trend = []
        for i, score in enumerate(recent_scores):
            improvement_trend.append({
                'quiz_number': total_quizzes - i,
                'score': score,
                'date': history[i].get('completed_at', '')
            })
        
        improvement_trend.reverse()
        
        return {
            'total_quizzes': total_quizzes,
            'average_score': user_data.get('average_score', 0),
            'total_questions_answered': total_questions,
            'accuracy_rate': accuracy_rate,
            'improvement_trend': improvement_trend,
            'recent_quizzes': history[:5]
        }

auth_service = AuthService()