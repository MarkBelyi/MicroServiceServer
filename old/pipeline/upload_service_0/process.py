import pandas as pd

class UploadService:
    def upload(self, file):
        """
        Загрузка данных из входного файла.
        :param file: Файл в формате Excel или CSV.
        :return: DataFrame с данными.
        """
        try:
            if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                data = pd.read_excel(file)
            elif file.filename.endswith('.csv'):
                data = pd.read_csv(file)
            else:
                raise ValueError("Unsupported file format")
            return data
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")
