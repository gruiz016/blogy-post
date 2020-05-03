from flask import Flask, render_template, redirect, request, flash, session
from models.user import db, connect_db, User
from utilities.signup import signup_user, confirm_user, validate_and_try_user
from utilities.login import login_user, check_if_logged_in
from utilities.edit_user import edit_user_info, delete_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc1122311231'

connect_db(app)


@app.route('/')
def index():
    user_id = session.get('user_id', None)
    username = session.get('username', None)
    token = session.get('token', None)
    return check_if_logged_in(username, token, user_id)


@app.route('/', methods=['POST'])
def login():
    username = request.form['username'].lower()
    password = request.form['password']
    user = User.login(username, password)
    return login_user(user)



@app.route('/sign-up')
def signup():
    return render_template('signup.html')


@app.route('/sign-up', methods=['POST'])
def show_signed_up_user_profile():

    f_name = request.form['firstname'].lower()
    l_name = request.form['lastname'].lower()
    url = request.form['profile-pic'].lower()
    username = request.form['username'].lower()
    password = request.form['password']

    return validate_and_try_user(f_name, l_name, url, username, password)


@app.route('/user/<int:user_id>')
def method_name(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('user.html', user=user)


@app.route('/users')
def show_users():
    all_users = User.get_all_users()
    return render_template('home.html', users=all_users)

@app.route('/user/<int:user_id>/edit')
def edit_user(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('edit.html', user=user)

@app.route('/user/<int:user_id>/edit', methods=['POST'])
def edit_user_confirm(user_id):
    f_name = request.form['firstname'].lower()
    l_name = request.form['lastname'].lower()
    url = request.form['profile-pic'].lower()
    username = request.form['username'].lower()
    password = request.form['password']
    user = User.get_user_by_id(user_id)
    
    return edit_user_info(user, f_name, l_name, url, username, password)

@app.route('/user/<int:user_id>/delete')
def remove_user(user_id):
    return delete_user(user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')