from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    category = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(50), nullable=False, default='medium')

    def __init__(self, title, description, status='pending', category=None, priority='medium'):
        self.title = title
        self.description = description
        self.status = status
        self.category = category
        self.priority = priority

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Task with this title already exists.")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"An error occurred while saving the task: {str(e)}")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"An error occurred while updating the task: {str(e)}")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"An error occurred while deleting the task: {str(e)}")