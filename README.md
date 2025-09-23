# QR Postcard Generator API

A Flask API service that generates QR codes and applies them to postcard images at optimal positions.

## Features

- 🖼️ **Webhook endpoint** for processing postcard images
- 🔗 **QR code generation** with custom URLs
- 📐 **Optimal positioning** (880x880px at position 4695, 2940)
- 🎨 **Custom styling** with #cefe05 background color
- ☁️ **Railway deployment ready**

## API Endpoints

### `POST /generate-qr-postcard`
Main webhook endpoint that accepts a postcard image and URL, returns the image with QR code applied.

**Parameters:**
- `image` (file): Postcard image (multipart/form-data)
- `url` (string): URL to encode in QR code

**Returns:** PNG image with QR code applied

### `GET /health`
Health check endpoint with configuration details.

### `GET /`
API documentation and configuration info.

## Usage Example

```bash
curl -X POST \
  -F "image=@postcard.png" \
  -F "url=https://example.com/campaign" \
  https://your-api-url.railway.app/generate-qr-postcard \
  --output result.png
```

## QR Code Configuration

- **Size:** 880x880 pixels
- **Position:** Center at (4695, 2940), Top-left at (4255, 2500)
- **Background:** #cefe05 (bright yellow-green)
- **Border:** Minimal (1px)

## Development

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

### Testing

```bash
# Test with sample image
curl -X POST \
  -F "image=@postcardSampleBlank.png" \
  -F "url=https://example.com" \
  http://localhost:5000/generate-qr-postcard \
  --output test_result.png
```

## Deployment

### Railway

1. Connect this repository to Railway
2. Railway will automatically detect the Python app
3. Set environment variables if needed
4. Deploy!

The app automatically binds to `PORT` environment variable for Railway compatibility.

## Image Requirements

- **Minimum size:** 1000x1000 pixels
- **Format:** PNG, JPEG, or other PIL-supported formats
- **Maximum size:** 16MB

## License

MIT License - see LICENSE file for details.