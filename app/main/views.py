from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment
from .forms import UpdateProfile,PitchesForm,CommentForm,UpvoteForm,DownvoteForm
from .. import db


@main.route('/')
def index():
    pitches=Pitch.query.order_by(Pitch.posted.desc())      
    return render_template('index.html', pitches=pitches)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    pitches=Pitch.query.filter_by(user_id=user.id).order_by(Pitch.posted.desc())

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

    pitches=Pitch.query.filter_by(user_id=user.id).order_by(Pitch.posted.desc())

    return render_template('profile/update.html',form =form, user=user, pitches=pitches)



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


@main.route('/pitch/category/<cat>')
def category(cat):
    pitches=Pitch.query.filter_by(category=cat).order_by(Pitch.posted.desc())   
    title=pitches[0].category.capitalize()
    return render_template('category.html', title=title, pitches=pitches)



@main.route('/pitch/comment/<pitch_id>',methods = ['GET','POST'])
@login_required
def comment(pitch_id):
    pitch=Pitch.query.filter_by(id=pitch_id).first()
    form = CommentForm()
    form1 = UpvoteForm()
    form2 = DownvoteForm()    
    if form.validate_on_submit():
        new_comment = form.comment.data             

        # Updated comment instance
        this_comment = Comment(comment_text=new_comment,pitch=pitch, user=current_user)

        # save comment method
        this_comment.save_comment()
        return redirect(url_for('.comment', pitch_id=pitch_id))

    if form1.validate_on_submit() and form1.upvote.data:
        pitch.upvotes+=1
        db.session.commit()
        return redirect(url_for('.comment', pitch_id=pitch_id))

    elif form2.validate_on_submit() and form2.downvote.data:
        pitch.downvotes+=1
        db.session.commit()
        return redirect(url_for('.comment', pitch_id=pitch_id))

    comments=Comment.query.filter_by(pitch_id=pitch_id).order_by(Comment.posted.desc())  
    title = pitch.pitch_title
    return render_template('new_comment.html',title = title, comments=comments, comment_form=form, pitch=pitch, upvote_form=form1, downvote_form=form2)

