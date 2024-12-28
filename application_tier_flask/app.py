from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import boto3
from uuid import uuid4
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)
# Create a file handler
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
# Set the logging level for the file handler
file_handler.setLevel(logging.DEBUG)
# Add the handler to the Flask app logger
app.logger.addHandler(file_handler)
# Also log to stdout
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)

app.logger.info('Flask app startup')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = os.environ.get('DYNAMODB_TABLE')
app.logger.info(f'DynamoDB table: {table}')

# Initialize S3 client
s3 = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET')
app.logger.info(f'S3 bucket: {S3_BUCKET}')

def init_database():
    try:
        app.logger.info('Initializing database connection')
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        cursor = connection.cursor(dictionary=True)
        
        db_name = os.environ.get('DB_NAME')
        app.logger.info(f'Creating/using database: {db_name}')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        app.logger.info('Creating todos table if not exists')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                task VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.commit()
        app.logger.info('Database initialization successful')
        return connection, cursor
    
    except Exception as e:
        app.logger.error(f'Database initialization failed: {str(e)}', exc_info=True)
        raise e

try:
    db, cursor = init_database()
except Exception as e:
    app.logger.error(f'Failed to initialize database: {str(e)}', exc_info=True)
    raise e

@app.route('/api/upload', methods=['POST'])
def upload_file():
    app.logger.info('Starting file upload process')
    
    # Log request details
    app.logger.debug(f'Request files: {request.files}')
    app.logger.debug(f'Request form: {request.form}')
    
    if 'file' not in request.files:
        app.logger.error('No file part in request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    app.logger.info(f'Received file: {file.filename}')

    if file.filename == '':
        app.logger.error('Empty filename received')
        return jsonify({'error': 'No selected file'}), 400

    # Generate a unique filename
    filename = str(uuid4()) + os.path.splitext(file.filename)[1]
    app.logger.info(f'Generated unique filename: {filename}')

    try:
        app.logger.info(f'Attempting to upload file to S3 bucket: {S3_BUCKET}')
        # Log S3 client configuration
        app.logger.debug(f'S3 client config: region={s3.meta.region_name}')
        
        # Upload file to S3
        s3.upload_fileobj(file, S3_BUCKET, filename)
        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
        app.logger.info(f'File successfully uploaded. URL: {file_url}')
        return jsonify({'file_url': file_url}), 201
    
    except Exception as e:
        app.logger.error(f'Error uploading file to S3: {str(e)}', exc_info=True)
        # Log additional S3 details that might help debugging
        app.logger.error(f'S3 bucket: {S3_BUCKET}')
        app.logger.error(f'File details - name: {file.filename}, size: {file.content_length if hasattr(file, "content_length") else "unknown"}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    app.logger.debug('Health check endpoint called')
    return "Healthy!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.logger.info(f'Starting Flask app on port {port}')
    app.run(host='0.0.0.0', port=port)