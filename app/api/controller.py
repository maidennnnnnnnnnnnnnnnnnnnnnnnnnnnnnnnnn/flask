from datetime import datetime, timedelta

import jwt
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash

from app import db, basic_auth
from app.api import api_bp

from flask import current_app as app

from app.todo.entities import Todo
from app.user.entities import User


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

@api_bp.route('/login')
def login():
    auth = request.authorization

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('No such user in database', 401,
                             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})

    if check_password_hash(user.password, auth.password):
        expiry = datetime.utcnow() + timedelta(minutes=30)
        subject = "access"
        secret_key = app.config.get("SECRET_KEY")

        token = jwt.encode(
            {"sub": subject, "username": user.username, "exp": expiry},
            secret_key,
            algorithm="HS256"
        )

        return jsonify({"token": token})

    return make_response('Invalid username or password', 401,
                         {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})


@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todo_list = []
    for todo in todos:
        todo_list.append({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description
        })
    return jsonify({'todos': todo_list})


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    new_todo = Todo(title=data['title'], description=data.get('description', ''))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201


@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description
    })


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data['title']
    todo.description = data.get('description', '')
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})


@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

