import uuid
from datetime import datetime

from fastapi import APIRouter, File, Depends
from loguru import logger

from filler.core.schemas import FileData, User
from filler.core import redis
from filler.core.middleware import verify_token
from filler.core.storages import storage


router = APIRouter()


@router.post("/files", status_code=201)
async def declare_upload(file: FileData, user: User = Depends(verify_token)):
    """
    Says server to create file with random id and returns this id
    """

    file_id = str(uuid.uuid4().hex)
    file_extension = file.file_name.split(".")[-1]
    print(user)

    await redis.dump_data(
        file_id,
        {
            "file_name": file.file_name,
            "file_extension": file_extension,
            "file_size": file.file_size,
            "record_dt": str(datetime.now().isoformat()),
            "received_bytes_lower": 0,
            "owner_id": user.id,
        },
    )

    await storage.declare_upload(file_id)
    logger.info(f"Was created {file_id}")

    return {"file_id": file_id}


@router.put("/files/{file_id}")
async def upload(
    file_id: str,
    file_data: bytes = File(...),
):
    """
    Gets file_name and download bytes to drive with its name
    """
    logger.info(f"Recieved {len(file_data)} bytes")

    file = await redis.load_data(file_id)

    await storage.save(file_id + file["file_extension"], file_data)

    return {"message": f"Uploaded {len(file_data)} for {file_id}"}
