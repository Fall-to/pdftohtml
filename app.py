import os
import subprocess
from flask import Flask, request, send_file, render_template, redirect, url_for
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and file.filename.endswith('.pdf'):
            return convert_pdf(file)
        return 'Invalid file type', 400
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf(file=None):
    if file is None:
        file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, file.filename)
            file.save(pdf_path)
            html_filename = os.path.splitext(file.filename)[0] + '.html'
            html_path = os.path.join(tmpdir, html_filename)
            
            cmd = f"pdf2htmlEX --zoom 1.3 --dest-dir {tmpdir} {pdf_path}"
            subprocess.run(cmd, shell=True, check=True)
            
            if os.path.exists(html_path):
                return send_file(html_path, as_attachment=True, download_name=html_filename)
            else:
                return 'Error: HTML file not created', 500
    return 'Invalid file type', 400


@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
