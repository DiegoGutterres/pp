from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='frontend/static', static_url_path='/static')

UPLOAD_FOLDER = os.path.join('frontend', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        # Process the file (e.g., read content, extract information)
        info = process_file(filepath)
        return jsonify({'success': True, 'info': info}), 200

def process_file(filepath):
    # Aqui você processa o arquivo e extrai as informações necessárias
    with open(filepath, 'r') as f:
        content = f.read()
        # Supondo que o arquivo seja um texto simples
        lines = content.splitlines()
        num_lines = len(lines)
        num_words = sum(len(line.split()) for line in lines)
        return {'num_lines': num_lines, 'num_words': num_words}

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'start.html')

@app.route('/index.html')
def serve_start():
    return send_from_directory('frontend', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('frontend/static', path)


if __name__ == '__main__':
    app.run(debug=True)
