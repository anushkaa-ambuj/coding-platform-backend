# -------------------- MODULE IMPORTS --------------------
import sys
import os

# Add the parent directory to the system path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# FastAPI modules for building APIs and handling security/auth
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Pydantic models for data validation
from pydantic import BaseModel, EmailStr

# SQLAlchemy session for database operations
from sqlalchemy.orm import Session
from database.mysql_db import get_db  # function to get DB session

# ORM model representing the User table
from models import User

# For password hashing
from passlib.context import CryptContext

# For encoding/decoding JWT tokens
from jose import JWTError, jwt

# For token expiry and environment variables
import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a FastAPI router for defining related endpoints
router = APIRouter()

# -------------------- AUTH CONFIGURATION --------------------

# Load the secret key for JWT from environment variables
SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable is not set")

# Define the algorithm and expiration time for JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Set up password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup OAuth2 password bearer token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------- DATA MODELS (SCHEMAS) --------------------

# Model for user registration input
class RegisterModel(BaseModel):
    username: str
    email: EmailStr
    password: str

# Model for user login input
class LoginModel(BaseModel):
    email: EmailStr
    password: str

# Model for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# -------------------- ROUTES --------------------

# POST endpoint to register a new user
@router.post("/register")
def register_user(data: RegisterModel, db: Session = Depends(get_db)):
    # Check if a user with the given email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password securely
    hashed_pw = pwd_context.hash(data.password)
    
    # Create a new User object and add it to the database
    new_user = User(username=data.username, email=data.email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

# POST endpoint to log in a user and return a JWT access token
@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginModel, db: Session = Depends(get_db)):
    # Look for the user with the provided email
    user = db.query(User).filter(User.email == data.email).first()
    
    # Validate password; raise error if credentials are invalid
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Set token expiration time
    expiration = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create payload and encode JWT
    payload = {"sub": str(user.id), "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Return access token
    return {"access_token": token, "token_type": "bearer"}
