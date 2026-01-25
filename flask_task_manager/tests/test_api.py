import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from your_application import create_app, db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.test_user = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post('/api/register', json=self.test_user)

        # Log in to get JWT token
        response = self.client.post('/api/login', json=self.test_user)
        self.token = response.json['access_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/api/register', json={
            'username': 'newuser',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.json)

    def test_login_user(self):
        response = self.client.post('/api/login', json=self.test_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_protected_route(self):
        response = self.client.get('/api/protected', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_protected_route_without_token(self):
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 401)
        self.assertIn('msg', response.json)

    def test_create_task(self):
        response = self.client.post('/api/tasks', json={
            'title': 'Test Task',
            'description': 'This is a test task.'
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('task_id', response.json)

    def test_get_tasks(self):
        response = self.client.get('/api/tasks', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_update_task(self):
        # First create a task
        create_response = self.client.post('/api/tasks', json={
            'title': 'Update Task',
            'description': 'This task will be updated.'
        }, headers={'Authorization': f'Bearer {self.token}'})
        task_id = create_response.json['task_id']

        # Now update the task
        update_response = self.client.put(f'/api/tasks/{task_id}', json={
            'title': 'Updated Task',
            'description': 'This task has been updated.'
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('message', update_response.json)

    def test_delete_task(self):
        # First create a task
        create_response = self.client.post('/api/tasks', json={
            'title': 'Delete Task',
            'description': 'This task will be deleted.'
        }, headers={'Authorization': f'Bearer {self.token}'})
        task_id = create_response.json['task_id']

        # Now delete the task
        delete_response = self.client.delete(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(delete_response.status_code, 204)

if __name__ == '__main__':
    unittest.main()