# app.py
import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Candidates
CANDIDATES = [
    "Candidate A", 
    "Candidate B", 
    "Candidate C", 
    "Candidate D", 
    "Candidate E", 
    "Candidate F", 
    "Candidate G", 
    "Candidate H", 
    "Candidate I", 
    "Candidate J"
]

# In-memory storage
users = {}  # {username: {'password': hashed_password, 'has_voted': False}}
votes = {}  # {username: candidate}

def hash_password(password):
    """Create a secure hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Basic validation
        if not username or not password:
            flash('Username and password are required!')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        # Store user with hashed password
        users[username] = {
            'password': hash_password(password),
            'has_voted': False
        }
        
        flash('Registration successful! Please login.')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        if (username in users and 
            users[username]['password'] == hash_password(password)):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('vote'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    """Voting page"""
    if 'username' not in session:
        flash('Please login to vote')
        return redirect(url_for('index'))
    
    username = session['username']
    
    # Check if user has already voted
    if users[username]['has_voted']:
        flash('You have already voted!')
        return redirect(url_for('results'))
    
    if request.method == 'POST':
        candidate = request.form['candidate']
        
        if candidate not in CANDIDATES:
            flash('Invalid candidate selection')
            return redirect(url_for('vote'))
        
        # Record the vote
        votes[username] = candidate
        users[username]['has_voted'] = True
        
        flash(f'You have voted for {candidate}')
        return redirect(url_for('results'))
    
    return render_template('vote.html', candidates=CANDIDATES)

@app.route('/results')
def results():
    """Show voting results"""
    # Calculate vote counts
    vote_counts = {candidate: 0 for candidate in CANDIDATES}
    for vote in votes.values():
        vote_counts[vote] += 1
    
    # Calculate total votes
    total_votes = sum(vote_counts.values())
    
    return render_template('results.html', 
                           vote_counts=vote_counts, 
                           total_votes=total_votes, 
                           candidates=CANDIDATES)

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
