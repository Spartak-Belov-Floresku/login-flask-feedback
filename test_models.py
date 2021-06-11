from unittest import TestCase

from app import app
from models import db, User, Feedback

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_flask:password@localhost/test_flask_db'
app.config['SQLALCHEMY_ECHO'] = False


db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """test for user model"""

    def setUp(self):
        """clean up any existing users and feedback"""

        Feedback.query.delete()
        User.query.delete()


    def tearDown(self):
        """clean up any fould transaction"""

        db.session.rollback()


    def test_create_user_obj(self):
        """test to create user obj"""

        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')

        self.assertEqual(user.first_name, 'Goofy')


    def test_insert_user_into_db(self):
        """test to insert user into the db"""

        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.email, 'goofy@mail.com')

        """check if password string does not match with password from db"""
        self.assertNotEqual(user.password,'goofy_password')

class FeedbackTestCase(TestCase):
    """test for feedback model"""

    def setUp(self):
        """clean up any existing user and feedback"""

        User.query.delete()
        Feedback.query.delete()

    def tearDown(self):
        """clean up nay fould transaction"""

        db.session.rollback()

    def test_create_feedback_obj(self):
        """test to create feedback obj"""

        feedback = Feedback(title='New feedback', content='Content new feedback', username='goofy')

        self.assertEqual(feedback.title, 'New feedback')


    def test_insert_feedback_into_db(self):
        """test to insert feedback into the db"""

        """need to creat user befor to aplly username to a feedback"""
        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        feedback = Feedback(title='New feedback', content='Content new feedback', username='goofy')
        db.session.add(feedback)
        db.session.commit()

        self.assertEqual(feedback.username,'goofy')