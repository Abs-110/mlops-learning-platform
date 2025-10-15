from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mlops-learning-app-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mlops_learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_level = db.Column(db.String(20), default='beginner')
    current_module = db.Column(db.Integer, default=1)
    total_points = db.Column(db.Integer, default=0)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    external_resources = db.Column(db.Text, nullable=True)
    order_num = db.Column(db.Integer, nullable=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    quiz_score = db.Column(db.Integer, default=0)
    project_completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge_icon = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=False)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text, nullable=False)  # JSON string
    correct_answer = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.Text, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=True)
    solution = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's progress
    progress = Progress.query.filter_by(user_id=current_user.id).all()
    completed_modules = [p.module_id for p in progress if p.completed]
    
    # Get current module
    current_module = Module.query.filter_by(
        level=current_user.current_level,
        order_num=current_user.current_module
    ).first()
    
    # Get achievements
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.id).all()
    achievements = [Achievement.query.get(ua.achievement_id) for ua in user_achievements]
    
    return render_template('dashboard.html', 
                         current_module=current_module,
                         completed_modules=completed_modules,
                         achievements=achievements)

@app.route('/learn/<int:module_id>')
@login_required
def learn(module_id):
    module = Module.query.get_or_404(module_id)
    
    # Update last accessed
    progress = Progress.query.filter_by(
        user_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not progress:
        progress = Progress(user_id=current_user.id, module_id=module_id)
        db.session.add(progress)
    
    progress.last_accessed = datetime.utcnow()
    db.session.commit()
    
    # Get quiz questions
    quiz_questions = Quiz.query.filter_by(module_id=module_id).all()
    
    # Get project
    project = Project.query.filter_by(module_id=module_id).first()
    
    return render_template('learn.html', 
                         module=module,
                         quiz_questions=quiz_questions,
                         project=project)

@app.route('/complete_module', methods=['POST'])
@login_required
def complete_module():
    module_id = request.json.get('module_id')
    quiz_score = request.json.get('quiz_score', 0)
    
    progress = Progress.query.filter_by(
        user_id=current_user.id,
        module_id=module_id
    ).first()
    
    if progress:
        progress.completed = True
        progress.quiz_score = quiz_score
        db.session.commit()
        
        # Award points
        current_user.total_points += 10
        db.session.commit()
        
        # Check for achievements
        check_achievements(current_user.id)
        
        return jsonify({'success': True})
    
    return jsonify({'success': False})

def check_achievements(user_id):
    user = User.query.get(user_id)
    completed_modules = Progress.query.filter_by(user_id=user_id, completed=True).count()
    
    # First module completion
    if completed_modules >= 1:
        achievement = Achievement.query.filter_by(name='First Steps').first()
        if achievement and not UserAchievement.query.filter_by(
            user_id=user_id, achievement_id=achievement.id
        ).first():
            user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
            db.session.add(user_achievement)
    
    # Level completion achievements
    if completed_modules >= 4:  # Beginner level
        achievement = Achievement.query.filter_by(name='Beginner Master').first()
        if achievement and not UserAchievement.query.filter_by(
            user_id=user_id, achievement_id=achievement.id
        ).first():
            user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
            db.session.add(user_achievement)
    
    db.session.commit()

def initialize_data():
    """Initialize the database with sample data"""
    
    # Create modules
    modules_data = [
        {
            'level': 'beginner',
            'title': 'MLOps Fundamentals',
            'description': 'Learn the basics of MLOps and why it matters',
            'content': '''
            <h3>What is MLOps?</h3>
            <p>MLOps (Machine Learning Operations) is a set of practices that combines Machine Learning and DevOps to deploy and maintain ML systems in production reliably and efficiently.</p>
            
            <h3>Why MLOps Matters</h3>
            <p>Traditional software development has established practices for deployment and monitoring, but ML systems have unique challenges:</p>
            <ul>
                <li>Data dependencies and drift</li>
                <li>Model retraining needs</li>
                <li>Complex model validation</li>
                <li>Reproducibility challenges</li>
            </ul>
            
            <h3>MLOps Lifecycle</h3>
            <p>The MLOps lifecycle typically includes:</p>
            <ol>
                <li><strong>Data Management:</strong> Collection, validation, and preprocessing</li>
                <li><strong>Model Development:</strong> Training, validation, and packaging</li>
                <li><strong>Deployment:</strong> Model serving and infrastructure setup</li>
                <li><strong>Monitoring:</strong> Performance tracking and alerting</li>
                <li><strong>Retraining:</strong> Continuous model improvement</li>
            </ol>
            ''',
            'summary': 'MLOps bridges the gap between ML research and production deployment, ensuring reliable, scalable, and maintainable ML systems.',
            'external_resources': json.dumps([
                {'title': 'MLOps: Continuous delivery and automation pipelines in ML', 'url': 'https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning', 'type': 'article'},
                {'title': 'What is MLOps?', 'url': 'https://www.youtube.com/watch?v=9_BnHvm-5IY', 'type': 'video'},
                {'title': 'MLOps Best Practices', 'url': 'https://ml-ops.org/', 'type': 'resource'}
            ]),
            'order_num': 1
        },
        {
            'level': 'beginner',
            'title': 'ML Pipeline Basics',
            'description': 'Understand the fundamental components of ML pipelines',
            'content': '''
            <h3>ML Pipeline Components</h3>
            <p>A typical ML pipeline consists of several interconnected stages:</p>
            
            <h4>1. Data Ingestion</h4>
            <p>Raw data from various sources (databases, APIs, files) is collected and stored.</p>
            
            <h4>2. Data Preprocessing</h4>
            <p>Data cleaning, transformation, and feature engineering to prepare data for training.</p>
            
            <h4>3. Model Training</h4>
            <p>Using algorithms to learn patterns from the preprocessed data.</p>
            
            <h4>4. Model Validation</h4>
            <p>Testing model performance on unseen data to ensure quality.</p>
            
            <h4>5. Model Deployment</h4>
            <p>Making the trained model available for predictions in production.</p>
            
            <h4>6. Model Monitoring</h4>
            <p>Tracking model performance and data quality over time.</p>
            ''',
            'summary': 'ML pipelines automate the end-to-end process from raw data to deployed models, ensuring consistency and reproducibility.',
            'external_resources': json.dumps([
                {'title': 'ML Pipeline Design Patterns', 'url': 'https://www.kubeflow.org/docs/pipelines/', 'type': 'documentation'},
                {'title': 'Building ML Pipelines', 'url': 'https://www.youtube.com/watch?v=oF2Vh0LhJ0k', 'type': 'video'}
            ]),
            'order_num': 2
        }
    ]
    
    for module_data in modules_data:
        module = Module(**module_data)
        db.session.add(module)
    
    # Create achievements
    achievements_data = [
        {
            'name': 'First Steps',
            'description': 'Completed your first MLOps module',
            'badge_icon': '🎯',
            'requirements': 'Complete 1 module'
        },
        {
            'name': 'Beginner Master',
            'description': 'Completed all beginner level modules',
            'badge_icon': '🥉',
            'requirements': 'Complete 4 beginner modules'
        },
        {
            'name': 'Quiz Master',
            'description': 'Achieved 100% on a quiz',
            'badge_icon': '🧠',
            'requirements': 'Score 100% on any quiz'
        }
    ]
    
    for achievement_data in achievements_data:
        achievement = Achievement(**achievement_data)
        db.session.add(achievement)
    
    # Create sample quiz questions
    quiz_questions = [
        {
            'module_id': 1,
            'question': 'What does MLOps stand for?',
            'options': json.dumps(['Machine Learning Operations', 'Machine Learning Optimization', 'Machine Learning Organization', 'Machine Learning Orchestration']),
            'correct_answer': 0,
            'explanation': 'MLOps stands for Machine Learning Operations, combining ML and DevOps practices.'
        },
        {
            'module_id': 1,
            'question': 'Which of the following is NOT a typical MLOps lifecycle stage?',
            'options': json.dumps(['Data Management', 'Model Development', 'Software Testing', 'Model Monitoring']),
            'correct_answer': 2,
            'explanation': 'Software Testing is not a specific MLOps lifecycle stage, though testing is important throughout.'
        }
    ]
    
    for quiz_data in quiz_questions:
        quiz = Quiz(**quiz_data)
        db.session.add(quiz)
    
    # Create sample projects
    projects_data = [
        {
            'module_id': 1,
            'title': 'Your First MLOps Project',
            'description': 'Create a simple data pipeline using Python',
            'starter_code': '''
import pandas as pd
import numpy as np

# TODO: Load sample data
# TODO: Perform basic data cleaning
# TODO: Create a simple visualization

print("Welcome to your first MLOps project!")
            ''',
            'solution': '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load sample data
data = {'feature1': [1, 2, 3, 4, 5], 'feature2': [2, 4, 6, 8, 10], 'target': [1, 0, 1, 0, 1]}
df = pd.DataFrame(data)

# Basic data cleaning
print("Data shape:", df.shape)
print("Missing values:", df.isnull().sum())

# Create visualization
plt.figure(figsize=(8, 6))
plt.scatter(df['feature1'], df['feature2'], c=df['target'])
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Sample Data Visualization')
plt.show()

print("MLOps pipeline step 1 completed!")
            '''
        }
    ]
    
    for project_data in projects_data:
        project = Project(**project_data)
        db.session.add(project)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Module.query.count() == 0:
            initialize_data()
    app.run(debug=True)
