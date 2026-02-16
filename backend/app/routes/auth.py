from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import auth_service
from app.models.schemas import UserCreate, User
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()
security = HTTPBearer()

class LoginRequest(BaseModel):
    id_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register new user"""
    try:
        # In a real app, you'd create Firebase user here
        # For now, we'll assume Firebase handles registration on frontend
        
        return {
            "message": "User registration should be handled by Firebase SDK on frontend",
            "access_token": "",
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Login with Firebase token"""
    try:
        # Verify Firebase token
        decoded_token = auth_service.verify_firebase_token(login_data.id_token)
        
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        uid = decoded_token['uid']
        email = decoded_token.get('email', '')
        
        # Get or create user profile
        user_profile = auth_service.get_user_profile(uid)
        
        if not user_profile:
            # Create new profile
            user_profile = auth_service.create_user_profile(
                uid=uid,
                email=email,
                full_name=decoded_token.get('name', email.split('@')[0])
            )
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": uid, "email": email},
            expires_delta=timedelta(minutes=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_profile
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user info"""
    try:
        # Verify Firebase token
        token = credentials.credentials
        decoded_token = auth_service.verify_firebase_token(token)
        
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        uid = decoded_token['uid']
        user_profile = auth_service.get_user_profile(uid)
        
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user_profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))