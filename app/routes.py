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
    level = db.Column(db.String(20), nullable=False)
    show_connection = db.Column(db.Boolean, default=False)

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
                content='Join us in celebrating innovation and progress in our great city of Piltover! This year\'s theme focuses on the evolution of our communication systems.',
                level='public'
            ),
            Announcement(
                title='Legacy Systems Exhibition',
                content='Discover the history of Piltover\'s encryption methods at the Science Museum.\n\n' +
                        'Featured: The Linear Feedback Shift Register (LFSR) - A foundational technology that shaped our modern HextechCipher systems.',
                level='public'
            ),
            Announcement(
                title='WANTED: Jinx - Public Safety Alert',
                content='CAUTION: The criminal known as Jinx remains at large.\n\n' +
                        'Distinguishing Features:\n' +
                        '- Blue hair in long braids\n' +
                        '- Known for hextech-based explosives\n' +
                        '- Extremely dangerous\n\n' +
                        'Report any sightings immediately to Enforcer headquarters.\n\n' +
                        '<img src="/static/images/jinx.png" class="w-1/2 h-64 object-cover rounded-lg mb-4">\n\n' +
                        'DO NOT attempt to approach or apprehend.',
                level='public'
            ),
            Announcement(
                title='URGENT: HextechCipher Implementation',
                content='Technical specifications for new encryption system:\n\n' +
                        'Configuration:\n' +
                        '- Initial State: [1, 0, 1, 0]\n' +
                        '- Feedback Function: state[0] ⊕ state[1] ⊕ state[2]\n'
                        'Test Messages:\n' +
                        '1. HEXTECH{test_message_1}\n',
                level='council'
            ),
            Announcement(
                title='Security Protocol Update',
                content='All encrypted communications follow standard format:\n\n' +
                        '- Messages begin with "HEXTECH{"\n' +
                        '- Messages are encrypted using state-based transformation\n' +
                        '- Regular message rotation implemented\n\n' +
                        'Note: System shows predictable behavior after initial state.',
                level='council'
            ),
            Announcement(
                title='Initial Testing Progress',
                content='Jayce has begun testing the capabilities of the newly established protocol.\n\n' +
                        'Configuration information is highly confidential and must be protected at all costs."\n' +
                        'We are still securing the protocol behavior, configuration details are highly classified and\n' +
                        'must be protected at all costs.\n\n',
                level='council',
                show_connection=True
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