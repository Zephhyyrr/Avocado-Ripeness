import os
import uuid
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Import Modules
import config
from utils.image_utils import allowed_file, preprocess_image
from utils.model_utils import model_handler
from utils.pdf_utils import create_batch_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['GRAPH_FOLDER'] = config.GRAPH_FOLDER

# --- ROUTES ---
@app.route('/', methods=['GET'])
def index():
    models = model_handler.get_available_models()
    return render_template('index.html', models=models)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('file') # Get multiple files
    selected_model_name = request.form.get('selected_model')
    
    if not files or files[0].filename == '':
        return 'No selected file'
        
    if not selected_model_name:
        return "Please select a model."

    # Load Model Once
    model = model_handler.get_model(selected_model_name)
    if not model:
        return "Model not found or failed to load."

    results = []
    batch_id = str(uuid.uuid4())[:8] # Unique ID for this batch request

    for i, file in enumerate(files):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_id = f"{batch_id}_{i}"
            filename_base = f"{unique_id}_{os.path.splitext(filename)[0]}"
            
            save_filename = f"{unique_id}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], save_filename)
            file.save(save_path)
            
            # Preprocess
            img_array = preprocess_image(save_path)
            
            # Predict
            pred_probs = model.predict(img_array)[0]
            pred_idx = np.argmax(pred_probs)
            confidence = float(np.max(pred_probs))
            
            # Get threshold for this model (if exists)
            threshold = config.MODEL_THRESHOLDS.get(selected_model_name)
            
            # Check if confidence meets threshold
            if threshold is not None:
                if confidence >= threshold:
                    predicted_class = config.CLASS_LABELS[pred_idx]
                else:
                    predicted_class = "Bukan Alpukat"
            else:
                # No threshold for this model, use prediction directly
                predicted_class = config.CLASS_LABELS[pred_idx]
            
            results.append({
                'image_filename': save_filename,
                'image_path': save_path,
                'model_name': selected_model_name,
                'prediction': predicted_class,
                'confidence': confidence
            })

    if not results:
        return "No valid images processed."

    # Generate Batch PDF using all results
    pdf_filename = create_batch_pdf(batch_id, results)
    
    return render_template('result.html', 
                           results=results,
                           model_name=selected_model_name,
                           pdf_filename=pdf_filename)

if __name__ == '__main__':
    print(f"Server starting...")
    app.run(debug=True)
