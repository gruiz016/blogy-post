from flask import redirect, request, flash, session, render_template
from models.post import Post, db
from models.user import User

def save_user_post(title, content, user_id):
    '''Saves user's post to the database'''
    if len(title) == 0 or len(content) == 0:
        flash('Both fields are required!', 'alert-danger')
        return redirect('/create-post')
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')

def can_user_edit_post(post_id):
    '''Checks if user can edit a post. ID on post must match the id in session.'''
    try:
        post = Post.get_post_by_id(post_id)
        user_id = post.user_id
        if user_id == session.get('user_id'):
            return render_template('edit_post.html', post=post)
        else: 
            return redirect(f'/post/details/{post_id}')
    except AttributeError as ex:
        string = str(ex)
        print(string)
        if 'attribute' in string:
            flash('There is no post found, please try again!', 'alert-danger')
        return redirect('/')
    
def append_edit_posts(post_id, title, content):
    '''
    Edit Posts.
    
    Checks if anything in a post has changed and if it is, it updates the database.
    '''
    post = Post.get_post_by_id(post_id)
    
    if len(title) == 0 or len(content) == 0:
        flash('Both fields are required!', 'alert-danger')
        return redirect(f'/post/edit/{post_id}')

    if post.title != title:
        post.title = title
        
    if post.content != content:
        post.content = content
        
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/post/details/{post_id}')

def validate_post(post_id):
    '''Prevents users from accessing posts that are not in the database.'''
    try:
        post = Post.get_post_by_id(post_id)
        user = User.get_user_by_id(post.user_id)
        return render_template('post_details.html', post=post, user=user)
    except AttributeError as ex:
        string = str(ex)
        print(string)
        if 'attribute' in string:
            flash('There is no post found, please try again!', 'alert-danger')
        return redirect('/')
    
def delete_user_post(post_id):
    '''Deletes a users posts.'''
    user_id = session.get('user_id')
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('Post deleted!', 'alert-success')
    return redirect(f'/user/{user_id}')

def search_database_posts(title):
    '''Allows users to search for keywords in titles.'''
    all_posts = Post.search_post_titles(title=title)
    if len(all_posts) == 0:
        flash("Sorry, we couldn't find anything", 'alert-danger')
        return redirect('/')
    return render_template('search.html', posts=all_posts)
    
    
    
    
    