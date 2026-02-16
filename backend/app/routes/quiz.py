from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import auth_service
from app.services.quiz_generator import quiz_generator
from app.models.schemas import QuizGenerate, Quiz, QuizSubmission, QuizResult
from typing import Dict

router = APIRouter()
security = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current user ID"""
    token = credentials.credentials
    decoded_token = auth_service.verify_firebase_token(token)
    
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return decoded_token['uid']

@router.post("/generate", response_model=Quiz)
async def generate_quiz(
    quiz_data: QuizGenerate,
    user_id: str = Depends(get_current_user_id)
):
    """Generate quiz from donor email"""
    try:
        quiz = await quiz_generator.generate_quiz(
            user_id=user_id,
            email_content=quiz_data.donor_email,
            num_questions=quiz_data.num_questions
        )
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@router.post("/submit", response_model=QuizResult)
async def submit_quiz(
    submission: QuizSubmission,
    user_id: str = Depends(get_current_user_id)
):
    """Submit quiz answers and get results"""
    try:
        # In a real app, you'd retrieve the quiz from storage
        # For now, we'll need to pass the full quiz object
        # This is a simplified version
        
        raise HTTPException(
            status_code=501,
            detail="This endpoint requires storing quizzes. Use /evaluate instead."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate", response_model=QuizResult)
async def evaluate_quiz(
    quiz: Quiz,
    submission: QuizSubmission,
    user_id: str = Depends(get_current_user_id)
):
    """Evaluate quiz submission"""
    try:
        # Verify quiz belongs to user
        if quiz.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        # Evaluate the quiz
        result = await quiz_generator.evaluate_quiz(
            quiz=quiz,
            user_answers=[ans.dict() for ans in submission.answers]
        )
        
        # Save result to Firebase
        auth_service.save_quiz_result(user_id, result.dict())
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating quiz: {str(e)}")