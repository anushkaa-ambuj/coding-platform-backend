# Online Coding Assessment Platform - Backend

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

```ini
MYSQL_URI=mysql://user:pass@localhost/db
MONGO_URI=mongodb://localhost:27017/
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_BUCKET_NAME=coding-platform-bucket
JUDGE0_URL=https://judge0.p.rapidapi.com/
JUDGE0_API_KEY=your_api_key
SECRET_KEY=your_jwt_secret
REDIS_URL=redis://localhost:6379/0
```

### 4️⃣ Run MySQL and MongoDB
Ensure MySQL and MongoDB are running locally. You can use Docker or native installations.

### 5️⃣ Run the FastAPI Application
Start the FastAPI application:

```bash
fastapi dev app/main.py
```

### 6️⃣ Kafka Producer (Publish Tasks)
Kafka producers will push tasks into a Kafka topic, which will be consumed by Kafka consumers to process background tasks. You can implement Kafka producer logic inside your FastAPI routes or services.

Example producer (for code execution tasks):

```python
from kafka import KafkaProducer
import json
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_code_execution_task(task_data):
    producer.send(KAFKA_TOPIC, task_data)
    producer.flush()
```

### 7️⃣ Kafka Consumer (Process Tasks)
Kafka consumers will listen for tasks and process them asynchronously. This could be handled by a separate process running in the background.

Example consumer (for code execution processing):

```python
from kafka import KafkaConsumer
import json
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def process_code_execution_task(task_data):
    # Your code execution logic here
    pass

for message in consumer:
    task_data = message.value
    process_code_execution_task(task_data)
Run the consumer script as a separate process or service.
```


## 🧪 Test Case Management
- ✅ Public test cases are stored in MySQL and visible to users.

- 🔒 Hidden test cases are uploaded to AWS S3, and their S3 keys are referenced in the database.



## 📦 Docker Usage (Optional)
To containerize and run the application using Docker:

```bash
Copy code
docker build -t coding-backend .
docker run -p 8000:8000 coding-backend
```

## 📊 Future Improvements
- 🏆 Leaderboard and scoring system

- 🧠 Code similarity and plagiarism detection

- 🚫 Rate limiting and abuse protection

- 🎛️ Admin dashboard (React)

- 🌍 Multi-language support



