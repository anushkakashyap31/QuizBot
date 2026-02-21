from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import auth_service
from app.services.quiz_generator import quiz_generator
from app.models.schemas import QuizGenerate, Quiz, Question
from typing import Dict, List, Any
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Dependency to get current user ID"""
    token = credentials.credentials
    decoded_token = auth_service.verify_firebase_token(token)
    
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return decoded_token['uid']

@router.post("/generate")
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
        print(f"Error generating quiz: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating quiz: {str(e)}"
        )

@router.post("/evaluate")
async def evaluate_quiz(
    payload: Dict[str, Any],
    user_id: str = Depends(get_current_user_id)
):
    """Evaluate quiz submission"""
    try:
        # Extract quiz and answers from payload
        quiz_data = payload.get("quiz")
        answers_data = payload.get("answers", [])

        print(f"Received quiz_id: {quiz_data.get('quiz_id')}")
        print(f"Number of answers: {len(answers_data)}")

        if not quiz_data:
            raise HTTPException(status_code=400, detail="Quiz data is required")

        # Reconstruct Quiz object
        questions = [Question(**q) for q in quiz_data.get("questions", [])]
        
        # Handle created_at as either string or datetime
        created_at = quiz_data.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            except:
                created_at = datetime.now()
        
        quiz = Quiz(
            quiz_id=quiz_data.get("quiz_id"),
            user_id=quiz_data.get("user_id"),
            email_context=quiz_data.get("email_context"),
            questions=questions,
            created_at=created_at
        )

        # Verify quiz belongs to user
        if quiz.user_id != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")

        # Evaluate the quiz
        result = await quiz_generator.evaluate_quiz(
            quiz=quiz,
            user_answers=answers_data
        )

        # Save result to Firebase
        result_dict = result.dict()
        result_dict['completed_at'] = result_dict['completed_at'].isoformat()
        auth_service.save_quiz_result(user_id, result_dict)

        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error evaluating quiz: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error evaluating quiz: {str(e)}"
        )