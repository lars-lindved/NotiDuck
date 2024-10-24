from apps.email import blueprint
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_mail import Message
from apps import mail  # Import the mail instance from apps/__init__.py
from apps.models import db, NewsletterSubscriber, User 
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_login import current_user, login_required  # Import current_user
from .forms import NewsletterForm
from datetime import datetime


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

@blueprint.route('/subscribe', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access
def subscribe():
    email_address = current_user.email  # Get the email from the logged-in user

    # Check if the email is already subscribed
    existing_subscriber = NewsletterSubscriber.query.filter_by(email=email_address).first()
    if existing_subscriber:
        flash('You are already subscribed to the newsletter.', 'info')
        return redirect(url_for('dashboard_blueprint.index_dashboard'))

    # Generate a confirmation token
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email_address, salt='email-confirmation-salt')

    # Send confirmation email
    confirm_url = url_for('email_blueprint.confirm_subscription', token=token, _external=True)
    html = render_template('email/newsletter_confirmation.html', confirm_url=confirm_url)
    subject = "Confirm your subscription"
    send_email(email_address, subject, html)

    flash('A confirmation email has been sent. Please check your inbox.', 'success')
    return redirect(url_for('dashboard_blueprint.index_dashboard'))

@blueprint.route('/newsletter/confirm/<token>')
def confirm_subscription(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email_address = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except SignatureExpired:
        flash('The confirmation link has expired.', 'danger')
        return redirect(url_for('dashboard_blueprint.index_dashboard'))
    except BadSignature:
        flash('Invalid confirmation token.', 'danger')
        return redirect(url_for('dashboard_blueprint.index_dashboard'))

    # Add the subscriber to the database
    existing_subscriber = NewsletterSubscriber.query.filter_by(email=email_address).first()
    if not existing_subscriber:
        new_subscriber = NewsletterSubscriber(email=email_address)
        db.session.add(new_subscriber)
        db.session.commit()
        flash('Your subscription has been confirmed!', 'success')
    else:
        flash('You are already subscribed.', 'info')

    return redirect(url_for('dashboard_blueprint.index_dashboard'))
