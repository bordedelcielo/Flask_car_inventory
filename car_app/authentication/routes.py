from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_app.forms import UserLoginForm # import the UserLogin Form that
# we just created in forms.html.
from car_app.models import db, User # import a user
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth',__name__, template_folder = 'auth_templates') # our blueprint

@auth.route('/signup',methods = ['GET', 'POST']) # signup, register, etc.
def signup():
    # return render_template('signup.html') # this was our original code
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email,password=password)
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account for {email}.', "user-created") 

            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please check your form...')

    return render_template('signup.html', form = form)

@auth.route('/signin',methods = ['GET', 'POST']) # signup, register, etc.
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))