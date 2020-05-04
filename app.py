# Dependencies and models
from flask import Flask, render_template, redirect, request, flash, session
from models.user import db, connect_db, User
from models.post import Post
import os
# Helper functions
from utilities.signup import signup_user, confirm_user, validate_and_try_user
from utilities.login import login_user, check_if_logged_in
from utilities.edit_user import edit_user_info, delete_user, auth_user_edit, validate_user_profile
from utilities.post_edit import save_user_post, can_user_edit_post, append_edit_posts, validate_post, delete_user_post, search_database_posts

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///blogy_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SERCRET_KEY', '12345')
connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
    '''Custom 404 page'''
    return render_template('404.html'), 404

@app.route('/')
def index():
    '''Renders either the login/signup screen or the home screen depending if the user is logged in or not.'''
    user_id = session.get('user_id', None)
    username = session.get('username', None)
    token = session.get('token', None)
    return check_if_logged_in(username, token, user_id)

@app.route('/', methods=['POST'])
def login():
    '''Handles the login'''
    username = request.form['username'].lower()
    password = request.form['password']
    user = User.login(username, password)
    return login_user(user)

@app.route('/sign-up')
def signup():
    '''Signup form.'''
    return render_template('signup.html')

@app.route('/sign-up', methods=['POST'])
def show_signed_up_user_profile():
    '''Handles the signup process.'''
    f_name = request.form['firstname'].lower()
    l_name = request.form['lastname'].lower()
    url = request.form['profile-pic'].lower()
    username = request.form['username'].lower()
    password = request.form['password']
    return validate_and_try_user(f_name, l_name, url, username, password)

@app.route('/user/<int:user_id>')
def method_name(user_id):
    '''Displays the correct profile for the authorized user.'''
    return validate_user_profile(user_id)

@app.route('/search-posts')
def show_users():
    '''Handles ther search term in the navigation, and disables it if user is not logged in.'''
    if session.get('token') == None:
        return redirect('/')
    title = request.args['search']
    return search_database_posts(title)

@app.route('/user/<int:user_id>/edit')
def edit_user(user_id):
    '''Allows only the authorized user to edit thier profile.'''
    user = User.get_user_by_id(user_id)
    check_id = session.get('user_id')
    return auth_user_edit(user, user_id, check_id)

@app.route('/user/<int:user_id>/edit', methods=['POST'])
def edit_user_confirm(user_id):
    '''Handles the profile edit.'''
    f_name = request.form['firstname'].lower()
    l_name = request.form['lastname'].lower()
    url = request.form['profile-pic'].lower()
    username = request.form['username'].lower()
    password = request.form['password']
    user = User.get_user_by_id(user_id)
    return edit_user_info(user, f_name, l_name, url, username, password)

@app.route('/user/<int:user_id>/delete')
def remove_user(user_id):
    '''Deletes a user from the database.'''
    return delete_user(user_id)

@app.route('/logout')
def logout():
    '''Logs user out and clears the session.'''
    session.clear()
    return redirect('/')

@app.route('/create-post')
def create_post():
    '''Displays the create post form.'''
    if session.get('token') == None:
        return redirect('/')
    return render_template('create.html')

@app.route('/create-post', methods=['POST'])
def save_post():
    '''Handles the create form request.'''
    title = request.form['title']
    content = request.form['content']
    user_id = session.get('user_id')
    return save_user_post(title=title, content=content, user_id=user_id)

@app.route('/posts')
def posts():
    '''This is the home page, once logged in users will always be redirected to the posts page.'''
    all_post = Post.get_all_posts()
    return render_template('posts.html', posts=all_post)

@app.route('/post/details/<int:post_id>')
def post_details(post_id):
    '''Shows the post in a full page.'''
    return validate_post(post_id)

@app.route('/post/edit/<int:post_id>')
def edit_post(post_id):
    '''Displays the post edit.'''
    return can_user_edit_post(post_id)

@app.route('/post/edit/<int:post_id>', methods=['POST'])
def append_post(post_id):
    '''Handles the post edit request.'''
    title = request.form['title']
    content = request.form['content']
    return append_edit_posts(post_id, title, content)

@app.route('/post/delete/<int:post_id>')
def delete_post(post_id):
    '''Deletes a users post.'''
    return delete_user_post(post_id)