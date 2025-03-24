import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import pyttsx3
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

def get_available_voices():
    voices = engine.getProperty('voices')
    return [{'id': idx, 'name': voice.name} for idx, voice in enumerate(voices)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def create_audio(text, output_path, voice_settings):
    # Apply voice settings
    if 'voice_id' in voice_settings:
        voices = engine.getProperty('voices')
        if 0 <= voice_settings['voice_id'] < len(voices):
            engine.setProperty('voice', voices[voice_settings['voice_id']].id)
    
    if 'rate' in voice_settings:
        engine.setProperty('rate', voice_settings['rate'])
    if 'volume' in voice_settings:
        engine.setProperty('volume', voice_settings['volume'])
    if 'pitch' in voice_settings:
        engine.setProperty('pitch', voice_settings['pitch'])
    
    # Save the audio file
    engine.save_to_file(text, output_path)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/voices')
def get_voices():
    return jsonify(get_available_voices())

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get voice settings from request
        voice_settings = request.form.get('voice_settings', {})
        if isinstance(voice_settings, str):
            import json
            voice_settings = json.loads(voice_settings)
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_image(file_path)
        
        # Create audio file
        audio_filename = f"{os.path.splitext(filename)[0]}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        create_audio(text, audio_path, voice_settings)
        
        return jsonify({
            'success': True,
            'text': text,
            'audio_url': f'/audio/{audio_filename}'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        mimetype='audio/mpeg'
    )

if __name__ == '__main__':
    app.run(debug=True) 