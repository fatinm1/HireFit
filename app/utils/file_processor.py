import os
import tempfile
from typing import Optional
from fastapi import UploadFile

class FileProcessor:
    @staticmethod
    async def save_upload_file(upload_file: UploadFile) -> Optional[str]:
        """
        Save uploaded file to temporary directory and return its path
        """
        try:
            # Create a temporary file
            suffix = os.path.splitext(upload_file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                # Write the uploaded file's content to the temporary file
                content = await upload_file.read()
                temp_file.write(content)
                return temp_file.name
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    @staticmethod
    def cleanup_file(file_path: str) -> None:
        """
        Remove temporary file
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning up file: {e}")

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get file extension in lowercase
        """
        return os.path.splitext(filename)[1].lower()

    @staticmethod
    def is_supported_file(filename: str) -> bool:
        """
        Check if file format is supported
        """
        supported_extensions = {'.pdf', '.docx'}
        return FileProcessor.get_file_extension(filename) in supported_extensions 