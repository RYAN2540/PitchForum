from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required

from . import auth
from ..models import User,Pitch
from .forms import RegistrationForm,LoginForm
from .. import db
from ..email import mail_message


@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to PitchForum!","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    pitches=Pitch.query.order_by(Pitch.posted.desc())
    top_pitch=Pitch.query.order_by(Pitch.upvotes.desc()).first()
    title = "Sign up"
    return render_template('auth/register.html',registration_form = form, title=title, pitches=pitches, top_pitch=top_pitch)


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')
    
    top_pitch=Pitch.query.order_by(Pitch.upvotes.desc()).first()
    pitches=Pitch.query.order_by(Pitch.posted.desc())
    title = "Log in"
    return render_template('auth/login.html',login_form = login_form,title=title, pitches=pitches, top_pitch=top_pitch)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))