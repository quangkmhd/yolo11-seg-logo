from ultralytics import YOLO
from ..utils.logger import get_logger
from ..config import Config
from pathlib import Path

logger = get_logger("predictor")

class Predictor:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or Config.MODEL_CHECKPOINT
        logger.info(f"Loading model from: {self.model_path}")
        self.model = YOLO(self.model_path)

    def predict(self, source, stream=True):
        """Runs inference on the source."""
        logger.info(f"Running inference on: {source}")
        return self.model(source, stream=stream)

if __name__ == "__main__":
    # Example usage
    predictor = Predictor()
    source = "path/to/video.mp4"
    if Path(source).exists():
        results = predictor.predict(source)
        for result in results:
            if result.masks:
                logger.info(f"Detected {len(result.masks)} objects")
    else:
        logger.warning(f"Source not found: {source}")
