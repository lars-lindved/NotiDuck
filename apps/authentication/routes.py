# apps/authentication/routes.py

from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from apps import db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.models import User  # Import User from apps.models
from apps.authentication.util import verify_pass


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('dashboard_blueprint.index_dashboard'))

        # Invalid credentials
        flash('Wrong username or password', 'danger')
        return render_template('accounts/login.html', form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('dashboard_blueprint.index_dashboard'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already registered', 'warning')
            return render_template('accounts/register.html', form=create_account_form)

        # Check if email exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', 'warning')
            return render_template('accounts/register.html', form=create_account_form)

        # Create new user
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        # Log in the user
        login_user(user)
        return redirect(url_for('dashboard_blueprint.index_dashboard'))

    return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))
