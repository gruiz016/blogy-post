from models.user import User, db
from flask import flash, redirect, session
from random import randint

def signup_user(f_name, l_name, url, us_name, password):

    if len(f_name) == 0 or len(l_name) ==0 or len(us_name) == 0 or len(password) == 0:
        flash('All fields but URL are required.', 'alert-danger')
        return redirect('/sign-up')

    if len(url) < 2:
        new_user = User(first_name=f_name, last_name=l_name,
                        username=us_name, password=password)
    else:
        new_user = User(first_name=f_name, last_name=l_name,
                        url=url, username=us_name, password=password)
    
    db.session.add(new_user)
    db.session.commit()
    
    token = randint(1,300000)
    session['username'] = new_user.username
    session['token'] = token
    session['user_id'] = new_user.id
    
    return User.find_user_by_username(us_name)


def confirm_user(user):
    if user:
        return redirect(f'/user/{user.id}')
    flash('Something went wrong, please try again!', 'alert-danger')
    return redirect('/')


def validate_and_try_user(f_name, l_name, url, username, password):

    try:
        user = signup_user(f_name=f_name, l_name=l_name, url=url,
                           us_name=username, password=password)
        return confirm_user(user)
    except (Exception) as exc:
        string = str(exc)
        if 'duplicate key value violates unique constraint' in string:
            flash('Username taken, username must be unique.', 'alert-danger')
        return redirect('/sign-up')
