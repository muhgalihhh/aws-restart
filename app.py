from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///siakad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    class_id = db.Column(db.Integer, db.ForeignKey('school_class.id'))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    subject = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SchoolClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    academic_year = db.Column(db.String(20), nullable=False)
    students = db.relationship('Student', backref='school_class', lazy=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=1)

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('login'))

@app.route('/students')
def students():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        student = Student(
            nisn=request.form['nisn'],
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address'],
            gender=request.form['gender']
        )
        
        try:
            db.session.add(student)
            db.session.commit()
            flash('Siswa berhasil ditambahkan!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            flash('Error: Gagal menambahkan siswa!', 'error')
            db.session.rollback()
    
    return render_template('add_student.html')

@app.route('/teachers')
def teachers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

@app.route('/teachers/add', methods=['GET', 'POST'])
def add_teacher():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        teacher = Teacher(
            nip=request.form['nip'],
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address'],
            subject=request.form['subject']
        )
        
        try:
            db.session.add(teacher)
            db.session.commit()
            flash('Guru berhasil ditambahkan!', 'success')
            return redirect(url_for('teachers'))
        except Exception as e:
            flash('Error: Gagal menambahkan guru!', 'error')
            db.session.rollback()
    
    return render_template('add_teacher.html')

@app.route('/classes')
def classes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    classes = SchoolClass.query.all()
    return render_template('classes.html', classes=classes)

@app.route('/api/stats')
def api_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    stats = {
        'total_students': Student.query.count(),
        'total_teachers': Teacher.query.count(),
        'total_classes': SchoolClass.query.count(),
        'total_subjects': Subject.query.count()
    }
    
    return jsonify(stats)

def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@siakad.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)