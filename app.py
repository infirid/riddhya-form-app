from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import io
import base64

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    form_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'education': request.form['education'],
        'experience': request.form['experience'],
        'references': request.form['references'],
    }

    # Read and encode uploaded images
    photo = request.files['photo']
    aadhar = request.files['aadhar']
    pan = request.files['pan']

    form_data['photo_data'] = base64.b64encode(photo.read()).decode('utf-8')
    form_data['aadhar_data'] = base64.b64encode(aadhar.read()).decode('utf-8')
    form_data['pan_data'] = base64.b64encode(pan.read()).decode('utf-8')

    rendered = render_template('pdf_template.html', **form_data)
    pdf_file = io.BytesIO()
    HTML(string=rendered, base_url=request.base_url).write_pdf(pdf_file)
    pdf_file.seek(0)
    return send_file(pdf_file, as_attachment=True, download_name='application_form.pdf', mimetype='application/pdf')

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
