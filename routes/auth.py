from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('First_name')
        last_name = request.form.get('Last_name')
        username = request.form.get('Username')
        email = request.form.get('Email')
        password = request.form.get('Password')

        # Check if the user already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('User already exists', 'danger')
            return redirect(url_for('auth.signup'))

        # Create a new user instance
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        session['user_id'] = user.id

        flash('Logged in successfully', 'success')
        return redirect(url_for('job_app'))  # Redirect to the job_app page

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Clear session data
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
