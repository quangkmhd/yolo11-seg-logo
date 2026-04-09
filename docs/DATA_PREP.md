# Dataset Preparation Guide

Preparing your dataset correctly is the most important step in achieving high-accuracy logo segmentation.

## 1. Labeling (Labelme)

1. Use the [Labelme](https://github.com/wkentaro/labelme) annotation tool.
2. Annotate logos using the **Polygon** tool (not rectangles). Instance segmentation requires precise pixel boundaries.
3. Save each annotation as a JSON file in the same folder as the corresponding image.

## 2. Consolidating Sources

If you have data from multiple sources (e.g., recorded video frames, web scrapes, manual photography), use the processing tool to merge them:

```bash
python main.py data process --sources /path/to/source1 /path/to/source2
```
*The tool will handle filename conflicts by adding copy suffixes.*

## 3. Formatting for YOLO11-Seg

Once your images and JSON files are in one directory (defined by `SOURCE_DATA_DIR` in `.env`), run the converter:

```bash
python main.py data convert --train-split 0.8
```

### What this does:
1. **Creates Directory Structure**: Sets up `train/` and `val/` subfolders for both images and labels.
2. **Normalizes Coordinates**: Converts Labelme pixel coordinates into normalized [0, 1] values required by YOLO.
3. **Generates Metadata**: Automatically creates the `data.yaml` file with the correct class names found in your JSON files.

## 4. Best Practices for Logos

- **Background Diversity**: Include images where logos are not present (background class) to reduce false positives.
- **Lighting and Distortion**: Ensure your dataset has logos in poor lighting or on curved surfaces (like t-shirts).
- **Class Labels**: Be consistent with label names (e.g., don't mix `Nike` and `nike_logo`).
