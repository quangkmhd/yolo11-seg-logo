import os
import shutil
from pathlib import Path
from typing import List
from ..utils.logger import get_logger
from ..config import Config

logger = get_logger("preprocessor")

def move_files_safe(source_folders: List[str], destination_folder: str):
    """Moves files from multiple source folders to a single destination safely."""
    dest_path = Path(destination_folder)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Moving files to: {dest_path}")
    count_moved = 0
    
    for src_folder in source_folders:
        src_path = Path(src_folder)
        if not src_path.exists():
            logger.warning(f"Source folder does not exist: {src_path}")
            continue
            
        logger.info(f"Processing source: {src_path}")
        
        for file_path in src_path.iterdir():
            if file_path.is_file():
                filename = file_path.name
                target_path = dest_path / filename
                
                # Handle duplicates
                base = file_path.stem
                extension = file_path.suffix
                counter = 1
                while target_path.exists():
                    target_path = dest_path / f"{base}_copy_{counter}{extension}"
                    counter += 1
                
                shutil.move(str(file_path), str(target_path))
                count_moved += 1
                
    logger.info(f"Completed! Moved {count_moved} files.")
    return count_moved

if __name__ == "__main__":
    # Example usage based on legacy script
    sources = [
        "/home/quangnhvn34/fsoft/detect/data_logo_zip/dhl_23_12"
    ]
    move_files_safe(sources, str(Config.SOURCE_DATA_DIR))
