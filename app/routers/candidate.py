from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.mysql import get_db  # Corrected import
from models import Challenge, TestCase  # Corrected import

router = APIRouter()

@router.get("/challenges")
def get_all_challenges(db: Session = Depends(get_db)):
    return db.query(Challenge).all()

@router.get("/challenges/{challenge_id}")
def get_challenge_details(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    visible_cases = db.query(TestCase).filter(TestCase.challenge_id == challenge_id, TestCase.is_hidden == False).all()
    return {
        "challenge": challenge,
        "visible_test_cases": visible_cases
    }
