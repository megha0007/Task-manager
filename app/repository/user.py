from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User  # Adjust import according to your project structure
from config.database import get_db
from helpers.common_helper import get_password_hash, verify_password, create_access_token , verify_access_token # Placeholder for your actual helper functions
from datetime import timedelta
from schemas import UserCreate,UserLogin,UserResponse
router = APIRouter()
# User Registration
@router.post("/register", tags=['User'],response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and create the user
    # print(user)
    hashed_password =get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(username=new_user.username, email=new_user.email)

# User Login
@router.post("/login",tags=['User'])
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # Fetch the user by username
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT token
    access_token_expires = timedelta(hours=1)  # Token expiry time
    access_token = create_access_token(data={"sub": existing_user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}

@router.get("/protected-resource",tags=['User'])
def protected_resource(current_user: User = Depends(verify_access_token)):
    return {"message": "This is a protected resource.", "user": current_user}

