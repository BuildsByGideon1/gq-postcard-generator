#!/usr/bin/env python3
"""
QR Postcard Generator API
=========================

Flask API that accepts a postcard image and URL via webhook,
generates a QR code, and returns the postcard with QR code applied.

Features:
- Percentage-based QR positioning for scalable postcards
- API key authentication for security
- Automatic scaling based on postcard dimensions

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
from functools import wraps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# QR Positioning Configuration (percentage-based)
QR_CENTER_X_PERCENT = 84.73  # 84.73% of width
QR_CENTER_Y_PERCENT = 78.59  # 78.59% of height
QR_SIZE_PERCENT = 15.88      # 15.88% of width

# Postcard type configurations
POSTCARD_TYPES = {
    '6x4': {
        'min_width': 576,
        'min_height': 384,
        'aspect_ratio': 6/4,
        'pdf_width_inches': 6.25,
        'pdf_height_inches': 4.25
    },
    '9x6': {
        'min_width': 864,
        'min_height': 576,
        'aspect_ratio': 9/6,
        'pdf_width_inches': 9.25,
        'pdf_height_inches': 6.25
    },
    '11x6': {
        'min_width': 1056,
        'min_height': 576,
        'aspect_ratio': 11/6,
        'pdf_width_inches': 11.25,
        'pdf_height_inches': 6.25
    }
}

# API Key for security
API_KEY = os.environ.get('API_KEY', 'your-secret-api-key-change-this')

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.form.get('api_key')

        if not api_key:
            return jsonify({'error': 'API key required. Provide via X-API-Key header or api_key form field.'}), 401

        if api_key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 403

        return f(*args, **kwargs)
    return decorated_function

def calculate_qr_position(postcard_width, postcard_height):
    """Calculate QR position and size based on postcard dimensions"""

    # Calculate QR size based on percentage of width
    qr_size = int((QR_SIZE_PERCENT / 100) * postcard_width)

    # Calculate center position based on percentages
    center_x = int((QR_CENTER_X_PERCENT / 100) * postcard_width)
    center_y = int((QR_CENTER_Y_PERCENT / 100) * postcard_height)

    # Calculate top-left position
    top_left_x = center_x - (qr_size // 2)
    top_left_y = center_y - (qr_size // 2)

    # Ensure QR doesn't go outside bounds
    top_left_x = max(0, min(top_left_x, postcard_width - qr_size))
    top_left_y = max(0, min(top_left_y, postcard_height - qr_size))

    return {
        'size': qr_size,
        'center_x': center_x,
        'center_y': center_y,
        'top_left_x': top_left_x,
        'top_left_y': top_left_y
    }

def detect_background_color(postcard_image, center_x, center_y):
    """Detect the background color at the QR center position"""
    # Get the pixel color at the center of where QR will be placed
    pixel_color = postcard_image.getpixel((center_x, center_y))

    # Convert to RGB if it's RGBA
    if len(pixel_color) == 4:
        pixel_color = pixel_color[:3]

    # Check if the color is black or very dark (sum of RGB < 30)
    if sum(pixel_color) < 30:
        return "white"  # Use white if background is black/dark

    # Convert RGB tuple to hex string
    return f"#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}"

def generate_qr_code(url, background_color="#cefe05"):
    """Generate QR code with specified background color"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,  # Minimal border for larger QR
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR with detected background color
    qr_img = qr.make_image(fill_color="black", back_color=background_color)
    return qr_img

def apply_qr_to_postcard(postcard_image, qr_url):
    """Apply QR code to postcard at calculated percentage-based position with matching background color"""

    # Get postcard dimensions
    postcard_width, postcard_height = postcard_image.size

    # Calculate QR position and size based on percentages
    qr_config = calculate_qr_position(postcard_width, postcard_height)

    # Detect background color at QR center position
    background_color = detect_background_color(postcard_image, qr_config['center_x'], qr_config['center_y'])

    # Generate QR code with detected background color
    qr_image = generate_qr_code(qr_url, background_color)

    # Resize QR to calculated size
    qr_resized = qr_image.resize((qr_config['size'], qr_config['size']), Image.Resampling.LANCZOS)

    # Apply QR to postcard at calculated position
    postcard_image.paste(qr_resized, (qr_config['top_left_x'], qr_config['top_left_y']))

    # Add background color info to config for debugging
    qr_config['background_color'] = background_color

    return postcard_image, qr_config

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'QR Postcard Generator',
        'version': '2.0.0',
        'features': [
            'Percentage-based QR positioning',
            'API key authentication',
            'Scalable postcard support',
            'Auto-matching QR background colors'
        ],
        'qr_config': {
            'center_x_percent': QR_CENTER_X_PERCENT,
            'center_y_percent': QR_CENTER_Y_PERCENT,
            'size_percent': QR_SIZE_PERCENT,
            'background_color': 'Auto-detected from postcard'
        }
    })

