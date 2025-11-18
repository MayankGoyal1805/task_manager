import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity
)

# --- Database Setup ---
DATABASE_URI = 'mysql+pymysql://root:fantom%4090gm%28%29@127.0.0.1/task_manager'

# --- App Initialization ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- JWT Configuration ---
# I have CHANGED this key. This will invalidate all old tokens.
app.config["JWT_SECRET_KEY"] = "a-new-secret-key-to-force-a-reset"
jwt = JWTManager(app)  # Initialize JWTManager

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt

# --- MODELS ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', back_populates='creator')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum('todo', 'in_progress', 'done'), nullable=False, default='todo')
    due_date = db.Column(db.Date, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', back_populates='tasks')

# --- API ENDPOINTS ---

@app.route('/')
def hello_world():
    return "Hello! Your Task Manager API is running."

# --- AUTH ENDPOINTS ---

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "user_id": new_user.id
    }), 201

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

# --- SECURED TASK ENDPOINTS ---

@app.route('/api/tasks', methods=['GET', 'POST'])
@jwt_required()
def handle_tasks():
    current_user_id = get_jwt_identity()
    
    if request.method == 'POST':
        data = request.json
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            creator_id=current_user_id
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            "message": "Task created successfully",
            "task_id": new_task.id
        }), 201

    if request.method == 'GET':
        task_list = Task.query.filter_by(creator_id=current_user_id).all()
        tasks_json = []
        for task in task_list:
            tasks_json.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status
            })
        return jsonify(tasks=tasks_json)

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def handle_specific_task(task_id):
    current_user_id = get_jwt_identity()
    task_to_handle = Task.query.get_or_404(task_id)

    if task_to_handle.creator_id != current_user_id:
        return jsonify({"error": "Forbidden: You do not own this task"}), 403

    if request.method == 'DELETE':
        db.session.delete(task_to_handle)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    
    if request.method == 'PUT':
        data = request.json
        task_to_handle.title = data.get('title', task_to_handle.title)
        task_to_handle.description = data.get('description', task_to_handle.description)
        task_to_handle.status = data.get('status', task_to_handle.status)
        db.session.commit()
        return jsonify({
            "message": "Task updated successfully",
            "task_id": task_to_handle.id
        })

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)