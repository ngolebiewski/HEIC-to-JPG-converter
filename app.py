from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from PIL import Image
import pyheif
import os

app = Flask(__name__)

# Folder to store uploaded and converted images
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        # If no file is selected
        if file.filename == '':
            return 'No selected file'
        
        # If file is valid and ends with .heic
        if file and file.filename.lower().endswith('.heic'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Convert the HEIC image to JPG
            heif_image = pyheif.read(filepath)
            image = Image.frombytes(
                heif_image.mode, 
                heif_image.size, 
                heif_image.data, 
                "raw", 
                heif_image.mode
            )
            
            # Save the image as .jpg
            jpg_filename = file.filename.rsplit('.', 1)[0] + '.jpg'
            jpg_filepath = os.path.join(app.config['UPLOAD_FOLDER'], jpg_filename)
            image.save(jpg_filepath, "JPEG")

            # Provide a link for downloading the image
            return f'''
            <!doctype html>
            <title>Image Converted</title>
            <h1>Image successfully converted!</h1>
            <a href="/download/{jpg_filename}" download>Download {jpg_filename}</a>
            '''
    
    return '''
    <!doctype html>
    <title>Upload HEIC to Convert to JPG</title>
    <h1>Upload a HEIC file to convert to JPG</h1>
    <h2>For Ryan!</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/download/<filename>')
def download_file(filename):
    # Send the file to the user's browser for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
