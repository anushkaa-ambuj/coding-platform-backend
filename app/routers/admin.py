from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database.mysql import get_db
from models import Challenge, TestCase
from pydantic import BaseModel
import boto3
import uuid
from typing import Optional

router = APIRouter()

# ------------ SCHEMAS ------------

class ChallengeModel(BaseModel):
    title: str
    description: str
    input_format: str
    output_format: str
    sample_input: str
    sample_output: str

class TestCaseModel(BaseModel):
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    is_hidden: bool = False

# ------------ ENDPOINTS ------------

@router.post("/challenges")
def create_challenge(data: ChallengeModel, db: Session = Depends(get_db)):
    new_challenge = Challenge(**data.dict())
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge

@router.post("/challenges/{challenge_id}/testcases")
def add_test_case(
    challenge_id: int,
    is_hidden: bool = Form(...),
    input_data: Optional[str] = Form(None),
    expected_output: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    s3_key = None

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
        if not input_data or not expected_output:
            raise HTTPException(status_code=400, detail="Visible test cases must include input_data and expected_output.")

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