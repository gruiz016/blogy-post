from flask import redirect, flash, session
from models.user import db, User

def edit_user_info(user, f_name, l_name, url, username, password):
    
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
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    session.clear()
    return redirect('/')
    