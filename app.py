from flask import Flask, request, jsonify, send_from_directory
import os
from main import process_image_and_generate_response

app = Flask(__name__, static_folder='frontend/static', static_url_path='/static')

UPLOAD_FOLDER = os.path.join('frontend', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

response_data = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    global response_data
    response_data = {}  # Reset the response data for new uploads

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        img_text, simplified_text = process_image_and_generate_response(filepath)
        response_data['img_text'] = img_text
        response_data['simplified_text'] = simplified_text
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_response')
def get_response():
    if 'simplified_text' in response_data:
        return jsonify({'simplified_text': response_data['simplified_text']})
    else:
        return jsonify({'simplified_text': 'Nenhuma resposta disponível'})

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'start.html')

@app.route('/index.html')
def serve_start():
    return send_from_directory('frontend', 'index.html')

@app.route('/response.html')
def serve_response():
    return send_from_directory('frontend', 'response.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('frontend/static', path)

if __name__ == '__main__':
    app.run(debug=True)
