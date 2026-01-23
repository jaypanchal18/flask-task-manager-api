from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import db, Task, User
from marshmallow import Schema, fields, ValidationError

task_routes = Blueprint('task_routes', __name__)

class TaskSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)

@task_routes.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    try:
        task_data = TaskSchema().load(data)
        if task_data['user_id'] != current_user['id']:
            return jsonify({"msg": "Unauthorized to create task for this user"}), 403
        
        new_task = Task(title=task_data['title'], description=task_data['description'], user_id=current_user['id'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"msg": "Task created", "task": new_task.to_dict()}), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

@task_routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    
    try:
        tasks = Task.query.filter_by(user_id=current_user['id']).all()
        return jsonify([task.to_dict() for task in tasks]), 200
    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error", "error": str(e)}), 500

@task_routes.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user['id']).first()
        if not task:
            return jsonify({"msg": "Task not found or unauthorized"}), 404
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        
        db.session.commit()
        return jsonify({"msg": "Task updated", "task": task.to_dict()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

@task_routes.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user['id']).first()
        if not task:
            return jsonify({"msg": "Task not found or unauthorized"}), 404
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Task deleted"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500