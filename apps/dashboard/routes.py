# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.dashboard import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/dashboard')
@login_required
def index_dashboard():
    # Example data; replace with actual queries
    tokens_left = 1000
    # Dummy data for notifications
    notifications = [
        {
            'date': '2024-10-21 13:15',
            'monitor_name': 'example.com',
            'message': 'Price dropped by 10%',
            'read': False
        },
        {
            'date': '2024-10-20 17:00',
            'monitor_name': 'another-site.com',
            'message': 'Product back in stock',
            'read': True
        },

    ]
    total_notifications = len(notifications)

    # Dummy data for active monitors
    monitors = [
        {
            'website': 'example.com',
            'check_frequency': 'Hourly'
        },
        {
            'website': 'another-site.com',
            'check_frequency': 'Daily'
        }
    ]
    total_monitors = len(monitors)


    return render_template(
        'dashboard/index.html',
        segment='index',
        total_notifications=total_notifications,
        tokens_left=tokens_left,
        notifications=notifications,
        monitors=monitors,
    )


@blueprint.route('/<template>')
@login_required
def route_template_dashboard(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/dashboard/FILE.html
        return render_template("dashboard/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('dashboard/page-404.html'), 404

    except:
        return render_template('dashboard/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
