from ultralytics import YOLO
import torch

def main():
    # 1. PHẢI THAY ĐỔI: Thêm đuôi -seg để dùng mô hình Phân đoạn
    model = YOLO("yolo11n-seg.pt") 
    
    results = model.train(
        # Lưu ý: file data.yaml của bạn cũng phải định dạng cho segmentation 
        # (có chứa tọa độ các điểm bao quanh vật thể thay vì chỉ có tọa độ khung)
        data="/home/quangnhvn34/fsoft/detect/yolo11/yolo_dataset/data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        device="0",
        project="yolo11/checkpoints", 
        name="yolo11n_logo_seg", # Đổi tên project để tránh ghi đè
        verbose=True,
    )

    metrics = model.val()
    
    print(f"\n📊 Kết quả các chỉ số mAP cho Segmentation:")
    # Chỉ số dành cho Mask (Phần tô màu)
    print(f"mAP Mask (50-95): {metrics.seg.map:.4f}")
    print(f"mAP Mask (50):    {metrics.seg.map50:.4f}")
    
    # Bạn vẫn có thể in cả chỉ số Box (Khung bao) nếu muốn
    print(f"mAP Box (50-95):  {metrics.box.map:.4f}")

if __name__ == '__main__':
    main()