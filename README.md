# Exercise Recommendation System

This project implements an AI-powered Exercise Recommendation System for language learners. It analyzes user conversations, tracks errors, and provides personalized exercise recommendations based on the user's most frequent mistakes.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)
8. [Performance Optimization](#performance-optimization)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing](#contributing)
12. [License](#license)

## Features

- User conversation analysis
- Error tracking and categorization
- Personalized exercise recommendations
- Background task for updating error frequencies
- Caching for improved performance
- RESTful API for exercise generation

## Prerequisites

- Python 3.7+
- MongoDB 4.0+
- Redis (for advanced caching)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/exercise-recommendation-system.git
   cd exercise-recommendation-system
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB:

   - Install MongoDB if you haven't already
   - Start the MongoDB service

5. Set up Redis:
   - Install Redis if you want to use it for caching
   - Start the Redis service
   ```
   sudo apt-get install redis-server
   sudo service redis-server start
   ```

## Configuration

1. Create a `.env` file in the project root and add the following configurations:

   ```
   MONGODB_URI
   ```

2. Adjust the configurations as needed for your environment.

## Usage

1. Set up the database schema:

   ```
   python schema.py
   ```

2. Generate dummy data (optional):

   ```
   python generate_dummy_data.py
   ```

3. Start the Flask application:

   ```
   python app.py
   ```

4. The application will be available at `http://localhost:5000`

## API Endpoints

### Generate Exercise

- **URL**: `/generate-exercise`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "user_id": "username"
  }
  ```
- **Response**:
  ```json
  {
    "top_errors": [
      {
        "category": "Grammar",
        "subcategory": "Subject-Verb Agreement",
        "frequency": 10
      },
      ...
    ],
    "page": 1,
    "per_page": 5,
    "total": 20
  }
  ```

## Database Schema

The system uses MongoDB with the following collections:

1. `users`: Stores user information
2. `conversations`: Stores user conversations and utterances
3. `error_frequencies`: Stores aggregated error frequencies for each user

For detailed schema information, refer to `schema.py`.

## Performance Optimization

- The system uses caching to improve response times for frequently accessed data.
- Background tasks update error frequencies periodically to reduce real-time computation.
- Batch processing is used for inserting and updating large amounts of data.
- Database indexes are created to optimize query performance.

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in your `.env` file.
2. Use a production WSGI server like Gunicorn:
   ```
   gunicorn app:app
   ```
3. Set up a reverse proxy (e.g., Nginx) to handle incoming requests.
4. Ensure your MongoDB and Redis instances are properly secured and optimized for production use.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
