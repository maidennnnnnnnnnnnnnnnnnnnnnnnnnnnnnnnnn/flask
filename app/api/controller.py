from flask import jsonify, request

from app import db
from app.api import api_bp
from app.models import Todo


@api_bp.route('/todos', methods=['GET'])
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
def create_todo():
    data = request.get_json()
    new_todo = Todo(title=data['title'], description=data.get('description', ''))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created successfully'}), 201


@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description
    })


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data['title']
    todo.description = data.get('description', '')
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully'})


@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})
