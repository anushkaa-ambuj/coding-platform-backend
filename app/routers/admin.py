# Importing necessary modules from FastAPI, SQLAlchemy, and AWS SDK
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database.mysql_db import get_db  # Dependency to get the DB session
from models import Challenge, TestCase  # SQLAlchemy models for the database
from pydantic import BaseModel  # For request validation
import boto3  # AWS SDK to interact with S3
import uuid  # To generate unique keys for S3
from typing import Optional

# Creating a router object to define endpoints for challenges and test cases
router = APIRouter()

# ------------ SCHEMAS ------------

# Pydantic schema for Challenge model
class ChallengeModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    time_limit: Optional[int] = None
    memory_limit: Optional[int] = None

# Pydantic schema for TestCase model
class TestCaseModel(BaseModel):
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    is_hidden: bool = False

# ------------ ENDPOINTS ------------

# Create a new challenge
@router.post("/challenges")
def create_challenge(data: ChallengeModel, db: Session = Depends(get_db)):
    new_challenge = Challenge(**data.dict())  # Map fields to DB model
    db.add(new_challenge)                     # Add to DB session
    db.commit()                               # Commit transaction
    db.refresh(new_challenge)                 # Refresh instance with updated info (e.g., auto-generated ID)
    return new_challenge

# Edit/update an existing challenge
@router.put("/challenges/{challenge_id}")
def edit_challenge(
    challenge_id: int, 
    data: ChallengeModel, 
    db: Session = Depends(get_db)
):
    # Find challenge by ID
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    # If not found, return 404
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Update only provided fields
    if data.title is not None:
        challenge.title = data.title
    if data.description is not None:
        challenge.description = data.description
    if data.difficulty is not None:
        challenge.difficulty = data.difficulty
    if data.time_limit is not None:
        challenge.time_limit = data.time_limit
    if data.memory_limit is not None:
        challenge.memory_limit = data.memory_limit
    
    db.commit()
    db.refresh(challenge)
    
    return challenge

# Delete an existing challenge
@router.delete("/challenges/{challenge_id}")
def delete_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    db.delete(challenge)
    db.commit()
    return {"message": "Challenge deleted successfully"}

# Add a test case (visible or hidden) to a challenge
@router.post("/challenges/{challenge_id}/testcases")
def add_test_case(
    challenge_id: int,
    is_hidden: bool = Form(...),
    input_data: Optional[str] = Form(None),
    expected_output: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    s3_key = None  # Default key (for visible test cases)

    # If it's a hidden test case, upload the file to S3
    if is_hidden:
        if not file:
            raise HTTPException(status_code=400, detail="Hidden test case must include a file.")
        s3 = boto3.client("s3")
        s3_key = f"hidden_cases/{uuid.uuid4()}.txt"
        try:
            s3.upload_fileobj(file.file, "your-s3-bucket", s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")
    else:
        # Visible test cases must include input and output
        if not input_data or not expected_output:
            raise HTTPException(status_code=400, detail="Visible test cases must include input_data and expected_output.")

    # Create and store the test case
    new_case = TestCase(
        challenge_id=challenge_id,
        input_data=input_data,
        expected_output=expected_output,
        is_hidden=is_hidden,
        s3_key=s3_key
    )
    db.add(new_case)
    db.commit()
    return {"message": "Test case added successfully"}

# Edit an existing test case
@router.put("/challenges/{challenge_id}/testcases/{test_case_id}")
def edit_test_case(
    challenge_id: int, 
    test_case_id: int, 
    is_hidden: bool = Form(...),
    input_data: Optional[str] = Form(None),
    expected_output: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    test_case = db.query(TestCase).filter(
        TestCase.id == test_case_id, 
        TestCase.challenge_id == challenge_id
    ).first()

    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    # Update test case details
    test_case.is_hidden = is_hidden
    test_case.input_data = input_data
    test_case.expected_output = expected_output

    # If it's a hidden test case and file is provided, upload new file to S3
    if is_hidden and file:
        s3 = boto3.client("s3")
        s3_key = f"hidden_cases/{uuid.uuid4()}.txt"
        try:
            s3.upload_fileobj(file.file, "your-s3-bucket", s3_key)
            test_case.s3_key = s3_key
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")
    
    db.commit()
    db.refresh(test_case)
    return {"message": "Test case updated successfully"}

# Delete a test case from a challenge
@router.delete("/challenges/{challenge_id}/testcases/{test_case_id}")
def delete_test_case(challenge_id: int, test_case_id: int, db: Session = Depends(get_db)):
    test_case = db.query(TestCase).filter(
        TestCase.id == test_case_id, 
        TestCase.challenge_id == challenge_id
    ).first()

    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")

    # If it's a hidden test case, delete the associated file from S3
    if test_case.is_hidden and test_case.s3_key:
        s3 = boto3.client("s3")
        try:
            s3.delete_object(Bucket="your-s3-bucket", Key=test_case.s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete from S3: {str(e)}")
    
    db.delete(test_case)
    db.commit()
    return {"message": "Test case deleted successfully"}
