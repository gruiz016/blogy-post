'''Functions to edit user profiles'''

from flask import redirect, flash, session, render_template, session
from models.user import db, User
from models.post import Post

def edit_user_info(user, f_name, l_name, url, username, password):
    '''Checks against current vaules to see if anything has changed in the user form.'''
    if len(f_name) == 0 or len(l_name) ==0 or len(username) == 0 or len(password) == 0:
        flash('All fields but URL are required.', 'alert-danger')
        return redirect(f'/user/{user.id}/edit')
    
    if f_name != user.first_name:
        user.first_name = f_name
        
    if l_name != user.last_name:
        user.last_name = l_name
        
    if url != user.url:
        user.url = url
        
    if username != user.username:
        user.username = username
        
    if password != user.password:
        user.password = password
        
    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/user/{user.id}')

def delete_user(user_id):
    '''Deletes users from the database and clears session data.'''
    try:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        session.clear()
        return redirect('/')
    except Exception as ex:
        string = str(ex)
        print(ex)
        if 'update or delete on table' in string:
            flash('Delete posts first before, deleting profile.', 'alert-danger')
        return redirect(f'/user/{user_id}')
        

def auth_user_edit(user, user_id, check_id):
    '''Checks if user has permissions to edit profile. Also prevents users from editing others profiles.'''
    if check_id == user_id:
        return render_template('edit.html', user=user)
    else:
        return redirect(f'/user/{check_id}')

def validate_user_profile(user_id):
    '''Prevents user from accessing users profiles that is not theres.'''
    user_token = session.get('user_id')
    if user_id == user_token:
        user = User.get_user_by_id(user_id)
        user_posts = Post.get_post_by_user(user_id)
        return render_template('user.html', user=user, posts=user_posts)
    else:
        return redirect(f'/user/{user_token}')
    