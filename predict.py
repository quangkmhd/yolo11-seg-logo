from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("/home/quangnhvn34/fsoft/detect/yolo11/checkpoints/yolo11n_logo_seg2/weights/best.pt")

# Define path to video file
source = "path/to/video.mp4"

# Run inference on the source
results = model(source, stream=True)  # generator of Results objects

# Access the results
for result in results:
    xy = result.masks.xy  # mask in polygon format
    xyn = result.masks.xyn  # normalized
    masks = result.masks.data  # mask in matrix format (num_objects x H x W)
    