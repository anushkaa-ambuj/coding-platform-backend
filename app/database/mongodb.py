from motor.motor_asyncio import AsyncIOMotorClient

# Replace with your actual URI
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "yourdbname"

client = AsyncIOMotorClient(MONGO_URI)
mongodb = client[MONGO_DB_NAME]
