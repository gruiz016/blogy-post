from unittest import TestCase
from app import app, validate_and_try_user
from flask import request
from models.user import db

class BlogyTest(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
        
    def tearDown(self):
        db.session.rollback()
        
    def test_index_get(self):
        '''Test home page'''
        with app.test_client() as client:
            res = client.get('/', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<label for="username">Username:</label>', html)
            
    def test_index_post(self):
        '''Test login auth'''
        with app.test_client() as client:
            data = {'username': 'rm544bs', 'password': '12345!'}
            res = client.post('/', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('User Name/Password was incorrect, please try again', html)
             
    def test_sign_up_post(self):
        '''Test if database creates a new user.'''
        with app.test_client() as client:
            data = {
                'firstname': 'Giovanni',
                'lastname': 'Ruiz',
                'profile-pic': '',
                'username': 'gruiz016',
                'password': 'pass12345'
            }
            res = client.post('/sign-up', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Username: gruiz016</h1>', html)
            
    def test_create_post(self):
        '''Test if database creates a new post.'''
        with app.test_client() as client:
            validate_and_try_user('Giovanni', 'Ruiz', '', 'gruiz016', 'pass12345')
            data = {
                'title': 'Testing123',
                'content': 'This is a test post!',
            }
            res = client.post('/create-post', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Testing123', html)