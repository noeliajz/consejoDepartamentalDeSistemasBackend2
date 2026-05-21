from flask import Flask
from flask_cors import CORS
from drive import upload_file, list_files, download_file
from drive import delete_file

app = Flask(__name__)
CORS(app)

# Rutas
app.add_url_rule('/api/upload', 'upload', upload_file, methods=['POST'])
app.add_url_rule('/api/files', 'files', list_files, methods=['GET'])
app.add_url_rule('/api/download/<file_id>', 'download', download_file, methods=['GET'])
app.add_url_rule('/api/delete/<file_id>', 'delete', delete_file, methods=['DELETE'])


if __name__ == '__main__':
    app.run(port=5000, debug=True)