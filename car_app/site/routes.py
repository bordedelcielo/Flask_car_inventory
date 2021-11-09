from flask import Blueprint, render_template

"""
    In the below code, arguments are specified for
    Blueprint object creation. The first argument,
    'site', is the Blueprint's name. Flask uses
    this for routing.

    The second argument, __name__, is the Blueprint's
    import name. Flask uses this to locate the
    Blueprint's resources.
"""

site = Blueprint('site',__name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')