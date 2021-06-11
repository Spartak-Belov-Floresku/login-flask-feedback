from unittest import TestCase

from app import app
from models import db, User, Feedback


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_flask:password@localhost/test_lask_db'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """test for view user"""

    def setUp(self):
        """add sample user"""

        User.query.delete()

        """create user dic_obj to use tests"""
        self.user = {'username':'goofy', 'password':'goofy_password', 'email':'goofy@mail.com', 'first_name':'Goofy', 'last_name':'Goof'}

        self.username = self.user['username']
        self.password = self.user['password']
        self.count = 0

    
    def tearDown(self):
        """clean up any fouled transaction."""

        db.session.rollback()


    def test_user_register(self):
        """test to register user"""

        with app.test_client() as client:

            responce = client.post('/register', data=self.user, follow_redirects=True)

            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Feedback Page:', html)


    def test_user_login(self):
        """test tologin user"""

        """create user in db"""
        user = User.register('goofy', 'goofy_password', 'goofy@mail.com', 'Goofy', 'Goof')
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:

            user_data = {'username':self.username, 'password': self.password}
            responce = client.post('/login', data=user_data, follow_redirects=True)

            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Feedback Page:', html)


    def test_delete_user_from_db(self):
        """test to delete from db"""

        with app.test_client() as client:

            with client.session_transaction() as session:
                session['username'] = self.username
            
            responce = client.get(f'/users/{self.username}/delete', follow_redirects=True)
            
            html = responce.get_data(as_text=True)

            self.assertEqual(responce.status_code, 200)
            self.assertIn('Register Form:', html)

