from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from uuid import uuid4
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('mytest')

# Initialize S3 client
s3 = boto3.client('s3')
S3_BUCKET = 'bymyckei3283'  # Replace with your S3 bucket name

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo_id = str(uuid4())
    task = data.get('task')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    # Add todo to DynamoDB
    table.put_item(
        Item={
            'id': todo_id,
            'task': task
        }
    )

    return jsonify({'id': todo_id, 'task': task}), 201

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Generate a unique filename
    filename = str(uuid4()) + os.path.splitext(file.filename)[1]

    try:
        # Upload file to S3
        s3.upload_fileobj(file, S3_BUCKET, filename)
        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
        return jsonify({'file_url': file_url}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)