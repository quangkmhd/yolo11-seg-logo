import os
import json
import shutil
import glob
import random
from pathlib import Path
from typing import List, Dict
from ..utils.logger import get_logger
from ..config import Config

logger = get_logger("converter")

class LabelmeToYoloConverter:
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        
    def _convert_single_file(self, json_file: Path, classes: List[str]) -> List[str]:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        image_width = data['imageWidth']
        image_height = data['imageHeight']
        yolo_annotations = []
        
        for shape in data['shapes']:
            label = shape['label']
            if label not in classes:
                continue
            
            class_id = classes.index(label)
            points = shape['points']
            
            # Segmentation format: class_id x1 y1 x2 y2 ...
            normalized_points = []
            for p in points:
                px = p[0] / image_width
                py = p[1] / image_height
                normalized_points.append(f"{px:.6f} {py:.6f}")
            
            points_str = " ".join(normalized_points)
            yolo_annotations.append(f"{class_id} {points_str}")
            
        return yolo_annotations

    def run(self, train_split: float = 0.8):
        # Reset output directory
        if self.output_dir.exists():
            logger.info(f"Cleaning output directory: {self.output_dir}")
            shutil.rmtree(self.output_dir)
            
        for split in ['train', 'val']:
            (self.output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
            (self.output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)
            
        json_files = list(self.source_dir.glob('*.json'))
        if not json_files:
            logger.error(f"No JSON files found in {self.source_dir}")
            return

        # Discover classes
        all_labels = set()
        for jf in json_files:
            with open(jf, 'r') as f:
                d = json.load(f)
                for s in d['shapes']:
                    all_labels.add(s['label'])
        
        classes = sorted(list(all_labels))
        logger.info(f"Classes found: {classes}")
        
        random.seed(42)
        random.shuffle(json_files)
        split_idx = int(len(json_files) * train_split)
        
        file_splits = {'train': json_files[:split_idx], 'val': json_files[split_idx:]}
        
        for split, files in file_splits.items():
            logger.info(f"Processing {split} split ({len(files)} files)...")
            for json_file in files:
                base_name = json_file.stem
                
                # Find matching image
                image_file = None
                for ext in ['.png', '.jpg', '.jpeg', '.bmp']:
                    candidate = self.source_dir / (base_name + ext)
                    if candidate.exists():
                        image_file = candidate
                        break

                if not image_file:
                    continue
                    
                annotations = self._convert_single_file(json_file, classes)
                if not annotations:
                    continue

                # Copy image
                shutil.copy(str(image_file), str(self.output_dir / 'images' / split / image_file.name))
                
                # Save label
                with open(self.output_dir / 'labels' / split / (base_name + '.txt'), 'w') as f:
                    f.write('\n'.join(annotations))
                    
        # Create data.yaml
        yaml_content = {
            'path': str(self.output_dir.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'nc': len(classes),
            'names': classes
        }
        
        import yaml
        with open(self.output_dir / 'data.yaml', 'w') as f:
            yaml.dump(yaml_content, f, default_flow_style=False)
            
        logger.info(f"Conversion complete! Dataset ready at: {self.output_dir}")

if __name__ == "__main__":
    converter = LabelmeToYoloConverter(str(Config.SOURCE_DATA_DIR), str(Config.OUTPUT_DATA_DIR))
    converter.run()
