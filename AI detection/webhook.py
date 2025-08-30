import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store image metadata
images = []

@app.route('/webhook', methods=['POST', 'OPTIONS'])
def webhook():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Secure the filename and append a UUID to ensure uniqueness
    original_filename = secure_filename(file.filenamea)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    image_url = f'http://{request.host}/uploads/{unique_filename}'
    images.append({'name': unique_filename, 'url': image_url})
    return jsonify({'message': 'Image received', 'url': image_url}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images', methods=['GET'])
def get_images():
    return jsonify({'images': images})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
