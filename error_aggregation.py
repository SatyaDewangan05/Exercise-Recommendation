# error_aggregation.py

from datetime import datetime, timedelta
from pymongo import UpdateOne
from database import get_database

db = get_database()


def aggregate_errors_for_user(user_id, time_window=None):
    match_stage = {"user_id": user_id}
    if time_window:
        start_date = datetime.now() - timedelta(days=time_window)
        match_stage["started_at"] = {"$gte": start_date}

    pipeline = [
        {"$match": match_stage},
        {"$unwind": "$utterances"},
        {"$unwind": "$utterances.errors"},
        {"$group": {
            "_id": {
                "category": "$utterances.errors.category",
                "subcategory": "$utterances.errors.subcategory"
            },
            "frequency": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "category": "$_id.category",
            "subcategory": "$_id.subcategory",
            "frequency": 1
        }}
    ]

    return list(db.conversations.aggregate(pipeline))


def update_error_frequencies(user_id, aggregated_errors):
    bulk_operations = [
        UpdateOne(
            {
                "user_id": user_id,
                "category": error["category"],
                "subcategory": error["subcategory"]
            },
            {
                "$set": {
                    "frequency": error["frequency"],
                    "last_updated": datetime.now()
                }
            },
            upsert=True
        ) for error in aggregated_errors
    ]

    if bulk_operations:
        db.error_frequencies.bulk_write(bulk_operations)


def update_all_user_error_frequencies(time_window=30):
    for user in db.users.find({}, {"_id": 1}):
        aggregated_errors = aggregate_errors_for_user(user["_id"], time_window)
        update_error_frequencies(user["_id"], aggregated_errors)
