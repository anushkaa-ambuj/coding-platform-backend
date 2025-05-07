# submission_model.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Submission(BaseModel):
    user_id: int
    challenge_id: int
    code: str
    language: str
    status: str = "Pending"
    output: Optional[str]
    error: Optional[str]
    execution_time: Optional[float]
    memory: Optional[int]
    submitted_at: datetime = datetime.utcnow()
