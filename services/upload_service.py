# services/upload_service.py

import pandas as pd

class UploadService:
    def upload(self, input_file):
        try:
            data = pd.read_excel(input_file)
            return data
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла: {e}")

