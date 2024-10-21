from apps.email import blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_mail import Message
from .forms import NewsletterForm
#from apps import mail  # Import the mail instance
from models import db, NewsletterSubscriber
from itsdangerous import URLSafeTimedSerializer
from flask import current_app


@blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = NewsletterForm()
    if form.validate_on_submit():
        email_address = form.email.data
        # Check if the email is already subscribed
        existing_subscriber = NewsletterSubscriber.query.filter_by(email=email_address).first()
        if existing_subscriber:
            flash('This email is already subscribed.', 'info')
            return redirect(url_for('email_blueprint.subscribe'))

        # Generate a confirmation token
        # Serializer for generating confirmation tokens
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email_address, salt='email-confirmation-salt')

        # Send confirmation email
        confirm_url = url_for('email_blueprint.confirm_subscription', token=token, _external=True)
        html = render_template('email/newsletter_confirmation.html', confirm_url=confirm_url)
        subject = "Confirm your subscription"
        send_email(email_address, subject, html)

        flash('A confirmation email has been sent. Please check your inbox.', 'success')
        return redirect(url_for('home_blueprint.index'))
    return render_template('email/subscribe.html', form=form)

# Route to confirm the subscription
from itsdangerous import SignatureExpired, BadSignature

@blueprint.route('/newsletter/confirm/<token>')
def confirm_subscription(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email_address = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except SignatureExpired:
        flash('The confirmation link has expired.', 'danger')
        return redirect(url_for('email_blueprint.subscribe'))
    except BadSignature:
        flash('Invalid confirmation token.', 'danger')
        return redirect(url_for('email_blueprint.subscribe'))

    # Add the subscriber to the database
    new_subscriber = NewsletterSubscriber(email=email_address)
    db.session.add(new_subscriber)
    db.session.commit()
    flash('Your subscription has been confirmed!', 'success')
    return redirect(url_for('home_blueprint.index'))

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

    
# @email_blueprint.route('/test-email')
# def test_email():
#     msg = Message(
#         'Test Email from Flask',
#         sender=current_app.config['MAIL_DEFAULT_SENDER'],
#         recipients=['larl@live.dk'],  # Replace with your personal email to receive the test email
#         body='This is a test email sent from Flask using AWS WorkMail SMTP settings.'
#     )
#     try:
#         mail.send(msg)
#         return 'Email sent successfully!'
#     except Exception as e:
#         return f'An error occurred: {e}'
