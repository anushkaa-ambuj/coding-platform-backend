from fastapi import FastAPI
from routers import auth, admin, candidate, submissions

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(candidate.router, prefix="/candidate", tags=["Candidate"])
app.include_router(submissions.router, prefix="/submissions", tags=["Submissions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Online Coding Platform API"}

