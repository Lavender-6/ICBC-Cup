import os
import shutil
from app.config import settings


def save_upload(file_path: str, dataset_id: str) -> str:
    dest_dir = os.path.join(settings.upload_dir, dataset_id)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, os.path.basename(file_path))
    shutil.move(file_path, dest_path)
    return dest_path


def delete_upload(dataset_id: str):
    dest_dir = os.path.join(settings.upload_dir, dataset_id)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
