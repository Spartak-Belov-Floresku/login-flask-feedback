from flask import Flask, request, redirect, render_template, flash,  session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://admin_flask:password@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'helloworld'
app.debug = True
DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/register')


"""show register form page"""
@app.route('/register', methods=['GET', 'POST'])
def register_form():

    """checking if username exists in session"""
    username = session.get('username')
    if username:
        """checking if user exists in db"""
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(f'/users/{user.username}')


    form = RegisterForm()

    if form.validate_on_submit():
        """get data from form fields"""

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        try:
            user = User.register(username, password, email, first_name, last_name)
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            flash(f'Error: {err}', 'alert alert-danger font-weight-bold')
            return render_template('register.html', form=form)

        session['username'] = user.username
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)



"""show login form page"""
@app.route('/login', methods=['GET', 'POST'])
def login_form():

    """checking if username exists in session"""
    username = session.get('username')
    if username:
        """checking if user exists in db"""
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(f'/users/{user.username}')

    form = LoginForm()

    if form.validate_on_submit():
        """get data from form fields"""

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash(f'Error: username/password is not correct', 'alert alert-danger font-weight-bold')
    

    return render_template('login.html', form=form)


"""logout user"""
@app.route('/logout')
def logout_page():

    """force to remove session"""
    session.pop('username')
    return redirect('/')



"""delete user account and all user's feedback"""
@app.route('/users/<username>/delete')
def delete_user(username):

    """checking if username exists in session"""
    user_name = session.get('username')

    if user_name:

        """delete all user's feedback from db"""
        Feedback.query.filter_by(username=user_name).delete()
        db.session.commit()

        """delete all user from db"""
        User.query.filter_by(username=user_name).delete()
        db.session.commit()

        """delete session"""
        session.pop('username')

        return redirect('/register')
    
    flash(f'Error: You must be logged in to view!', 'alert alert-danger font-weight-bold')
    return redirect('/login')



"""show all feedback page"""
@app.route('/users/<username>')
def secret_page(username):

    """checking if username exists in session"""
    user_name = session.get('username')
    """checking if username exists in db"""
    user = User.query.filter_by(username=user_name).first()
    if user:
        """retrieving user's feedback from db"""
        user_feed_back = Feedback.query.filter_by(username=user.username).all()
        return render_template('user_feedback.html', user=user, feeds_back=user_feed_back)
    
    flash(f'Error: You must be logged in to view!', 'alert alert-danger font-weight-bold')
    return redirect('/login')


"""show add feedback form page"""
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback_form(username):

    """checking if username exists in session"""
    user_name = session.get('username')

    """checking if username exists in db"""
    user = User.query.filter_by(username=user_name).first()

    if not user:
        flash(f'Error: You must be logged in to view!', 'alert alert-danger font-weight-bold')
        return redirect('/login')


    form = FeedbackForm()

    if form.validate_on_submit():
        """get data from form fields"""

        title = form.title.data
        content = form.content.data
        
        """create a new feedback"""
        feed_back = Feedback(title=title, content=content, username=user.username)

        db.session.add(feed_back)
        db.session.commit()

        return redirect(f'/users/{user.username}')

    name_form = 'Add feedback:'
    action = f'/users/{user_name}/feedback/add'

    return render_template('feedback.html', form=form, name_form=name_form, action=action)


"""show update feedback page"""
@app.route('/feedback/<int:feed_id>/update', methods=['GET', 'POST'])
def update_feedback_page(feed_id):
    """checking if username exists in session"""
    user_name = session.get('username')
    """checking if username exists in db"""
    user = User.query.filter_by(username=user_name).first()
    if not user:
        flash(f'Error: You must be logged in to view!', 'alert alert-danger font-weight-bold')
        return redirect('/login')

    """check if the feedback is belong to the user"""
    feedback = Feedback.query.filter_by(id=feed_id).first()
    if not feedback.username == user_name:
        """redirect to the page feedback"""
        return redirect(f'/users/{user_name}')

    """pass data inside form object"""
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        """update data of the feedback"""

        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{user.username}')


    name_form = 'Update feedback:'
    action = f'/feedback/{feed_id}/update'

    return render_template('feedback.html', form=form, name_form=name_form, action=action)
    

"""delete feedback from db"""
@app.route('/feedback/<int:feed_id>/delete', methods=['POST'])
def delete_feedback(feed_id):

    """checking if username exists in session"""
    user_name = session.get('username')
    """checking if username exists in db"""
    user = User.query.filter_by(username=user_name).first()
    if not user:
        flash(f'Error: You must be logged in to view!', 'alert alert-danger font-weight-bold')
        return redirect('/login')

    Feedback.query.filter_by(id=feed_id).delete()
    db.session.commit()

    return redirect(f'/users/{user.username}')














if __name__ == "__main__":
    app.run(debug=True)