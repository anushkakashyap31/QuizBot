from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth
from app.services.auth_service import auth_service
from app.models.schemas import UserCreate, User
from pydantic import BaseModel, EmailStr
from datetime import timedelta

router = APIRouter()
security = HTTPBearer()

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class LoginRequest(BaseModel):
    id_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class RegisterRequest(BaseModel):
    """Request model for backend registration (Postman testing)"""
    email: EmailStr
    password: str
    full_name: str

class EmailLoginRequest(BaseModel):
    """Request model for email/password login (Postman testing)"""
    email: EmailStr
    password: str

# ============================================
# EXISTING ENDPOINTS (Frontend - Unchanged)
# ============================================

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """
    Register new user (Frontend)
    Frontend handles Firebase registration via SDK
    """
    try:
        return {
            "message": "User registration should be handled by Firebase SDK on frontend",
            "access_token": "",
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """
    Login with Firebase token (Frontend)
    Works with Firebase SDK authentication
    """
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
    """
    Get current user info
    Works with both frontend and backend tokens
    """
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

# ============================================
# NEW ENDPOINTS (Postman Testing - Optional)
# ============================================

@router.post("/register-direct")
async def register_direct(user_data: RegisterRequest):
    """
    🆕 Register user directly via backend (Postman/API testing)
    
    Creates Firebase user server-side without needing frontend.
    Perfect for Postman testing!
    
    Example:
    {
        "email": "test@example.com",
        "password": "Test@123456",
        "full_name": "Test User"
    }
    """
    try:
        # Create Firebase user
        firebase_user = firebase_auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.full_name
        )
        
        print(f"✓ Created Firebase user: {firebase_user.uid}")
        
        # Create custom token
        custom_token = firebase_auth.create_custom_token(firebase_user.uid)
        
        # Create user profile in database
        user_profile = auth_service.create_user_profile(
            uid=firebase_user.uid,
            email=user_data.email,
            full_name=user_data.full_name
        )
        
        # Generate JWT access token
        access_token = auth_service.create_access_token(
            data={"sub": firebase_user.uid, "email": user_data.email},
            expires_delta=timedelta(minutes=30)
        )
        
        print(f"✓ User registered successfully: {user_data.email}")
        
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "uid": firebase_user.uid,
                "email": user_data.email,
                "full_name": user_data.full_name
            },
            "firebase_custom_token": custom_token.decode('utf-8') if isinstance(custom_token, bytes) else custom_token
        }
        
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered. Use /login-email endpoint to login."
        )
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login-email")
async def login_with_email(credentials: EmailLoginRequest):
    """
    🆕 Login with email/password (Postman/API testing)
    
    Simplified login for API testing without Firebase SDK.
    Returns access token directly.
    
    Example:
    {
        "email": "test@example.com",
        "password": "Test@123456"
    }
    """
    try:
        # Get user by email from Firebase
        firebase_user = firebase_auth.get_user_by_email(credentials.email)
        
        print(f"✓ Found user: {credentials.email}")
        
        # Create custom token (bypasses password verification)
        # Note: In production, use Firebase REST API to verify password
        custom_token = firebase_auth.create_custom_token(firebase_user.uid)
        
        # Get user profile
        user_profile = auth_service.get_user_profile(firebase_user.uid)
        
        if not user_profile:
            # Create profile if doesn't exist
            user_profile = auth_service.create_user_profile(
                uid=firebase_user.uid,
                email=credentials.email,
                full_name=firebase_user.display_name or "User"
            )
        
        # Generate JWT access token
        access_token = auth_service.create_access_token(
            data={"sub": firebase_user.uid, "email": credentials.email},
            expires_delta=timedelta(minutes=30)
        )
        
        print(f"✓ Login successful: {credentials.email}")
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_profile,
            "firebase_custom_token": custom_token.decode('utf-8') if isinstance(custom_token, bytes) else custom_token
        }
        
    except firebase_auth.UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please register first using /register-direct endpoint."
        )
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Authentication failed: {str(e)}"
        )

# ============================================
# TESTING/ADMIN ENDPOINTS (Optional)
# ============================================

@router.delete("/test/user/{email}")
async def delete_test_user(email: str):
    """
    🧪 Delete test user (Development/Testing only)
    
    Useful for cleaning up test data.
    Should be disabled in production!
    """
    try:
        # Get user by email
        firebase_user = firebase_auth.get_user_by_email(email)
        
        # Delete from Firebase
        firebase_auth.delete_user(firebase_user.uid)
        
        print(f"✓ Deleted test user: {email}")
        
        return {
            "message": f"User {email} deleted successfully",
            "uid": firebase_user.uid
        }
        
    except firebase_auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"❌ Delete error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")