from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pikapika07$@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    workout_sessions = db.relationship('WorkoutSession', backref='member', lazy=True)

class WorkoutSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)  # Duration in minutes
    notes = db.Column(db.Text)

# Schemas for serialization
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'join_date', 'active')

class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'workout_type', 'duration', 'notes')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Member Routes
@app.route('/members', methods=['POST'])
def add_member():
    try:
        name = request.json['name']
        email = request.json['email']
        
        new_member = Member(name=name, email=email)
        db.session.add(new_member)
        db.session.commit()
        
        return member_schema.jsonify(new_member), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route('/members/<id>', methods=['GET'])
def get_member(id):
    member = Member.query.get_or_404(id)
    return member_schema.jsonify(member)

@app.route('/members/<id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get_or_404(id)
    
    try:
        member.name = request.json.get('name', member.name)
        member.email = request.json.get('email', member.email)
        member.active = request.json.get('active', member.active)
        
        db.session.commit()
        return member_schema.jsonify(member)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/members/<id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({"message": "Member deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Workout Session Routes
@app.route('/workouts', methods=['POST'])
def add_workout():
    try:
        member_id = request.json['member_id']
        date = datetime.strptime(request.json['date'], '%Y-%m-%d %H:%M:%S')
        workout_type = request.json['workout_type']
        duration = request.json['duration']
        notes = request.json.get('notes', '')
        
        new_workout = WorkoutSession(
            member_id=member_id,
            date=date,
            workout_type=workout_type,
            duration=duration,
            notes=notes
        )
        
        db.session.add(new_workout)
        db.session.commit()
        
        return workout_session_schema.jsonify(new_workout), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/members/<id>/workouts', methods=['GET'])
def get_member_workouts(id):
    Member.query.get_or_404(id)  # Check if member exists
    workouts = WorkoutSession.query.filter_by(member_id=id).all()
    return workout_sessions_schema.jsonify(workouts)

@app.route('/workouts/<id>', methods=['PUT'])
def update_workout(id):
    workout = WorkoutSession.query.get_or_404(id)
    
    try:
        if 'date' in request.json:
            workout.date = datetime.strptime(request.json['date'], '%Y-%m-%d %H:%M:%S')
        workout.workout_type = request.json.get('workout_type', workout.workout_type)
        workout.duration = request.json.get('duration', workout.duration)
        workout.notes = request.json.get('notes', workout.notes)
        
        db.session.commit()
        return workout_session_schema.jsonify(workout)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)