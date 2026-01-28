import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from your_application import create_app, db

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        response = self.client.post('/api/register', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', json.loads(response.data))

    def test_user_login(self):
        self.client.post('/api/register', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        response = self.client.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_create_task(self):
        login_response = self.client.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']
        response = self.client.post('/api/tasks', headers={'Authorization': f'Bearer {access_token}'}, data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('task_id', json.loads(response.data))

    def test_get_tasks(self):
        login_response = self.client.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']
        self.client.post('/api/tasks', headers={'Authorization': f'Bearer {access_token}'}, data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task.'
        }), content_type='application/json')
        response = self.client.get('/api/tasks', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(json.loads(response.data)), 0)

    def test_update_task(self):
        login_response = self.client.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']
        task_response = self.client.post('/api/tasks', headers={'Authorization': f'Bearer {access_token}'}, data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task.'
        }), content_type='application/json')
        task_id = json.loads(task_response.data)['task_id']
        response = self.client.put(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {access_token}'}, data=json.dumps({
            'title': 'Updated Task',
            'description': 'This is an updated test task.'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('task_id', json.loads(response.data))

    def test_delete_task(self):
        login_response = self.client.post('/api/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        access_token = json.loads(login_response.data)['access_token']
        task_response = self.client.post('/api/tasks', headers={'Authorization': f'Bearer {access_token}'}, data=json.dumps({
            'title': 'Test Task',
            'description': 'This is a test task.'
        }), content_type='application/json')
        task_id = json.loads(task_response.data)['task_id']
        response = self.client.delete(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()