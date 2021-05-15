from abc import ABC, abstractmethod

from aiofile import AIOFile
from loguru import logger

from filler.core.settings import settings


class ABCUploader(ABC):
    @abstractmethod
    async def declare_upload(file_id: str):
        pass

    @abstractmethod
    async def save(file_name: str, data: bytes):
        pass


class LocalStorage(ABCUploader):
    @staticmethod
    async def declare_upload(file_id: str):
        pass

    @staticmethod
    async def save(file_name: str, data: bytes, offset: int):
        async with AIOFile(f"{settings.files_folder}/{file_name}", mode="ab") as file:
            await file.write(data, offset=offset)
            await file.fsync()
            logger.info(f"Writing in the {file_name}")


storage_types = {"local": LocalStorage}

storage = storage_types[settings.storage_type]()
