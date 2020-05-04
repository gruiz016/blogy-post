'''Login functions.'''

from flask import session, flash, redirect, render_template
from models.user import User, db
from random import randint

def login_user(user):
    '''If there is a user object, we set session data and redirect to the main page.'''
    if user:
        token = randint(1,300000)
        session['username'] = user.username
        session['token'] = token
        session['user_id'] = user.id
        return redirect('/posts')
    else:
        flash('User Name/Password was incorrect, please try again', 'alert-danger')
        return redirect('/') 
    
def check_if_logged_in(username, token, user_id):
    '''Checks if there is session data (if user logged in) and redirects accordingly.'''
    if username != None and token != None and user_id != None:
        return redirect('/posts')
    return render_template('index.html')
    

