from flask import Flask, request, jsonify, send_from_directory, session
import pymysql  
import os
import uuid
from main import process_image_and_generate_response, process_pdf_and_generate_response

app = Flask(__name__, static_folder='frontend/static', static_url_path='/static')
app.secret_key = 'fgJIMmgkrti5KKLOG@35451sfmkoit455#5'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db_tlinth'



# Conexão com o banco de dados
conn = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Gerar user_id único para cada nova sessão
@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())


def storeRes(modes, response):
    with conn.cursor() as cursor:
        user_id = session.get('user_id')
        sql = "INSERT INTO res_user (modes, response, user_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (modes, response, user_id)) 
        print(user_id)
    conn.commit()


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
        print(file.name)


        if '.png' in file.filename or '.jpg' in file.filename:

            img_text, simplified_text = process_image_and_generate_response(filepath)
            response_data['img_text'] = img_text
            response_data['simplified_text'] = simplified_text

            storeRes('ARQUIVO', simplified_text)
            return jsonify({'success': True}), 200
        

        elif '.pdf' in file.filename:
        
            pdf_text, simplified_text = process_pdf_and_generate_response(filepath)
            response_data['pdf_text'] = pdf_text
            response_data['simplified_text'] = simplified_text

            storeRes('ARQUIVO', simplified_text)
            return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({'error': str(e)}), 500

# @app.route('/retrieve', methods=['GET'])
# def retrieve():
#     user_id = session.get('user_id')
#     response = {'success': False, 'data': []}
#     try:
#         with conn.cursor() as cursor:
#             sql = "SELECT conteudo FROM registros WHERE user_id = %s"
#             cursor.execute(sql, (user_id,))
#             registros = cursor.fetchall()
#             response['data'] = registros
#             response['success'] = True
#     except Exception as e:
#         print(e)
#     return jsonify(response)   


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
