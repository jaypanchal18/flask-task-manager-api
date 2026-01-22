from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from ..models import Task, db

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    priority = data.get('priority')

    if not title or not category or priority not in ['low', 'medium', 'high']:
        return jsonify({'msg': 'Invalid input'}), 400

    new_task = Task(title=title, description=description, category=category, priority=priority, user_id=current_user)

    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'msg': 'Task created', 'task_id': new_task.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'msg': 'Error creating task', 'error': str(e)}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    category = request.args.get('category')
    priority = request.args.get('priority')

    query = Task.query.filter_by(user_id=current_user)

    if category:
        query = query.filter_by(category=category)
    if priority:
        query = query.filter_by(priority=priority)

    try:
        tasks = query.all()
        return jsonify([task.to_dict() for task in tasks]), 200
    except SQLAlchemyError as e:
        return jsonify({'msg': 'Error retrieving tasks', 'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    category = data.get('category')
    priority = data.get('priority')

    task = Task.query.filter_by(id=task_id, user_id=current_user).first()
    if not task:
        return jsonify({'msg': 'Task not found'}), 404

    if title:
        task.title = title
    if description:
        task.description = description
    if category:
        task.category = category
    if priority in ['low', 'medium', 'high']:
        task.priority = priority

    try:
        db.session.commit()
        return jsonify({'msg': 'Task updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'msg': 'Error updating task', 'error': str(e)}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user).first()
    if not task:
        return jsonify({'msg': 'Task not found'}), 404

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'msg': 'Task deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'msg': 'Error deleting task', 'error': str(e)}), 500