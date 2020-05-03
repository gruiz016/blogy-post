from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Creates a user model'''

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f'<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, username={u.username}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String, default='https://storage.needpix.com/rsynced_images/blank-profile-picture-973461_1280.png')
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).one()

    @classmethod
    def get_user_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def login(cls, username, password):
        return cls.query.filter_by(username=username, password=password).first()
