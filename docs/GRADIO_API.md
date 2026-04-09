# Gradio API & Web Interface

The web interface provided by `main.py serve` allows for both interactive usage and programmatic integration via a REST API.

## 1. Interactive Usage

1. Launch the server: `python main.py serve`.
2. Open `http://localhost:7860` in your browser.
3. **Upload an Image**: Drag and drop any image file.
4. **View Results**: The system will overlay highly accurate colored segmentation masks over any detected logos.

## 2. API Integration

Every Gradio app is also a web service. You can use the `gradio_client` Python library to interact with it from other applications.

### 2.1 Python Client Example
```bash
pip install gradio_client
```

```python
from gradio_client import Client

client = Client("http://localhost:7860")
result = client.predict(
		"path/to/my_image.jpg",	# str (filepath or URL to image)
		api_name="/predict"
)
print(f"Processed image saved at: {result}")
```

### 2.2 Raw HTTP Example
You can use `curl` or any HTTP library:

```bash
curl -X POST http://localhost:7860/api/predict \
     -H "Content-Type: application/json" \
     -d '{
       "data": ["data:image/jpeg;base64,/9j/4AAQ..."]
     }'
```

---

## 3. Customizing the UI

The interface logic resides in `src/logo_seg/app/interface.py`. You can modify this file to:
- Change the UI theme or CSS.
- Add additional input parameters (e.g., confidence threshold sliders).
- Customize the output display (e.g., returning raw JSON results instead of an annotated image).
