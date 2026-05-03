from flask import request, jsonify, send_file
import os
import io
import pickle

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 🔐 Permisos
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# 🔌 Conexión con Google Drive
def get_drive_service():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


# 📤 SUBIR ARCHIVO
def upload_file():
    try:
        file = request.files['file']
        file.save(file.filename)

        service = get_drive_service()

        file_metadata = {'name': file.filename}
        media = MediaFileUpload(file.filename, resumable=True)

        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        os.remove(file.filename)

        return jsonify({"id": uploaded.get('id')})

    except Exception as e:
        print("ERROR UPLOAD:", e)
        return jsonify({"error": str(e)}), 500


# 📋 LISTAR ARCHIVOS
def list_files():
    service = get_drive_service()

    results = service.files().list(
        pageSize=10,
        fields="files(id, name)"
    ).execute()

    return jsonify(results.get('files', []))


# 📥 DESCARGAR ARCHIVO
def download_file(file_id):
    service = get_drive_service()

    # 🔹 Obtener metadata (nombre original)
    file = service.files().get(fileId=file_id, fields="name").execute()
    file_name = file.get("name")

    # 🔹 Descargar contenido
    request_drive = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    downloader = MediaIoBaseDownload(fh, request_drive)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)

    # 🔹 Usar nombre real (con extensión)
    return send_file(fh, download_name=file_name, as_attachment=True)

# 🔹 Eliminar archivo
def delete_file(file_id):
    try:
        service = get_drive_service()

        service.files().delete(fileId=file_id).execute()

        return jsonify({"message": "Archivo eliminado"})

    except Exception as e:
        print("ERROR DELETE:", e)
        return jsonify({"error": str(e)}), 500