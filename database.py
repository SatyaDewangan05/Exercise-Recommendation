from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

db = None


def get_database():
    global db
    if db is None:
        client = MongoClient(os.getenv('MONGO_URI'))
        db = client['exercise_recommendation']
        print('Connected to DB')
    return db

# db.users.create_index([("username", 1)], unique=True)
# db.conversations.create_index([("user_id", 1), ("started_at", -1)])
# db.error_frequencies.create_index([("user_id", 1), ("frequency", -1)])
