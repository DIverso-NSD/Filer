import uuid
from datetime import datetime

from fastapi import APIRouter, File, Depends
from loguru import logger

from filler.core.schemas import FileData, User
from filler.core.middleware import verify_token
from filler.core.storages import storage
from filler.core import redis
from filler.core import psql


router = APIRouter()


@router.post("/files", status_code=201)
async def declare_upload(
    file: FileData,
    user: User = Depends(verify_token),
):
    """
    Says server to create file with random id and returns this id
    """

    file_id = str(uuid.uuid4().hex)
    file_extension = file.file_name.split(".")[-1]

    await redis.dump_data(
        file_id,
        {
            "file_name": file.file_name,
            "file_extension": file_extension,
            "file_size": file.file_size,
            "record_dt": str(datetime.now().isoformat()),
            "received_bytes": 0,
            "owner_id": user.id,
            "status": "created",
        },
    )

    await storage.declare_upload(file_id)
    await psql.create_file_record(
        file_id, file.file_name, file.file_size, "created", user.id
    )
    logger.info(f"Was created {file.file_name}")

    return {"file_id": file_id}


@router.put("/files/{file_id}")
async def upload(
    file_id: str,
    last_byte: int,
    file_data: bytes = File(...),
    user: User = Depends(verify_token),
):
    """
    Gets file_name and download bytes to drive with its name
    """

    logger.info(f"Recieved {len(file_data)} bytes")
    file = await redis.load_data(file_id)

    if file["received_bytes"] + len(file_data) != last_byte:
        return {"message": "Invalid data chunk"}

    if file["status"] == "done":
        return {"message": "Already uploaded"}

    if file["status"] == "created":
        await psql.patch_file_record("loading", file_id)

    if file["file_size"] < file["received_bytes"] + len(file_data):
        return {"error": "data that has been sent is too big"}

    await storage.save(file_id + file["file_extension"], file_data)

    if file["received_bytes"] + len(file_data) == file["file_size"]:
        await psql.patch_file_record("done", file_id)

        file["received_bytes"] = file["received_bytes"] + len(file_data)
        file["status"] = "done"
        await redis.dump_data(file_id, file)

        return {"message": "finally uploaded"}

    file["received_bytes"] = file["received_bytes"] + len(file_data)
    await redis.dump_data(file_id, file)

    return {
        "message": f"Keep going {len(file_data)} of {file['file_size']} for {file_id}"
    }
