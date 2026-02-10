import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
GRAPH_FOLDER = os.path.join(STATIC_FOLDER, 'graphs')
MODELS_FOLDER = os.path.join(BASE_DIR, 'models')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CLASS_LABELS = {0: 'Matang', 1: 'Mentah', 2: 'Setengah Matang'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)
os.makedirs(MODELS_FOLDER, exist_ok=True)
