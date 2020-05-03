from flask import session, flash, redirect, render_template
from models.user import User, db
from random import randint

def login_user(user):
    if user:
        token = randint(1,300000)
        session['username'] = user.username
        session['token'] = token
        session['user_id'] = user.id
        return redirect('/users')
    else:
        flash('User Name/Password was incorrect, please try again', 'alert-danger')
        return redirect('/') 
    
def check_if_logged_in(username, token, user_id):
    if username != None or token != None or user_id != None:
        return redirect('/users')
    return render_template('index.html')
    

