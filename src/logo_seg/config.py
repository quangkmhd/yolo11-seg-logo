import os
from pathlib import Path

class Config:
    # Project Paths
    ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
    SRC_DIR = ROOT_DIR / "src"
    
    # Data Paths
    SOURCE_DATA_DIR = Path(os.getenv("SOURCE_DATA_DIR", "/home/quangnhvn34/fsoft/detect/data_logo"))
    OUTPUT_DATA_DIR = Path(os.getenv("OUTPUT_DATA_DIR", "/home/quangnhvn34/fsoft/detect/yolo_dataset"))
    
    # Model Paths
    MODEL_CHECKPOINT = os.getenv("MODEL_CHECKPOINT", "best.pt")
    TRAIN_PROJECT = os.getenv("TRAIN_PROJECT", "yolo11/checkpoints")
    TRAIN_NAME = os.getenv("TRAIN_NAME", "yolo11n_logo_seg")
    
    # Training Parameters
    EPOCHS = int(os.getenv("EPOCHS", 100))
    IMGSZ = int(os.getenv("IMGSZ", 640))
    BATCH = int(os.getenv("BATCH", 16))
    DEVICE = os.getenv("DEVICE", "0")
    
    @classmethod
    def ensure_dirs(cls):
        """Ensures that required directories exist."""
        cls.OUTPUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
