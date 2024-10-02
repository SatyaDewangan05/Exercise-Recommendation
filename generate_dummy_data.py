import random
from datetime import datetime, timedelta
from database import get_database
from bson import ObjectId
from tqdm import tqdm
from pymongo import UpdateMany

# Connect to MongoDB
db = get_database()


def generate_dummy_data(num_users=10, conversations_per_user=5, utterances_per_conversation=10):
    # Clear existing data
    db.users.delete_many({})
    db.conversations.delete_many({})
    db.error_frequencies.delete_many({})

    error_categories = ["Grammar", "Vocabulary", "Pronunciation", "Fluency"]
    error_subcategories = {
        "Grammar": ["Subject-Verb Agreement", "Tense", "Article Usage", "Preposition"],
        "Vocabulary": ["Wrong Word Choice", "Collocation", "Idiomatic Expression", "Academic Vocabulary"],
        "Pronunciation": ["Vowel Sound", "Consonant Sound", "Word Stress", "Intonation"],
        "Fluency": ["Hesitation", "Repetition", "Filler Words", "Sentence Structure"]
    }

    users = []
    conversations = []
    error_frequencies = {}

    # Generate users
    for i in tqdm(range(num_users)):
        user = {
            "_id": ObjectId(),
            "username": f"user{i+1}",
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365))
        }
        users.append(user)

        # Generate conversations for each user
        for j in range(conversations_per_user):
            conversation = {
                "user_id": user["_id"],
                "started_at": datetime.now() - timedelta(days=random.randint(1, 30)),
                "utterances": []
            }

            # Generate utterances for each conversation
            for k in range(utterances_per_conversation):
                utterance = {
                    "text": f"This is utterance {k+1} in conversation {j+1} for user {i+1}",
                    "timestamp": conversation["started_at"] + timedelta(minutes=k*2),
                    "errors": []
                }

                # Generate random errors for each utterance
                num_errors = random.randint(0, 3)
                for _ in range(num_errors):
                    category = random.choice(error_categories)
                    subcategory = random.choice(error_subcategories[category])
                    utterance["errors"].append({
                        "category": category,
                        "subcategory": subcategory
                    })

                    # Update error frequencies
                    error_key = (user["_id"], category, subcategory)
                    if error_key in error_frequencies:
                        error_frequencies[error_key] += 1
                    else:
                        error_frequencies[error_key] = 1

                conversation["utterances"].append(utterance)

            conversations.append(conversation)

    # Bulk insert users and conversations
    db.users.insert_many(users)
    db.conversations.insert_many(conversations)

    # Bulk update error frequencies
    error_freq_updates = [
        UpdateMany(
            {"user_id": user_id, "category": category, "subcategory": subcategory},
            {"$set": {"frequency": frequency, "last_updated": datetime.now()}},
            upsert=True
        )
        for (user_id, category, subcategory), frequency in error_frequencies.items()
    ]

    if error_freq_updates:
        db.error_frequencies.bulk_write(error_freq_updates)

    print("Dummy data generation completed.")


if __name__ == "__main__":
    generate_dummy_data(num_users=1000, conversations_per_user=10,
                        utterances_per_conversation=100)
