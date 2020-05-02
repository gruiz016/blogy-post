from flask import Flask, render_template, redirect, request, flash
from models.user import db, connect_db, User
from utilities.signup import signup_user, confirm_user, validate_and_try_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc1122311231'

connect_db(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.login(username, password)

    if user:
        return redirect('/users')
    else:
        flash('User Name/Password was incorrect, please try again', 'alert-danger')
        return redirect('/')


@app.route('/sign-up')
def signup():
    return render_template('signup.html')


@app.route('/sign-up', methods=['POST'])
def show_signed_up_user_profile():

    f_name = request.form['firstname']
    l_name = request.form['lastname']
    url = request.form['profile-pic']
    username = request.form['username']
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
