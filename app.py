#!/usr/bin/env python3
"""
QR Postcard Generator API
=========================

Flask API that accepts a postcard image and URL via webhook,
generates a QR code, and returns the postcard with QR code applied.

Endpoint: POST /generate-qr-postcard
"""

from flask import Flask, request, jsonify, send_file
from PIL import Image
import qrcode
import io
import base64
import tempfile
import os
from werkzeug.utils import secure_filename

# Import our optimal QR placement configuration
from optimal_qr_placement import QR_SIZE, CENTER_X, CENTER_Y, TOP_LEFT_X, TOP_LEFT_Y

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def generate_qr_code(url):
    """Generate QR code with optimal settings"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,  # Minimal border for larger QR
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR with yellow-green background
    qr_img = qr.make_image(fill_color="black", back_color="#cefe05")
    return qr_img

def apply_qr_to_postcard(postcard_image, qr_url):
    """Apply QR code to postcard at optimal position"""

    # Generate QR code
    qr_image = generate_qr_code(qr_url)

    # Resize QR to optimal size
    qr_resized = qr_image.resize((QR_SIZE, QR_SIZE), Image.Resampling.LANCZOS)

    # Apply QR to postcard
    postcard_image.paste(qr_resized, (TOP_LEFT_X, TOP_LEFT_Y))

    return postcard_image

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'QR Postcard Generator',
        'qr_config': {
            'size': QR_SIZE,
            'center': [CENTER_X, CENTER_Y],
            'top_left': [TOP_LEFT_X, TOP_LEFT_Y]
        }
    })

@app.route('/generate-qr-postcard', methods=['POST'])
def generate_qr_postcard():
    """
    Main webhook endpoint

    Accepts:
    - image: postcard image file (multipart/form-data)
    - url: URL to encode in QR code (form field)

    Returns:
    - Postcard image with QR code applied
    """

    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        if 'url' not in request.form:
            return jsonify({'error': 'No URL provided'}), 400

        image_file = request.files['image']
        qr_url = request.form['url']

        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400

        # Validate URL
        if not qr_url or len(qr_url.strip()) == 0:
            return jsonify({'error': 'URL cannot be empty'}), 400

        # Load and validate image
        try:
            postcard = Image.open(image_file.stream)

            # Validate image dimensions (should be close to our test dimensions)
            width, height = postcard.size
            if width < 1000 or height < 1000:  # Basic size check
                return jsonify({'error': 'Image too small (minimum 1000x1000px)'}), 400

        except Exception as e:
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

        # Apply QR code
        result_postcard = apply_qr_to_postcard(postcard, qr_url.strip())

        # Save to memory buffer
        img_buffer = io.BytesIO()
        result_postcard.save(img_buffer, format='PNG', optimize=True)
        img_buffer.seek(0)

        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='qr_postcard.png'
        )

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'QR Postcard Generator API',
        'version': '1.0.0',
        'endpoints': {
            'POST /generate-qr-postcard': {
                'description': 'Generate QR postcard',
                'parameters': {
                    'image': 'Postcard image file (multipart/form-data)',
                    'url': 'URL to encode in QR code (form field)'
                },
                'returns': 'PNG image with QR code applied'
            },
            'GET /health': 'Health check and configuration'
        },
        'qr_placement': {
            'size': f'{QR_SIZE}x{QR_SIZE}px',
            'center': [CENTER_X, CENTER_Y],
            'background_color': '#cefe05'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)