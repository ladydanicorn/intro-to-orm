# Fitness Center Management API

A Flask-SQLAlchemy based REST API for managing a fitness center's members and workout sessions.

## Features

- Member management (CRUD operations)
- Workout session scheduling and tracking
- RESTful API endpoints
- MySQL database integration

## Installation

1. Clone the repository
```bash
git clone <https://github.com:ladydanicorn/intro-to-orm.git>    
cd intro_to_orm
```

2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure database
- Create a MySQL database named `fitness_center`
- Update the database URI in `app.py` with your credentials

## API Endpoints

### Members

- POST `/members` - Create a new member
```json
{
    "name": "John Doe",
    "email": "john@example.com"
}
```

- GET `/members` - Get all members
- GET `/members/<id>` - Get specific member
- PUT `/members/<id>` - Update member
- DELETE `/members/<id>` - Delete member

### Workout Sessions

- POST `/workouts` - Create workout session
```json
{
    "member_id": 1,
    "date": "2024-03-03 10:00:00",
    "workout_type": "Cardio",
    "duration": 60,
    "notes": "Treadmill and cycling"
}
```

- GET `/members/<id>/workouts` - Get member's workout sessions
- PUT `/workouts/<id>` - Update workout session

## Running the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

## Testing

Use Postman or curl to test the API endpoints. Example:

```bash
curl -X POST http://localhost:5000/members \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "email": "john@example.com"}'
```

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL Connector Python

## License

MIT License

## Author

Danielle Bronson for Coding Temple