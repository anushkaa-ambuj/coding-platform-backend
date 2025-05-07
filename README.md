# 🧠 Online Coding Assessment Platform - Backend

This project is a scalable backend system for a coding assessment platform, designed using **FastAPI**, **MySQL**, **MongoDB**, **Celery**, **Redis**, **AWS S3**, and **Judge0**. It supports code execution, candidate evaluation, problem creation, and admin analytics.

---

## 🚀 Tech Stack

| Component      | Technology                          |
|----------------|-------------------------------------|
| Backend        | FastAPI (Python 3.9+)               |
| Auth           | JWT (OAuth2 Password Flow)          |
| Relational DB  | MySQL (Users, Problems, TestCases)  |
| NoSQL DB       | MongoDB (Submissions & Results)     |
| Task Queue     | Celery + Redis (async evaluation)   |
| Code Execution | Judge0 API                          |
| File Storage   | AWS S3 (Hidden Test Cases)          |
| Deployment     | Docker (Production-ready)           |

---

## 🗂️ Project Structure



## 🔐 Authentication

JWT-based system using FastAPI's `OAuth2PasswordBearer`.

- `POST /auth/register`: Register new user  
- `POST /auth/login`: Login and receive JWT token  


## 🧑‍💻 Candidate APIs

- `GET /candidate/challenges`: List all challenges  
- `GET /candidate/challenges/{id}`: Challenge details  
- `POST /candidate/submissions`: Submit code (triggers Celery)  
- `GET /candidate/submissions`: View past submissions  



## 🛠️ Admin APIs

- `POST /admin/challenges`: Create a challenge  
- `PUT /admin/challenges/{id}`: Update challenge  
- `POST /admin/challenges/{id}/testcases`: Upload test cases (S3)  
- `GET /admin/analytics`: Submission stats per challenge  


## 🧮 Database Schema

### MySQL

- **Users**  
- **Challenges**  
- **TestCases** (hidden cases stored in S3)  

### MongoDB

- **Submissions**

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/coding-platform-backend.git
cd coding-platform-backend
```

### 2️⃣ Install Dependencies
Make sure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```
### Configure Environment Variables
Create a .env file in the root directory with the following content:

ini
Copy code
MYSQL_URI=mysql://user:pass@localhost/db
MONGO_URI=mongodb://localhost:27017/
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=coding-platform-bucket
JUDGE0_URL=https://judge0.p.rapidapi.com/
JUDGE0_API_KEY=your_api_key
SECRET_KEY=your_jwt_secret
REDIS_URL=redis://localhost:6379/0
4️⃣ Run MySQL and MongoDB
Ensure MySQL and MongoDB are running locally. You can use Docker or native installations.

5️⃣ Run the FastAPI Application
bash
Copy code
uvicorn app.main:app --reload
6️⃣ 

📦 Docker Usage (Optional)
To containerize and run the application using Docker:

```bash
Copy code
docker build -t coding-backend .
docker run -p 8000:8000 coding-backend
```

📊 Future Improvements
🏆 Leaderboard and scoring system

🧠 Code similarity and plagiarism detection

🚫 Rate limiting and abuse protection

🎛️ Admin dashboard (React)

🌍 Multi-language support



