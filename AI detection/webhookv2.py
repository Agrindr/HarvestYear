import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Add CORS support

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')  # Better path handling
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store image metadata
images = []

@app.route('/webhook', methods=['POST', 'OPTIONS'])  # Add OPTIONS for CORS
def webhook():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 
        
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    image_url = f'http://{request.host}/uploads/{filename}'  # Full URL
    images.append({'name': filename, 'url': image_url})
    return jsonify({'message': 'Image received', 'url': image_url}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images', methods=['GET'])
def get_images():
    return jsonify({'images': images})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)