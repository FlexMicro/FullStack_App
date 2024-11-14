from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def init_database():
    try:
        # First connect without specifying a database
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        cursor = connection.cursor(dictionary=True)
        
        # Create the database if it doesn't exist
        db_name = os.environ.get('DB_NAME')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create the todos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.commit()
        
        return connection, cursor
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e

# Initialize database connection and cursor globally
try:
    db, cursor = init_database()
except Exception as e:
    print(f"Failed to initialize database: {e}")
    raise e

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        cursor.execute('SELECT * FROM todos')
        todos = cursor.fetchall()
        return jsonify(todos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        task = request.json['task']
        cursor.execute('INSERT INTO todos (task) VALUES (%s)', (task,))
        db.commit()
        return jsonify({'id': cursor.lastrowid, 'task': task})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        db.commit()
        return jsonify({'message': 'Todo deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))