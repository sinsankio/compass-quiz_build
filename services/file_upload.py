import os
import stat
import shutil

from fastapi import UploadFile


class FileUploadService:
    FILE_UPLOAD_SAVE_ROOT_PATH: str = 'api/uploads'

    @staticmethod
    def write_files(file_save_dir_path: str, files: list[UploadFile]) -> list[str]:
        for file in files:
            file_save_path = os.path.join(file_save_dir_path, file.filename)
            with open(file_save_path, 'wb+') as file_save:
                file_save.write(file.file.read())
        return os.listdir(file_save_dir_path)

    @staticmethod
    def upload_files(dir_name: str, files: list[UploadFile]) -> list[str] | None:
        file_save_dir_path = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, dir_name)
        if not os.path.exists(file_save_dir_path):
            os.mkdir(file_save_dir_path)
            return FileUploadService.write_files(file_save_dir_path, files)

    @staticmethod
    def get_existing_file_names(dir_name: str) -> list[str] | None:
        file_save_dir_path = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, dir_name)
        if os.path.exists(file_save_dir_path):
            return os.listdir(file_save_dir_path)

    @staticmethod
    def update_existing_files(dir_name: str, allowed_file_names: list) -> list[str] | None:
        file_save_dir_path = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, dir_name)
        if os.path.exists(file_save_dir_path):
            file_names = os.listdir(file_save_dir_path)
            for file_name in file_names:
                if file_name not in allowed_file_names:
                    file_path = os.path.join(file_save_dir_path, file_name)
                    os.chmod(file_path, stat.S_IWUSR)
                    os.remove(file_path)
            return os.listdir(file_save_dir_path)

    @staticmethod
    def add_new_files(dir_name: str, files: list[UploadFile]) -> list[str] | None:
        file_save_dir_path = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, dir_name)
        if os.path.exists(file_save_dir_path):
            return FileUploadService.write_files(file_save_dir_path, files)

    @staticmethod
    def delete_existing_files(dir_name: str) -> bool:
        file_save_dir_path = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, dir_name)
        if os.path.exists(file_save_dir_path):
            shutil.rmtree(file_save_dir_path)
            return True
        return False
