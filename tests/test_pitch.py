import unittest
from app.models import Pitch,User
from app import db

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Ryan = User(username = 'Ryan',email = 'ryan@ms.com',bio='jkjkjk',password = 'crucible')
        self.new_pitch = Pitch(pitch_title='Title for this pitch',category="promotion",upvotes=0, downvotes=0,pitch_text='This is the best thing since sliced bread',user = self.user_Ryan )

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.pitch_title,'Title for this pitch')
        self.assertEquals(self.new_pitch.category,"promotion")
        self.assertEquals(self.new_pitch.pitch_text,'This is the best thing since sliced bread')
        self.assertEquals(self.new_pitch.upvotes,0)
        self.assertEquals(self.new_pitch.downvotes,0)
        self.assertEquals(self.new_pitch.user,self.user_Ryan)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)