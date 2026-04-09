# API & Command Line Reference

The YOLO11 Logo Segmentation toolkit is controlled via a unified Command Line Interface (CLI) and provides clean Python classes for integration.

## 1. CLI Usage (`main.py`)

The `main.py` entry point supports multiple subcommands.

### 1.1 Data Commands
Handles dataset organization and format conversion.

- **Process Raw Files:**
  ```bash
  python main.py data process --sources /path/to/raw1 /path/to/raw2
  ```
- **Convert to YOLO Format:**
  ```bash
  python main.py data convert --train-split 0.8
  ```

### 1.2 Training Command
Initiates the YOLO11 segmentation training loop.

```bash
python main.py train
```
*Settings for epochs, batch size, and device are controlled via `src/logo_seg/config.py` or `.env` variables.*

### 1.3 Prediction Command
Runs inference on a target file or camera.

```bash
python main.py predict --source my_video.mp4 --model best.pt
```

### 1.4 Serving Command
Launches the Gradio web interface.

```bash
python main.py serve --port 7860
```

---

## 2. Python API Reference

You can import the core modules directly into your Python code.

### 2.1 Inference with `Predictor`
```python
from src.logo_seg.models.predictor import Predictor

# Initialize the engine
engine = Predictor(model_path="best.pt")

# Run on a directory
results = engine.predict(source="data/test_images/")

for result in results:
    print(f"Detected {len(result.masks)} logos")
```

### 2.2 Global Settings with `Config`
```python
from src.logo_seg.config import Config

# View current project root
print(Config.ROOT_DIR)

# Access configured output directory
print(Config.OUTPUT_DATA_DIR)
```

---

## 3. Web API (Gradio)

When running the web server (`python main.py serve`), a REST API is automatically exposed.

**Endpoint:** `POST /api/predict`

**Example Request:**
```json
{
  "data": ["data:image/jpeg;base64,..."]
}
```
*Refer to the "Use via API" link at the bottom of the Gradio web page for interactive documentation.*