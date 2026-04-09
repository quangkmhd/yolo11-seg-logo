import gradio as gr
import cv2
import numpy as np
from ..models.predictor import Predictor
from ..utils.logger import get_logger

logger = get_logger("app")

def create_app(model_path: str = None):
    predictor = Predictor(model_path)

    def predict_image(image):
        results = predictor.predict(image, stream=False)
        for result in results:
            # result.plot() returns a BGR numpy array
            im_array = result.plot()
            im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)
            return im_rgb
        return image

    interface = gr.Interface(
        fn=predict_image,
        inputs=gr.Image(type="numpy", label="Upload an Image"),
        outputs=gr.Image(type="numpy", label="Prediction"),
        title="YOLO11 Logo Segmentation",
        description="Upload an image to detect and segment logos using YOLO11."
    )
    
    return interface

if __name__ == "__main__":
    app = create_app()
    app.launch()
