from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch
from .forms import UpdateProfile,PitchesForm
from .. import db


@main.route('/')
def index():

    return render_template('index.html')


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    pitches=Pitch.query.filter_by(user_id=user.id)

    return render_template("profile/profile.html", user = user, pitches=pitches)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, user=user)



@main.route('/new-pitch', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchesForm()    
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category_opts.data
        upvote=0
        downvote=0       

        # Updated pitch instance
        this_pitch = Pitch(pitch_title=title, pitch_text=pitch, category=category, upvotes=upvote, downvotes=downvote, user=current_user)

        # save pitch method
        this_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New Pitch'
    return render_template('new_pitch.html',title = title, pitch_form=form)

