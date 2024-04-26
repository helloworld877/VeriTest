import os
import shutil
from flask import Flask, request, jsonify, send_file
import tempfile
import zipfile
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)


@app.route('/upload_files', methods=['POST'])
def upload_files():
    # Get Mode_Number field from form data
    mode_number = request.form.get('Mode_Number')
    if mode_number == '1':
        try:
            v_file = request.files['vFile']
            py_file = request.files['pyFile']
            # Save or process the uploaded files here
            v_file.save('uploaded_files/' + v_file.filename)
            py_file.save('uploaded_files/' + py_file.filename)

            arguments = []
            arguments.append(os.path.abspath(
                f"uploaded_files/{v_file.filename}"))
            arguments.append(os.path.abspath(
                f"uploaded_files/{py_file.filename}"))

            # Run the Bash script with command-line arguments
            HOME = os.environ.get('VERITEST_HOME')
            subprocess.run(
                ['bash', f"{HOME}/mode_selection.bash"] + arguments, check=True)

            ################################

            directory_to_zip = 'uploaded_files/results'

            # Create a temporary file to store the ZIP archive
            zip_fd, zip_path = tempfile.mkstemp()
            os.close(zip_fd)

            # Create a ZIP archive of the directory
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(directory_to_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(
                            file_path, directory_to_zip))
            #########################
            # Delete the individual uploaded files
            os.remove('uploaded_files/' + v_file.filename)
            os.remove('uploaded_files/' + py_file.filename)

            # Return the zip file for download

            return send_file(zip_path, as_attachment=True)
        except Exception as e:
            print("EXCEPTION")
            print(e)
            return jsonify(success=False, error=str(e)), 400
    else:
        return jsonify(success=False, error="Invalid Mode_Number"), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
