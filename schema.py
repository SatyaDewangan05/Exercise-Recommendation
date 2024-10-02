from pymongo import ASCENDING, DESCENDING
from database import get_database


def setup_mongodb_schema():
    # Connect to MongoDB
    db = get_database()

    # Users Collection
    if "users" not in db.list_collection_names():
        db.create_collection("users", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["username", "created_at"],
                "properties": {
                    "username": {
                        "bsonType": "string"
                    },
                    "created_at": {
                        "bsonType": "date"
                    }
                }
            }
        })

    # Conversations Collection
    if "conversations" not in db.list_collection_names():
        db.create_collection("conversations", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["user_id", "started_at", "utterances"],
                "properties": {
                    "user_id": {
                        "bsonType": "objectId"
                    },
                    "started_at": {
                        "bsonType": "date"
                    },
                    "utterances": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["text", "timestamp", "errors"],
                            "properties": {
                                "text": {
                                    "bsonType": "string"
                                },
                                "timestamp": {
                                    "bsonType": "date"
                                },
                                "errors": {
                                    "bsonType": "array",
                                    "items": {
                                        "bsonType": "object",
                                        "required": ["category", "subcategory"],
                                        "properties": {
                                            "category": {
                                                "enum": ["Grammar", "Vocabulary", "Pronunciation", "Fluency"]
                                            },
                                            "subcategory": {
                                                "bsonType": "string"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        })

    # Error Frequencies Collection
    if "error_frequencies" not in db.list_collection_names():
        db.create_collection("error_frequencies", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["user_id", "category", "subcategory", "frequency", "last_updated"],
                "properties": {
                    "user_id": {
                        "bsonType": "objectId"
                    },
                    "category": {
                        "enum": ["Grammar", "Vocabulary", "Pronunciation", "Fluency"]
                    },
                    "subcategory": {
                        "bsonType": "string"
                    },
                    "frequency": {
                        "bsonType": "int"
                    },
                    "last_updated": {
                        "bsonType": "date"
                    }
                }
            }
        })

    # Create indexes
    db.users.create_index([("username", ASCENDING)], unique=True)
    db.conversations.create_index(
        [("user_id", ASCENDING), ("started_at", DESCENDING)])
    db.error_frequencies.create_index(
        [("user_id", ASCENDING), ("frequency", DESCENDING)])

    print("MongoDB schema setup completed.")


# def setup_mongodb_schema():
#     # Connect to MongoDB
#     db = get_database()

#     # Add indexes
#     db.users.create_index("username", unique=True)
#     db.conversations.create_index([("user_id", 1), ("started_at", -1)])
#     db.error_frequencies.create_index([("user_id", 1), ("frequency", -1)])
#     db.error_frequencies.create_index(
#         [("user_id", 1), ("category", 1), ("subcategory", 1)], unique=True)

#     print("MongoDB schema and indexes setup completed.")


if __name__ == "__main__":
    setup_mongodb_schema()
