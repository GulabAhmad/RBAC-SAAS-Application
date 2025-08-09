from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import create_access_token, create_refresh_token, authenticate_user, verify_refresh_token
from .. import crud, schemas
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=schemas.User)
async def register_user(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user with email verification"""
    try:
        print(f"🔍 Registering user: {user.email}")
        
        # Check if passwords match
        if user.password != user.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Create user with email verification
        user_data = schemas.UserCreate(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            organization_name=user.organization_name
        )
        
        print(f"✅ User data created: {user_data.email}")
        
        result = crud.create_user(db=db, user=user_data)
        print(f"✅ User created successfully: {result.email}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error in register_user: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/verify-email", response_model=schemas.User)
async def verify_email(
    verification: schemas.EmailVerification,
    db: Session = Depends(get_db)
):
    """Verify user email with verification code"""
    return crud.verify_user_email(db=db, email=verification.email, verification_code=verification.verification_code)


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint to get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if email is verified
    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email first."
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@router.post("/refresh-token", response_model=schemas.Token)
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    email = verify_refresh_token(refresh_token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    new_refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token
    }


@router.post("/forgot-password")
async def forgot_password(
    request: schemas.PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    success = crud.request_password_reset(db=db, email=request.email)
    return {"message": "Password reset email sent successfully"}


@router.post("/verify-reset-code")
async def verify_reset_code(
    request: schemas.PasswordResetVerify,
    db: Session = Depends(get_db)
):
    """Verify password reset code"""
    crud.verify_password_reset_code(db=db, email=request.email, reset_code=request.reset_code)
    return {"message": "Reset code verified successfully"}


@router.post("/reset-password", response_model=schemas.User)
async def reset_password(
    request: schemas.PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Reset password with reset code"""
    # Check if passwords match
    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    return crud.reset_password(
        db=db, 
        email=request.email, 
        reset_code=request.reset_code, 
        new_password=request.new_password
    )
