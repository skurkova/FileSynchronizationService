import os
from typing import Any, Dict

import requests
from loguru import logger


class CloudService:
    def __init__(self, cloud_folder: str, token: str, base_url: str):
        self.cloud_folder = cloud_folder
        self.token = token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"OAuth {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def check_existence_cloud_folder(self) -> Any:
        """Метод создает папку в директории в облачном хранилище, если ее нет"""
        response = requests.get(
            self.base_url, headers=self.headers, params={"path": self.cloud_folder}
        )
        if response.status_code != 200:
            create_response = requests.put(
                self.base_url, headers=self.headers, params={"path": self.cloud_folder}
            )
            return create_response
        return response

    def get_info(self) -> Dict[str, str]:
        """Метод, получения информации о хранящихся в облачном хранилище файлах"""
        response = requests.get(
            self.base_url, headers=self.headers, params={"path": self.cloud_folder}
        )
        cloud_files = {}
        if response.status_code == 200:
            for item in response.json().get("_embedded").get("items"):
                if item["type"] == "file":
                    cloud_files.update({item["name"]: item["modified"]})
            return cloud_files
        else:
            return {}

    def load(self, file_path: str) -> Any:
        """Метод загрузки файла в облачное хранилище"""
        file_name = os.path.basename(file_path)
        response = requests.get(
            f"{self.base_url}/upload",
            headers=self.headers,
            params={"path": f"{self.cloud_folder}/{file_name}", "overwrite": True},
        )
        if response.status_code == 200:
            upload_url = response.json().get("href")
            try:
                with open(file_path, "rb") as file:
                    load_response = requests.put(upload_url, files={"file": file})
            except Exception as exp:
                logger.error(f"Ошибка при чтении файла {file_name}: {exp}")
            return load_response
        else:
            logger.error(
                f'Ошибка запроса URL для загрузки файла {file_name}: {response.json().get("message")}'
            )

    def reload(self, file_path: str) -> Any:
        """Метод перезаписи файла в облачное хранилище"""
        return self.load(file_path=file_path)

    def delete(self, filename: str) -> Any:
        """Метод удаления файла из облачного хранилища"""
        response = requests.delete(
            f"{self.base_url}",
            headers=self.headers,
            params={"path": f"{self.cloud_folder}/{filename}"},
        )
        return response
