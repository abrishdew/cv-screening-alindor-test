from flask import Flask, render_template, request, redirect, url_for
import openai
import os
import magic
import pdfplumber
from docx import Document
import io

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    cv = request.files['cv']
    job_description = request.files['job_description']
    score, explanation = process_files(cv, job_description)
    return render_template('result.html', score=score, explanation=explanation)

def process_files(cv, job_description):
    cv_text = extract_text(cv)
    job_description_text = extract_text(job_description)
    return analyze_with_openai(cv_text, job_description_text)

def extract_text(file):
    # Create a buffer from the file stream
    buffer = io.BytesIO(file.read())
    file_mime_type = magic.from_buffer(buffer.read(2048), mime=True)
    buffer.seek(0)

    if 'application/pdf' in file_mime_type:
        return extract_text_from_pdf(buffer)
    elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in file_mime_type:
        return extract_text_from_docx(buffer)
    elif 'text/plain' in file_mime_type:
        buffer.seek(0)
        return buffer.read().decode('utf-8')
    else:
        return "Unsupported file format"

def extract_text_from_pdf(buffer):
    text = ""
    with pdfplumber.open(buffer) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(buffer):
    doc = Document(buffer)
    return "\n".join([para.text for para in doc.paragraphs])

def analyze_with_openai(cv_text, job_description_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sophisticated AI trained to evaluate CVs."},
                {"role": "user", "content": f"Job Description: {job_description_text}"},
                {"role": "user", "content": f"CV: {cv_text}"}
            ]
        )
        explanation = response.choices[0].message['content']
        score = determine_score(explanation)
        return score, explanation
    except Exception as e:
        print(f"API call failed: {str(e)}")
        return 0, "An error occurred during processing. Please try again later."

def determine_score(text):
    if "excellent fit" in text:
        return 10
    elif "good fit" in text:
        return 8
    elif "moderate fit" in text:
        return 6
    elif "poor fit" in text:
        return 4
    return 7  # Default score if no specific keywords found

if __name__ == '__main__':
    app.run(debug=True, port=5002)
