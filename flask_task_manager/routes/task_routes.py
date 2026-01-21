from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from ..models import db, Task

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({"msg": "Title is required"}), 400

    new_task = Task(title=title, description=description, user_id=current_user)
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_routes.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user).first()
    
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    
    return jsonify(task.to_dict()), 200

@task_routes.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user).first()
    
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if title:
        task.title = title
    if description:
        task.description = description

    try:
        db.session.commit()
        return jsonify(task.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_routes.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user).first()
    
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Task deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500