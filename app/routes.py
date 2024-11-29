from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from sqlalchemy import text
import socket
import threading
import time
import random
from functools import wraps

bp = Blueprint('main', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # citizen or council

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20), nullable=False)  # public or council

def council_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'council':
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    if not User.query.filter_by(username='citizen').first():
        citizen = User(username='citizen', password='progress_day', role='citizen')
        council = User(username='councillor', password='hex_tech_secure', role='council')
        db.session.add(citizen)
        db.session.add(council)
        
        announcements = [
            Announcement(
                title='Welcome to Progress Day!',
                content='Join us in celebrating innovation and progress in our great city of Piltover!',
                level='public'
            ),
            Announcement(
                title='Hextech Crystal Exhibition',
                content='Visit the new Hextech Crystal exhibition at the Science Museum. Open to all citizens!',
                level='public'
            ),
            Announcement(
                title='URGENT: LFSR Communication System',
                content='Technical specifications for new encryption system:\n\n' +
                        'LFSR Configuration:\n' +
                        '- Initial State: [1, 0, 1, 0]\n' +
                        '- Feedback Function: state[0] ⊕ state[1] ⊕ state[2]\n' +
                        '- Port: 18739\n\n' +
                        'Test Messages:\n' +
                        '1. HEXTECH{test_message_1}\n' +
                        '2. Connect using: nc localhost 18739\n\n' +
                        'Note: Engineering suggests monitoring bit patterns in output stream.',
                level='council'
            ),
            Announcement(
                title='Security Notice: Message Format',
                content='All encrypted communications follow standard format:\n\n' +
                        '- Messages begin with "HEXTECH{"\n' +
                        '- Current messages in rotation:\n' +
                        '  * Test message\n' +
                        '  * Security protocol update\n' +
                        '  * Flag location status\n\n' +
                        'Warning: Initial analysis shows potential patterns in encrypted output.',
                level='council'
            ),
            Announcement(
                title='Engineering Report: LFSR Analysis',
                content='Preliminary findings on LFSR implementation:\n\n' +
                        '1. Feedback mechanism uses only first 3 bits\n' +
                        '2. State transitions show regular patterns\n' +
                        '3. Output sequence length shorter than expected\n\n' +
                        'Recommendation: Full security audit needed.',
                level='council'
            )
        ]
        
        for announcement in announcements:
            db.session.add(announcement)
        
        db.session.commit()

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/login')
def index():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    query = text(f"SELECT * FROM user WHERE username='{username}' AND password='{password}'")
    result = db.session.execute(query)
    user = result.fetchone()
    
    if user:
        session['role'] = user[3]
        if user[3] == 'council':
            return redirect(url_for('main.announcements', level='council'))
        return redirect(url_for('main.announcements', level='citizen'))
    
    return render_template('login.html', error="Invalid credentials")

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/announcements/<level>')
def announcements(level):
    if level == 'council' and ('role' not in session or session['role'] != 'council'):
        return redirect(url_for('main.security'))
    
    if level == 'council':
        announcements = Announcement.query.all()
    else:
        announcements = Announcement.query.filter_by(level='public').all()
    
    return render_template('announcements.html', 
                         announcements=announcements, 
                         level=level)

@bp.route('/security')
def security():
    return render_template('security.html', 
                         error="Access Denied: Council credentials required.")