# This will be inserted as a dict, not a SQLAlchemy model
# Sample structure:
{
  "user_id": 1,
  "challenge_id": 2,
  "code": "print('Hello')",
  "language": "python3",
  "status": "Passed",  # or "Failed", "Error"
  "result": {
    "stdout": "...",
    "stderr": "...",
    "time": "0.12",
    "memory": "128000"
  }
}
