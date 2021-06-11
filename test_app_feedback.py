from unittest import TestCase

from app import app
from models import db, User, Feedback


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_flask:password@localhost/test_flask_db'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()


class FeedbackViewTestCase(TestCase):
    """test for view feedback"""

    def setUp(self):
        """add sample user"""

        Feedback.query.delete()
        User.query.delete()

        """create user dic_obj to use tests"""
        self.feedback = {'title':'New test title', 'content':'New test content', 'username':'goofy'}

        self.title = self.feedback['title']
        self.content = self.feedback['content']
        self.username = self.feedback['username']

    
    def tearDown(self):
        """clean up any fouled transaction."""

        db.session.rollback()


    def test_add_feedback(self):
        """add feedback into db"""

        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:

            with client.session_transaction() as session:
                session['username'] = self.username

            responce = client.post(f'/users/{self.username}/feedback/add', data=self.feedback, follow_redirects=True)

            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Feedback Page:', html)
            self.assertIn(self.feedback['title'], html)


    def test_update_feedback(self):
        """update feedback into db"""

        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        feedback = Feedback(title=self.title, content=self.content, username=self.username)
        db.session.add(feedback)
        db.session.commit()

        self.feedback['title'] = "Updated title"
        
        with app.test_client() as client:

            with client.session_transaction() as session:
                session['username'] = feedback.username

            responce = client.post(f'/feedback/{feedback.id}/update', data=self.feedback, follow_redirects=True)

            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Feedback Page:', html)
            self.assertIn(self.feedback['title'], html)


    def test_delete_feedback(self):
        """delete feedback into db"""

        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        feedback = Feedback(title=self.title, content=self.content, username=self.username)
        db.session.add(feedback)
        db.session.commit()
        
        with app.test_client() as client:

            with client.session_transaction() as session:
                session['username'] = feedback.username

            responce = client.post(f'/feedback/{feedback.id}/delete', follow_redirects=True)

            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Feedback Page:', html)
