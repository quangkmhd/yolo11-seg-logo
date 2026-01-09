import os
import json
import shutil
import glob
import random

# Configuration
SOURCE_DIR = '/home/quangnhvn34/fsoft/detect/data_logo'
OUTPUT_DIR = '/home/quangnhvn34/fsoft/detect/yolo_dataset'

def convert_labelme_to_yolo(json_file, classes):
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
        
        # CHUẨN SEGMENTATION: Lấy tất cả các điểm x, y
        normalized_points = []
        for p in points:
            px = p[0] / image_width
            py = p[1] / image_height
            normalized_points.append(f"{px:.6f} {py:.6f}")
        
        points_str = " ".join(normalized_points)
        yolo_annotations.append(f"{class_id} {points_str}")
        
    return yolo_annotations

def main():
    # Xóa và tạo mới thư mục output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        
    for split in ['train', 'val']:
        os.makedirs(os.path.join(OUTPUT_DIR, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(OUTPUT_DIR, 'labels', split), exist_ok=True)
        
    json_files = glob.glob(os.path.join(SOURCE_DIR, '*.json'))
    
    # Lấy danh sách class
    all_labels = set()
    for jf in json_files:
        with open(jf, 'r') as f:
            d = json.load(f)
            for s in d['shapes']:
                all_labels.add(s['label'])
    
    classes = sorted(list(all_labels))
    print(f"Classes found: {classes}")
    
    random.seed(42)
    random.shuffle(json_files)
    split_idx = int(len(json_files) * 0.8)
    
    file_splits = {'train': json_files[:split_idx], 'val': json_files[split_idx:]}
    
    for split, files in file_splits.items():
        for json_file in files:
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            
            # Tìm ảnh tương ứng (không phân biệt hoa thường)
            image_file = None
            possible_images = glob.glob(os.path.join(SOURCE_DIR, base_name + ".*"))
            for p_img in possible_images:
                if p_img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_file = p_img
                    break

            if not image_file:
                continue
                
            # Convert và lưu
            annotations = convert_labelme_to_yolo(json_file, classes)
            if not annotations: continue # Bỏ qua nếu file json không có polygon hợp lệ

            # Lưu ảnh
            shutil.copy(image_file, os.path.join(OUTPUT_DIR, 'images', split, os.path.basename(image_file)))
            
            # Lưu label txt
            with open(os.path.join(OUTPUT_DIR, 'labels', split, base_name + '.txt'), 'w') as f:
                f.write('\n'.join(annotations))
                
    # Tạo data.yaml với đường dẫn tương đối (tốt cho tính di động)
    yaml_content = f"""
path: {OUTPUT_DIR} # Thư mục gốc của dataset
train: images/train
val: images/val

nc: {len(classes)}
names: {classes}
"""
    with open(os.path.join(OUTPUT_DIR, 'data.yaml'), 'w') as f:
        f.write(yaml_content.strip())
        
    print(f"✅ Xong! Dữ liệu Segmentation đã sẵn sàng tại: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()