from flask import Flask, request, render_template, jsonify
import os
from datetime import datetime
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_unique_filename():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4()).split('-')[0]
    return f"{timestamp}_{unique_id}"

def save_text(date, text):
    date_folder = os.path.join(app.config['UPLOAD_FOLDER'], date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)

    # 生成唯一的文本文件名
    unique_filename = get_unique_filename()
    text_filename = os.path.join(date_folder, f"{unique_filename}.txt")

    with open(text_filename, 'w') as f:
        f.write(text)

def save_image(date, image):
    date_folder = os.path.join(app.config['UPLOAD_FOLDER'], date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)

    # 生成唯一的图片文件名
    unique_filename = get_unique_filename()
    image_filename = os.path.join(date_folder, f"{unique_filename}.jpg")
    
    image.save(image_filename)

def get_uploaded_data(date):
    date_folder = os.path.join(app.config['UPLOAD_FOLDER'], date)
    
    if not os.path.exists(date_folder):
        return []

    uploaded_data = []
    for filename in os.listdir(date_folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # 处理图片文件
            image_path = os.path.join(date_folder, filename)
            uploaded_data.append({
                'type': 'image',
                'filename': filename,
                'path': image_path,
            })
        elif filename.endswith('.txt'):
            # 处理文本文件
            text_path = os.path.join(date_folder, filename)
            with open(text_path, 'r') as text_file:
                text = text_file.read()
                uploaded_data.append({
                    'type': 'text',
                    'filename': filename,
                    'text': text,
                })

    return uploaded_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_uploaded_data')
def get_data():
    date = request.args.get('date')
    uploaded_data = get_uploaded_data(date)
    return jsonify(uploaded_data)

@app.route('/upload', methods=['POST'])
def upload():
    date = request.form['date']
    text = request.form['text']
    image = request.files['image']
    
    if image and image.filename:
        save_image(date, image)

    if text:
        save_text(date, text)

    return '上传成功！'

if __name__ == '__main__':
    app.run(debug=True)
