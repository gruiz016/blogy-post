from flask import redirect, request, flash
from models.post import Post, db

def save_user_post(title, content, user_id):
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')