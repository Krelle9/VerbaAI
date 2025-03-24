# PDF & Image to Speech Converter

A web application that converts PDF documents and images to speech using OCR and text-to-speech technology.

## Features

- Upload PDF files and images (PNG, JPG, JPEG)
- Extract text from PDFs and images using OCR
- Convert extracted text to speech
- Modern, responsive web interface
- Drag and drop file upload
- Real-time processing status

## Prerequisites

- Python 3.7 or higher
- Tesseract OCR installed on your system
  - For macOS: `brew install tesseract`
  - For Ubuntu: `sudo apt-get install tesseract-ocr`
  - For Windows: Download and install from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload a PDF or image file by dragging and dropping it into the upload zone or clicking the "Choose File" button.

4. Wait for the processing to complete. The extracted text will be displayed, and you can play the generated audio using the audio player.

## File Size Limits

- Maximum file size: 16MB
- Supported file types: PDF, PNG, JPG, JPEG

## Notes

- The application uses Google Text-to-Speech (gTTS) for text-to-speech conversion
- OCR quality depends on the image quality and text clarity
- Processing time may vary depending on file size and content 