import os
from fpdf import FPDF
from config import UPLOAD_FOLDER

def create_batch_pdf(filename_base, results):
    """
    results: List of dicts, each containing:
    {
        'image_path': ...,
        'model_name': ...,
        'prediction': ...,
        'confidence': ...,
        'graph_path': ...
    }
    """
    pdf = FPDF()
    
    # Title Page
    pdf.add_page()
    pdf.set_font("Arial", size=24, style='B')
    pdf.cell(190, 20, txt="Laporan Deteksi Alpukat", ln=True, align='C')
    pdf.set_font("Arial", size=14)
    pdf.cell(190, 10, txt=f"Total Gambar: {len(results)}", ln=True, align='C')
    pdf.ln(20)
    
    for i, res in enumerate(results):
        # New page for each result (or 2 per page if fitted, but 1 is cleaner for now with graphs)
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(190, 10, txt=f"Gambar #{i+1}", ln=True, align='L')
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        # Image
        # Center image
        img_width = 80
        x_centered = (210 - img_width) / 2
        pdf.image(res['image_path'], x=x_centered, w=img_width)
        pdf.ln(5)
        
        # Prediction Info
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 8, txt=f"Model: {res['model_name']}", ln=True, align='C')
        
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(190, 10, txt=f"Prediksi: {res['prediction']}", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.cell(190, 8, txt=f"Confidence: {res['confidence']:.2%}", ln=True, align='C')
        
        pdf.ln(5)
        
        # Confidence Graph - Removed from UI, removed from PDF as requested or just skipped if None
        # if res['graph_path'] and os.path.exists(res['graph_path']):
        #    pdf.image(res['graph_path'], x=35, w=140)
        
    
    pdf_filename = f'{filename_base}_batch_report.pdf'
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
    pdf.output(pdf_path)
    return pdf_filename
