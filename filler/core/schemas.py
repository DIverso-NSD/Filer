from pydantic import BaseModel
from pydantic.fields import Field


class FileData(BaseModel):
    file_name: str = Field(
        ...,
        example="NSD.zip",
        description="File name for uploaded file",
    )
    file_size: int = Field(..., gt=0, example=1024, description="File size in bytes")


class User(BaseModel):
    id: int = Field(..., example=1, description="User id")
    login: str = Field(..., example="kuder", description="User login")
