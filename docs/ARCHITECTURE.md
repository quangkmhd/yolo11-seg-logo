# System Architecture: YOLO11 Logo Segmentation

## 1. Architectural Overview

The YOLO11 Logo Segmentation toolkit is structured around the Ultralytics YOLO (You Only Look Once) ecosystem. The project follows a **modular production architecture** to ensure scalability, ease of maintenance, and professional-grade deployment.

The codebase is organized into a core package `logo_seg` containing distinct modules for data processing, modeling, and application interfaces.

---

## 2. Package Structure

### 2.1 Core Package (`src/logo_seg/`)
- **`config.py`**: The central brain of the system. It manages all paths, training parameters, and environment settings. It supports `.env` files for seamless environment switching.
- **`utils/logger.py`**: Provides standardized logging across the entire application, replacing basic `print` statements with formatted output and timestamps.

### 2.2 Data Module (`src/logo_seg/data/`)
- **`preprocessor.py`**: Handles raw data organization. It safely moves and renames files from multiple source directories into a unified structure, handling filename collisions automatically.
- **`converter.py`**: A specialized engine that converts standard Labelme JSON annotations into the pixel-perfect segmentation format required by YOLO11 (`class x1 y1 x2 y2 ...`).

### 2.3 Modeling Module (`src/logo_seg/models/`)
- **`trainer.py`**: A high-level wrapper for the Ultralytics training engine. It automatically detects hardware (CUDA), loads the correct `data.yaml`, and initiates the training loop with optimized hyperparameters.
- **`predictor.py`**: A reusable class-based inference engine. It can be initialized with any model checkpoint and provides a unified interface for predicting on images or video streams.

### 2.4 Application Module (`src/logo_seg/app/`)
- **`interface.py`**: Houses the Gradio web interface logic. By decoupling the UI from the model logic, we can easily swap between web apps, CLI tools, or REST APIs.

---

## 3. Data Flow

### Training Workflow
1. **Raw Inputs**: Images + Labelme JSONs are placed in a source directory.
2. **Preprocessing**: `python main.py data process` consolidates files.
3. **Conversion**: `python main.py data convert` transforms annotations and generates `data.yaml`.
4. **Training**: `python main.py train` executes the YOLO11n-seg training loop.
5. **Output**: Best-performing weights are saved to `yolo11/checkpoints`.

### Unified CLI Entry Point
The `main.py` at the project root acts as the orchestrator, importing specialized functions from the underlying package to execute tasks based on CLI arguments.

---

## 4. Containerization

The project includes a `Dockerfile` based on the official Ultralytics runtime. This ensures that the complex dependencies (CUDA, PyTorch, FFmpeg) are correctly configured for any production environment.