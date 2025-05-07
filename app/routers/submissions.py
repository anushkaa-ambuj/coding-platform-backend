from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import requests, time, os
from bson.objectid import ObjectId

router = APIRouter()

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["code_platform"]
submissions = db["submissions"]

JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
JUDGE0_HEADERS = {
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
    "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
    "Content-Type": "application/json"
}

class SubmissionModel(BaseModel):
    user_id: int
    challenge_id: int
    language_id: int  # e.g., 71 for Python 3
    source_code: str
    stdin: str = ""

@router.post("/")
def submit_code(data: SubmissionModel):
    judge_payload = {
        "source_code": data.source_code,
        "language_id": data.language_id,
        "stdin": data.stdin
    }
    judge_res = requests.post(JUDGE0_URL + "?base64_encoded=false&wait=false",
                              headers=JUDGE0_HEADERS, json=judge_payload)
    if judge_res.status_code != 201:
        raise HTTPException(status_code=500, detail="Judge0 submission failed")

    token = judge_res.json().get("token")
    result = None
    for _ in range(10):
        res = requests.get(f"{JUDGE0_URL}/{token}?base64_encoded=false", headers=JUDGE0_HEADERS)
        if res.json().get("status", {}).get("id") in [1, 2]:  # In queue or processing
            time.sleep(2)
        else:
            result = res.json()
            break

    submission_data = {
        "user_id": data.user_id,
        "challenge_id": data.challenge_id,
        "language_id": data.language_id,
        "source_code": data.source_code,
        "stdin": data.stdin,
        "status": result.get("status"),
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr"),
        "created_at": time.time()
    }
    insert_result = submissions.insert_one(submission_data)
    return {"submission_id": str(insert_result.inserted_id), "result": result}

@router.get("/{submission_id}")
def get_submission(submission_id: str):
    result = submissions.find_one({"_id": ObjectId(submission_id)})
    if not result:
        raise HTTPException(status_code=404, detail="Submission not found")
    result["_id"] = str(result["_id"])
    return result
