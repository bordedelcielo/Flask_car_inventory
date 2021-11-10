from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_app.forms import UserLoginForm # import the UserLogin Form that
# we just created in forms.html.
from car_app.models import db, User # import a user

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
    return render_template('signin.html')