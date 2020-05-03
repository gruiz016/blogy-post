from models.user import db, User, relationship
from datetime import datetime

class Post(db.Model):
    '''Creates a Post model'''

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f'<Post id={p.id}, title={p.title}, content={p.content}, user_id={p.user_id}, created_at={p.created_at}>'
    
    users = relationship("User")
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @classmethod
    def get_all_posts(cls):
        return cls.query.all()
    
    @classmethod
    def get_post_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_post_by_id(cls, post_id):
        return cls.query.get(post_id)
    
