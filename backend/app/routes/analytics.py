from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import auth_service
from typing import List, Dict

router = APIRouter()
security = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current user ID"""
    token = credentials.credentials
    decoded_token = auth_service.verify_firebase_token(token)
    
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return decoded_token['uid']

@router.get("/history")
async def get_history(user_id: str = Depends(get_current_user_id)) -> List[Dict]:
    """Get user's quiz history"""
    try:
        history = auth_service.get_user_history(user_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress")
async def get_progress(user_id: str = Depends(get_current_user_id)) -> Dict:
    """Get user's progress analytics"""
    try:
        analytics = auth_service.get_user_analytics(user_id)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats(user_id: str = Depends(get_current_user_id)) -> Dict:
    """Get detailed statistics"""
    try:
        user_profile = auth_service.get_user_profile(user_id)
        analytics = auth_service.get_user_analytics(user_id)
        
        return {
            "user": user_profile,
            "analytics": analytics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))