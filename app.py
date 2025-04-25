# from flask import Flask, render_template, request, jsonify, redirect, url_for, session
# from dotenv import load_dotenv
# from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
# import os
# import requests
# import datetime
# from functools import wraps

# # Load environment variables
# load_dotenv()

# # Configuration
# SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
# SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")
# API_KEY = os.getenv("API_KEY")
# API_VERSION = os.getenv("API_VERSION")
# AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
# CONTAINER_NAME = os.getenv("CONTAINER_NAME")
# ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")

# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = os.urandom(24)  # Required for session management

# # Hardcoded credentials
# VALID_CREDENTIALS = {
#     "admin": "admin123"
# }

# # Build Azure Search endpoint
# endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version={API_VERSION}"

# # Blob client
# blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
# container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
        
#         if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
#             session['username'] = username
#             return redirect(url_for('index'))
#         else:
#             return render_template('login.html', error='Invalid username or password')
    
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/')
# @login_required
# def index():
#     return render_template('index4.html')

# @app.route('/search', methods=['POST'])
# @login_required
# def search():
#     user_query = request.form.get('query')
    
#     if not user_query:
#         return jsonify({'error': 'No query provided'}), 400

#     headers = {
#         "Content-Type": "application/json",
#         "api-key": API_KEY
#     }

#     payload = {
#         "search": user_query,
#         "searchFields": "content,metadata_storage_name",
#         "select": "content,metadata_storage_name,metadata_storage_path",
#         "scoringProfile": "contentBoost",
#         "top": 10,
#         "queryType": "full",
#         "searchMode": "all"
#     }

#     try:
#         response = requests.post(endpoint, headers=headers, json=payload)
#         response.raise_for_status()
#         results = response.json().get("value", [])
        
#         for result in results:
#             if 'metadata_storage_path' in result:
#                 try:
#                     blob_name = result['metadata_storage_name']
#                     blob_client = container_client.get_blob_client(blob_name)
                    
#                     if not blob_client.exists():
#                         result['view_url'] = None
#                         continue
                    
#                     ext = blob_name.lower().split('.')[-1] if '.' in blob_name else ''
#                     result['file_type'] = {
#                         'pdf': 'pdf',
#                         'doc': 'word', 'docx': 'word',
#                         'xls': 'excel', 'xlsx': 'excel',
#                         'ppt': 'powerpoint', 'pptx': 'powerpoint',
#                         'txt': 'text',
#                         'json': 'text',
#                         'csv': 'text'
#                     }.get(ext, 'other')
                    
#                     sas_token = generate_blob_sas(
#                         account_name=blob_service_client.account_name,
#                         container_name=CONTAINER_NAME,
#                         blob_name=blob_name,
#                         account_key=ACCOUNT_KEY,
#                         permission=BlobSasPermissions(read=True),
#                         expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
#                         content_disposition='inline'
#                     )
#                     result['view_url'] = f"{blob_client.url}?{sas_token}"
                    
#                     props = blob_client.get_blob_properties()
#                     result['file_size'] = props.size
#                     result['last_modified'] = props.last_modified.isoformat()
                    
#                 except Exception as e:
#                     app.logger.error(f"Error generating SAS URL for blob {blob_name}: {str(e)}")
#                     result['view_url'] = None
        
#         return jsonify({'results': results})
#     except requests.exceptions.RequestException as e:
#         app.logger.error(f"Search API error: {str(e)}")
#         return jsonify({'error': 'Search service error. Please try again later.'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import os
import requests
import datetime
from functools import wraps

# Load environment variables
load_dotenv()

# Configuration
SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")
API_KEY = os.getenv("API_KEY")
API_VERSION = os.getenv("API_VERSION")
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")

# Initialize Flask app
app = Flask(__name__)
# Use a secure secret key from environment variable or generate a random one
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

# Fetch credentials from environment variables
VALID_CREDENTIALS = {
    os.getenv("ADMIN_USERNAME", "admin"): os.getenv("ADMIN_PASSWORD", "K9#mP2$vL5@nX8")
}

# Build Azure Search endpoint
endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version={API_VERSION}"

# Blob client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index4.html')

@app.route('/search', methods=['POST'])
@login_required
def search():
    user_query = request.form.get('query')
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "search": user_query,
        "searchFields": "content,metadata_storage_name",
        "select": "content,metadata_storage_name,metadata_storage_path",
        "scoringProfile": "contentBoost",
        "top": 10,
        "queryType": "full",
        "searchMode": "all"
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        results = response.json().get("value", [])
        
        for result in results:
            if 'metadata_storage_path' in result:
                try:
                    blob_name = result['metadata_storage_name']
                    blob_client = container_client.get_blob_client(blob_name)
                    
                    if not blob_client.exists():
                        result['view_url'] = None
                        continue
                    
                    ext = blob_name.lower().split('.')[-1] if '.' in blob_name else ''
                    result['file_type'] = {
                        'pdf': 'pdf',
                        'doc': 'word', 'docx': 'word',
                        'xls': 'excel', 'xlsx': 'excel',
                        'ppt': 'powerpoint', 'pptx': 'powerpoint',
                        'txt': 'text',
                        'json': 'text',
                        'csv': 'text'
                    }.get(ext, 'other')
                    
                    sas_token = generate_blob_sas(
                        account_name=blob_service_client.account_name,
                        container_name=CONTAINER_NAME,
                        blob_name=blob_name,
                        account_key=ACCOUNT_KEY,
                        permission=BlobSasPermissions(read=True),
                        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                        content_disposition='inline'
                    )
                    result['view_url'] = f"{blob_client.url}?{sas_token}"
                    
                    props = blob_client.get_blob_properties()
                    result['file_size'] = props.size
                    result['last_modified'] = props.last_modified.isoformat()
                    
                except Exception as e:
                    app.logger.error(f"Error generating SAS URL for blob {blob_name}: {str(e)}")
                    result['view_url'] = None
        
        return jsonify({'results': results})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Search API error: {str(e)}")
        return jsonify({'error': 'Search service error. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)