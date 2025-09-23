# Deployment Instructions

## GitHub Setup

1. **Initialize Git Repository:**
```bash
git init
git add .
git commit -m "Initial QR Postcard Generator API

🚀 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

2. **Create GitHub Repository:**
- Go to https://github.com/new
- Repository name: `qr-postcard-generator`
- Description: "Flask API that generates QR codes and applies them to postcard images"
- Make it Public
- Don't initialize with README (we already have one)

3. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/qr-postcard-generator.git
git branch -M main
git push -u origin main
```

## Railway Deployment

1. **Connect to Railway:**
- Go to https://railway.app
- Sign up/login with GitHub
- Click "New Project" → "Deploy from GitHub repo"
- Select your `qr-postcard-generator` repository

2. **Railway will automatically:**
- Detect it's a Python app
- Install dependencies from `requirements.txt`
- Use `Procfile` to start with gunicorn
- Set the correct Python version from `runtime.txt`

3. **Get Your API URL:**
- After deployment, Railway will give you a URL like:
- `https://your-app-name.railway.app`

## Testing Your Deployed API

```bash
# Test health endpoint
curl https://your-app-name.railway.app/health

# Test QR generation
curl -X POST \
  -F "image=@postcardSampleBlank.png" \
  -F "url=https://example.com/test" \
  https://your-app-name.railway.app/generate-qr-postcard \
  --output result.png
```

## API Usage

### Webhook URL
```
POST https://your-app-name.railway.app/generate-qr-postcard
```

### Parameters
- `image`: Postcard image file (multipart/form-data)
- `url`: URL to encode in QR code

### Response
- PNG image with QR code applied at optimal position

### Example with curl:
```bash
curl -X POST \
  -F "image=@your_postcard.png" \
  -F "url=https://your-campaign-url.com" \
  https://your-app-name.railway.app/generate-qr-postcard \
  --output final_postcard.png
```

### Example with Python:
```python
import requests

with open("postcard.png", "rb") as f:
    response = requests.post(
        "https://your-app-name.railway.app/generate-qr-postcard",
        files={"image": f},
        data={"url": "https://your-url.com"}
    )

if response.status_code == 200:
    with open("result.png", "wb") as f:
        f.write(response.content)
```

## Configuration

The QR code is positioned at:
- **Size:** 880x880 pixels
- **Center:** (4695, 2940)
- **Background:** #cefe05
- **Border:** Minimal (1px)

These settings are optimized for your specific postcard template.