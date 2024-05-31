from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import db, bcrypt
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('User already exists', 'danger')
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

        flash('Logged in successfully', 'success')
        return redirect(url_for('auth.login'))

    return render_template('login.html')