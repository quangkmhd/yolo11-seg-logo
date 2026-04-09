import os
import shutil

# Danh sách các folder nguồn cần chuyển
source_folders = [
"/home/quangnhvn34/fsoft/detect/data_logo_zip/dhl_23_12"
]

# Folder đích
destination_folder = "/home/quangnhvn34/fsoft/detect/data_logo"

def move_files_safe():
    # 1. Tạo folder đích nếu chưa tồn tại
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Đã tạo folder đích: {destination_folder}")

    count_moved = 0
    
    # 2. Duyệt qua từng folder nguồn
    for src_folder in source_folders:
        if not os.path.exists(src_folder):
            print(f"⚠️ Cảnh báo: Folder không tồn tại -> {src_folder}")
            continue
            
        print(f"--- Đang xử lý: {src_folder} ---")
        
        # Duyệt qua từng file trong folder nguồn
        for filename in os.listdir(src_folder):
            src_path = os.path.join(src_folder, filename)
            
            # Chỉ xử lý nếu là file (bỏ qua folder con nếu có)
            if os.path.isfile(src_path):
                dest_path = os.path.join(destination_folder, filename)
                
                # Xử lý trùng tên: Nếu file đã tồn tại ở đích, thêm hậu tố _copy_1, _copy_2...
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    new_filename = f"{base}_copy_{counter}{extension}"
                    dest_path = os.path.join(destination_folder, new_filename)
                    counter += 1
                
                # Thực hiện di chuyển
                shutil.move(src_path, dest_path)
                count_moved += 1

    print(f"\n✅ Hoàn tất! Đã chuyển tổng cộng {count_moved} file vào {destination_folder}")

if __name__ == "__main__":
    move_files_safe()