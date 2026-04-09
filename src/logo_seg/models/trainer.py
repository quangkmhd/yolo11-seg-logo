from ultralytics import YOLO
from ..utils.logger import get_logger
from ..config import Config

logger = get_logger("trainer")

def train_model():
    """Trains the YOLO11 segmentation model."""
    logger.info("Initializing YOLO11n-seg model...")
    model = YOLO("yolo11n-seg.pt")
    
    data_yaml = Config.OUTPUT_DATA_DIR / "data.yaml"
    if not data_yaml.exists():
        logger.error(f"Data config not found: {data_yaml}. Please run data conversion first.")
        return

    logger.info(f"Starting training on {data_yaml}...")
    results = model.train(
        data=str(data_yaml),
        epochs=Config.EPOCHS,
        imgsz=Config.IMGSZ,
        batch=Config.BATCH,
        device=Config.DEVICE,
        project=Config.TRAIN_PROJECT,
        name=Config.TRAIN_NAME,
        verbose=True,
    )

    logger.info("Validation...")
    metrics = model.val()
    
    logger.info("Segmentation Metrics:")
    logger.info(f"mAP Mask (50-95): {metrics.seg.map:.4f}")
    logger.info(f"mAP Mask (50):    {metrics.seg.map50:.4f}")
    
    return model, results

if __name__ == "__main__":
    train_model()