@app.route('/generate-qr-postcard', methods=['POST'])
@require_api_key
def generate_qr_postcard():
    """
    Main webhook endpoint with API key authentication

    Accepts:
    - image: postcard image file (multipart/form-data)
    - url: URL to encode in QR code (form field)
    - postcard_type: Type of postcard (6x4, 9x6, or 11x6)
    - api_key: API key for authentication (form field OR X-API-Key header)

    Returns:
    - PDF file with QR code applied at percentage-based position
    - Custom headers with QR positioning info for debugging
    """

    try:
        # Validate request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        if 'url' not in request.form:
            return jsonify({'error': 'No URL provided'}), 400

        if 'postcard_type' not in request.form:
            return jsonify({'error': 'No postcard_type provided'}), 400

        image_file = request.files['image']
        qr_url = request.form['url']
        postcard_type = request.form['postcard_type']

        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400

        # Validate URL
        if not qr_url or len(qr_url.strip()) == 0:
            return jsonify({'error': 'URL cannot be empty'}), 400

        # Validate postcard type
        if postcard_type not in POSTCARD_TYPES:
            valid_types = list(POSTCARD_TYPES.keys())
            return jsonify({'error': f'Invalid postcard_type. Valid types: {valid_types}'}), 400

        # Load and validate image
        try:
            postcard = Image.open(image_file.stream)

            # Validate image dimensions based on postcard type
            width, height = postcard.size
            min_config = POSTCARD_TYPES[postcard_type]

            if width < min_config['min_width'] or height < min_config['min_height']:
                return jsonify({
                    'error': f'Image too small for {postcard_type}. Minimum: {min_config["min_width"]}x{min_config["min_height"]}px'
                }), 400

        except Exception as e:
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

        # Apply QR code with percentage-based positioning
        result_postcard, qr_config = apply_qr_to_postcard(postcard, qr_url.strip())

        # Convert image to PDF with standard postcard dimensions
        pdf_buffer = io.BytesIO()

        # Get postcard type configuration for PDF dimensions
        postcard_config = POSTCARD_TYPES[postcard_type]

        # Convert inches to points (1 inch = 72 points)
        pdf_width_points = postcard_config['pdf_width_inches'] * 72
        pdf_height_points = postcard_config['pdf_height_inches'] * 72

        # Create PDF canvas with standard postcard dimensions
        c = canvas.Canvas(pdf_buffer, pagesize=(pdf_width_points, pdf_height_points))

        # Convert PIL image to ReportLab ImageReader
        img_buffer = io.BytesIO()
        result_postcard.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_reader = ImageReader(img_buffer)

        # Scale and fit the image to the PDF page
        # The image will be scaled to fit the entire PDF page
        c.drawImage(img_reader, 0, 0, width=pdf_width_points, height=pdf_height_points)
        c.save()

        pdf_buffer.seek(0)

        # Add QR configuration to response headers for debugging
        response = send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='qr_postcard.pdf'
        )

        # Add custom headers with QR positioning info
        response.headers['X-QR-Size'] = str(qr_config['size'])
        response.headers['X-QR-Center-X'] = str(qr_config['center_x'])
        response.headers['X-QR-Center-Y'] = str(qr_config['center_y'])
        response.headers['X-QR-Background-Color'] = qr_config['background_color']
        response.headers['X-Postcard-Size'] = f"{postcard.size[0]}x{postcard.size[1]}"
        response.headers['X-Postcard-Type'] = postcard_type
        response.headers['X-PDF-Dimensions'] = f"{postcard_config['pdf_width_inches']}x{postcard_config['pdf_height_inches']} inches"

        return response

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'QR Postcard Generator API',
        'version': '2.0.0',
        'description': 'Scalable QR postcard generation with percentage-based positioning, outputs PDF files',
        'features': [
            'Percentage-based QR positioning',
            'API key authentication',
            'Automatic scaling for any postcard size',
            'Optimal QR placement ratios',
            'PDF output format'
        ],
        'endpoints': {
            'POST /generate-qr-postcard': {
                'description': 'Generate QR postcard with authentication',
                'authentication': 'Required via X-API-Key header or api_key form field',
                'parameters': {
                    'image': 'Postcard image file (multipart/form-data)',
                    'url': 'URL to encode in QR code (form field)',
                    'postcard_type': 'Type of postcard: 6x4, 9x6, or 11x6 (form field)',
                    'api_key': 'API key (form field, optional if using header)'
                },
                'headers': {
                    'X-API-Key': 'API key (alternative to form field)'
                },
                'returns': 'PDF file with QR code applied at optimal position',
                'response_headers': [
                    'X-QR-Size: QR code size in pixels',
                    'X-QR-Center-X: QR center X coordinate',
                    'X-QR-Center-Y: QR center Y coordinate',
                    'X-QR-Background-Color: Auto-detected QR background color',
                    'X-Postcard-Size: Original postcard dimensions',
                    'X-Postcard-Type: Postcard type used',
                    'X-PDF-Dimensions: PDF output dimensions in inches'
                ]
            },
            'GET /health': 'Health check and configuration',
            'GET /': 'This documentation'
        },
        'qr_configuration': {
            'positioning': 'Percentage-based for scalability',
            'center_x_percent': f'{QR_CENTER_X_PERCENT}%',
            'center_y_percent': f'{QR_CENTER_Y_PERCENT}%',
            'size_percent': f'{QR_SIZE_PERCENT}% of width',
            'background_color': 'Auto-detected from postcard (white if black detected)',
            'border': 'Minimal (1px)'
        },
        'security': {
            'api_key_required': True,
            'methods': ['X-API-Key header', 'api_key form field']
        },
        'postcard_types': {
            '6x4': {'min_size': '576x384px', 'aspect_ratio': '1.5:1', 'pdf_size': '6.25"x4.25"'},
            '9x6': {'min_size': '864x576px', 'aspect_ratio': '1.5:1', 'pdf_size': '9.25"x6.25"'},
            '11x6': {'min_size': '1056x576px', 'aspect_ratio': '1.83:1', 'pdf_size': '11.25"x6.25"'}
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)