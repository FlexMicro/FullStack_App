from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(name)
CORS(app)

db = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
)

cursor = db.cursor(dictionary=True)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        cursor.execute('SELECT * FROM todos')
        todos = cursor.fetchall()
        return jsonify(todos)
    except Exception as e:
        return jsonify({'error': 'Error fetching todos'}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        task = request.json['task']
        cursor.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'task': task})
    except Exception as e:
        return jsonify({'error': 'Error adding todo'}), 500

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        db.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        return jsonify({'error': 'Error deleting todo'}), 500

if name == 'main':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))