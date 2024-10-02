# background_tasks.py

from apscheduler.schedulers.background import BackgroundScheduler
from error_aggregation import update_error_frequencies, aggregate_errors_for_user
from database import get_database

db = get_database()


def update_user_batch(user_ids, time_window=30):
    for user_id in user_ids:
        aggregated_errors = aggregate_errors_for_user(user_id, time_window)
        update_error_frequencies(user_id, aggregated_errors)


def update_all_user_error_frequencies(time_window=30, batch_size=100):
    user_cursor = db.users.find({}, {"_id": 1}).batch_size(batch_size)
    user_batch = []

    for user in user_cursor:
        user_batch.append(user["_id"])
        if len(user_batch) == batch_size:
            update_user_batch(user_batch, time_window)
            user_batch = []

    if user_batch:
        update_user_batch(user_batch, time_window)


def start_background_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_all_user_error_frequencies, 'interval', hours=24)
    scheduler.start()
