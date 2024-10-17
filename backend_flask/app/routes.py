from flask import Blueprint, jsonify, request, g
from .database import get_db

bp = Blueprint('main', __name__)

@bp.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        _, cursor = get_db()
        cursor.execute('SELECT * FROM todos')
        todos = cursor.fetchall()
        return jsonify(todos)
    except Exception as e:
        return jsonify({'error': 'Error fetching todos'}), 500

@bp.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        db, cursor = get_db()
        task = request.json['task']
        cursor.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'task': task})
    except Exception as e:
        return jsonify({'error': 'Error adding todo'}), 500

@bp.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        db, cursor = get_db()
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        db.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        return jsonify({'error': 'Error deleting todo'}), 500