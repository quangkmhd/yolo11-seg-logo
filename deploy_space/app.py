import gradio as gr
from ultralytics import YOLO
import cv2
import numpy as np

# Load the model
# NOTE: In Hugging Face Spaces, you should upload your 'best.pt' 
# to the root of the repository or a subfolder.
# Here we assume it's in the root or same relative path.
model = YOLO("best.pt") 

def predict(image):
    results = model(image)
    # Visualize the results
    for result in results:
        im_array = result.plot()  # plot a BGR numpy array of predictions
        im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB) # RGB
        return im_rgb

iface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="numpy", label="Upload an Image"),
    outputs=gr.Image(type="numpy", label="Prediction"),
    title="YOLO11 Object Detection/Segmentation",
    description="Upload an image to detect/segment objects using YOLO11."
)

if __name__ == "__main__":
    iface.launch(share=True)
