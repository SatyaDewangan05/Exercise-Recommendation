# app.py

from flask import Flask, request, jsonify
from flask_caching import Cache
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from database import get_database
from schema import setup_mongodb_schema
from generate_dummy_data import generate_dummy_data
# from background_tasks import start_background_tasks
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import json

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)

# Configure caching
cache = Cache(app=app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

db = get_database()
setup_mongodb_schema()

# Setup logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route('/generate-dummy-data', methods=['POST'])
def gen_dummy_data():
    try:
        generate_dummy_data()
        return jsonify({'msg': 'success'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-exercise', methods=['POST'])
@limiter.limit("100 per minute")  # Adjust the rate limit as needed
# @cache.memoize(timeout=10)
def generate_exercise():
    try:
        user_id = request.json.get('user_id')

        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        user = db.users.find_one({"username": user_id})
        if not user:
            return jsonify({'error': 'No user found with this username'}), 404

        cache_key = f"top_errors:{user['_id']}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(json.loads(cached_result))

        top_errors = list(db.error_frequencies.find(
            {"user_id": ObjectId(user['_id'])}
        ).sort("frequency", -1))

        result = {
            'top_errors': [{
                "errorCategory": error["category"],
                "errorSubcategory": error["subcategory"],
                "errorFrequency": error["frequency"]
            } for error in top_errors],
        }

        cache.set(cache_key, json.dumps(result))
        return jsonify(result)

    except PyMongoError as e:
        app.logger.error(f"Database error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


if __name__ == '__main__':
    app.run(debug=True)
