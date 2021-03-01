from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write a bio.',validators = [Required()])
    submit = SubmitField('Submit')


class PitchesForm(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    pitch = TextAreaField('Your pitch', validators=[Required()], render_kw={'class': 'form-control', 'rows': 10})
    category_opts = RadioField('Choose category', validators=[Required()], choices=[('pickup','Pickup pitch'),('interview','Interview pitch'),('product','Product pitch'),('promotion','Promotion pitch'),('idea','Idea pitch')])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Write comment.',validators = [Required()])
    submit = SubmitField('Post')

class UpvoteForm(FlaskForm):
    upvote=SubmitField('Upvote')

class DownvoteForm(FlaskForm):
    downvote=SubmitField('Downvote')