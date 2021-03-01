import unittest
from app.models import Pitch,User,Comment
from app import db

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Ryan = User(username = 'Ryan',password = 'crucible', email = 'ryan@ms.com', bio='jkjkjk')
        self.new_pitch = Pitch(pitch_title='Title for this pitch',category="promotion",upvotes=0, downvotes=0,pitch_text='This is the best thing since sliced bread',user = self.user_Ryan )
        self.new_comment= Comment(comment_text='Is a good one', user=self.user_Ryan, pitch=self.new_pitch)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment_text,'Is a good one')        
        self.assertEquals(self.new_comment.user,self.user_Ryan)
        self.assertEquals(self.new_comment.pitch,self.new_pitch)

    def test_save_pitch(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)